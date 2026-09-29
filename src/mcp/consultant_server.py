"""Read-only MCP facade for the AgenteSAP consultant."""
from __future__ import annotations

import hmac
import os
from dataclasses import asdict

import uvicorn
from mcp.server.mcpserver import MCPServer
from mcp.server.transport_security import TransportSecuritySettings
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.routing import Route

from src.agent.router import run_agent
from src.github.client import GitHubClient
from src.investigation.engine import investigate

SERVER_NAME = "agentesap-consultant"
mcp = MCPServer(SERVER_NAME)


def _client() -> GitHubClient:
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise RuntimeError("GITHUB_TOKEN is required by the AgenteSAP MCP server")
    return GitHubClient(
        os.getenv("GITHUB_OWNER", "araortiz99"),
        os.getenv("GITHUB_REPO", "agenteSAP"),
        token=token,
    )


def _ref() -> str:
    configured = os.getenv("GITHUB_REF_NAME") or os.getenv("GITHUB_REF") or "main"
    for prefix in ("refs/heads/", "refs/tags/"):
        if configured.startswith(prefix):
            return configured[len(prefix) :]
    return configured


def _limit(value: int) -> int:
    if value < 1 or value > 20:
        raise ValueError("max_results must be between 1 and 20")
    return value


def _auth_required() -> bool:
    return os.getenv("AGENTESAP_MCP_AUTH_REQUIRED", "true").strip().lower() in {
        "1",
        "true",
        "yes",
        "on",
    }


def _bearer_token() -> str:
    token = os.getenv("AGENTESAP_MCP_BEARER_TOKEN")
    if _auth_required() and not token:
        raise RuntimeError(
            "AGENTESAP_MCP_BEARER_TOKEN is required when MCP authentication is enabled"
        )
    return token or ""


def _authorize_http(scope: dict[str, object]) -> bool:
    if not _auth_required():
        return True
    headers = {
        key.decode("latin-1").lower(): value.decode("latin-1")
        for key, value in scope.get("headers", [])
    }
    authorization = headers.get("authorization", "")
    if not authorization.startswith("Bearer "):
        return False
    supplied = authorization.removeprefix("Bearer ").strip()
    expected = _bearer_token()
    return bool(supplied) and hmac.compare_digest(supplied, expected)


class BearerAuthASGI:
    """Small raw ASGI auth layer; intentionally outside the MCP tool schema."""

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http" or scope.get("path") != "/mcp":
            await self.app(scope, receive, send)
            return

        if not _authorize_http(scope):
            response = JSONResponse(
                {"error": "authentication_required"},
                status_code=401,
                headers={"WWW-Authenticate": "Bearer"},
            )
            await response(scope, receive, send)
            return

        await self.app(scope, receive, send)


async def healthz(_: Request) -> Response:
    return JSONResponse(
        {
            "status": "ok",
            "service": SERVER_NAME,
            "read_only": True,
            "auth_required": _auth_required(),
            "qas_runtime_enabled": os.getenv(
                "AGENTESAP_SAP_RUNTIME_ENABLED", ""
            ).lower()
            in {"1", "true", "yes", "on"},
        }
    )


@mcp.tool()
def consult_sap(
    request: str,
    ticket_id: str | None = None,
    max_results: int = 8,
) -> dict[str, object]:
    """Consult AgenteSAP with bounded, evidence-first, read-only reasoning."""
    if not request or not request.strip():
        raise ValueError("request must not be empty")
    response = run_agent(
        _client(),
        request.strip(),
        ref=_ref(),
        ticket_id=ticket_id,
        max_results=_limit(max_results),
    )
    payload = {
        "read_only": True,
        "request": response.request,
        "intent": response.plan.intent,
        "ticket_id": response.plan.ticket_id,
    }
    result = response.result
    if hasattr(result, "answer"):
        payload.update(
            {
                "answer": result.answer,
                "citations": [asdict(x) for x in getattr(result, "citations", ())],
                "traceability": asdict(result.traceability),
                "evidence_count": len(result.traceability.evidence),
                "uncited_evidence_ids": list(
                    getattr(result, "uncited_evidence_ids", ())
                ),
            }
        )
    else:
        payload["result"] = (
            asdict(result) if hasattr(result, "__dataclass_fields__") else result
        )
    return payload


@mcp.tool()
def investigate_sap(
    request: str,
    max_steps: int = 5,
    max_results: int = 8,
) -> dict[str, object]:
    """Run bounded investigation without LLM synthesis; read-only."""
    if not request or not request.strip():
        raise ValueError("request must not be empty")
    if max_steps < 1 or max_steps > 10:
        raise ValueError("max_steps must be between 1 and 10")
    max_results = _limit(max_results)
    result = investigate(
        _client(),
        request.strip(),
        ref=_ref(),
        max_steps=max_steps,
        max_results=max_results,
    )
    return {
        "read_only": True,
        "query": result.query,
        "intent": result.plan.intent,
        "conclusion_status": result.conclusion_status,
        "conclusion": result.conclusion,
        "conclusion_reason": result.conclusion_reason,
        "findings": list(result.findings),
        "gaps": list(result.evidence.gaps),
        "evidence": [asdict(x) for x in result.report.evidence]
        if result.report
        else [],
        "hypotheses": [asdict(x) for x in result.hypotheses],
    }


@mcp.tool()
def agentesap_health() -> dict[str, object]:
    """Return non-secret service configuration metadata."""
    return {
        "service": SERVER_NAME,
        "read_only": True,
        "github_configured": bool(os.getenv("GITHUB_TOKEN")),
        "public_sap_mcp_enabled": os.getenv(
            "AGENTESAP_SAP_PUBLIC_MCP_ENABLED", ""
        ).lower()
        in {"1", "true", "yes", "on"},
        "qas_runtime_enabled": os.getenv(
            "AGENTESAP_SAP_RUNTIME_ENABLED", ""
        ).lower()
        in {"1", "true", "yes", "on"},
        "auth_required": _auth_required(),
        "ref": _ref(),
    }


def _allowed_hosts() -> list[str]:
    raw = os.getenv(
        "AGENTESAP_MCP_ALLOWED_HOSTS",
        "agentesap-consultant-mcp.onrender.com:*",
    )
    return [item.strip() for item in raw.split(",") if item.strip()]


def _build_http_app():
    _bearer_token()
    transport_security = TransportSecuritySettings(
        allowed_hosts=_allowed_hosts(),
        allowed_origins=[
            f"https://{host.removesuffix(':*')}"
            for host in _allowed_hosts()
            if host.endswith(":*")
        ],
    )
    app = mcp.streamable_http_app(
        streamable_http_path=os.getenv("AGENTESAP_MCP_SERVER_PATH", "/mcp"),
        stateless_http=True,
        json_response=True,
        host=os.getenv("AGENTESAP_MCP_SERVER_HOST", "0.0.0.0"),
        transport_security=transport_security,
        custom_starlette_routes=[Route("/healthz", healthz, methods=["GET"])],
    )
    return BearerAuthASGI(app)


def main() -> None:
    transport = os.getenv("AGENTESAP_MCP_SERVER_TRANSPORT", "stdio").strip()
    if transport not in {"stdio", "streamable-http"}:
        raise ValueError(
            "AGENTESAP_MCP_SERVER_TRANSPORT must be 'stdio' or 'streamable-http'"
        )

    if transport == "stdio":
        mcp.run(transport="stdio")
        return

    app = _build_http_app()
    uvicorn.run(
        app,
        host=os.getenv("AGENTESAP_MCP_SERVER_HOST", "0.0.0.0"),
        port=int(os.getenv("AGENTESAP_MCP_SERVER_PORT", "8000")),
    )


if __name__ == "__main__":
    main()
