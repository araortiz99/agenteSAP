"""Local HTTP application shell for AgenteSAP.

This is intentionally a thin presentation layer over the existing agent.
It binds to localhost by default and never introduces SAP write operations.
"""

from __future__ import annotations

import argparse
from dataclasses import asdict, is_dataclass
import json
import os
import time
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

from src.agent.router import run_agent
from src.llm.client import LLMConfigurationError
from src.github.client import GitHubAPIError, GitHubClient
from src.agent.consultant import ConsultationResult
from src.app.contracts import build_workbench_analysis


APP_ROOT = Path(__file__).resolve().parent
INDEX = APP_ROOT / "static" / "index.html"
MAX_RESULTS = 20

_GITHUB_CLIENT: GitHubClient | None = None
_GITHUB_CLIENT_CONFIG: tuple[str, str, str | None] | None = None


def _response_payload(response: object) -> dict:
    if not is_dataclass(response):
        return {"result": str(response)}
    return asdict(response)


def _github_client() -> GitHubClient:
    """Reuse one read-only GitHub client so repository data is cached across requests."""
    global _GITHUB_CLIENT, _GITHUB_CLIENT_CONFIG

    config = (
        os.getenv("GITHUB_OWNER", "araortiz99"),
        os.getenv("GITHUB_REPO", "agenteSAP"),
        os.getenv("GITHUB_TOKEN"),
    )
    if _GITHUB_CLIENT is None or _GITHUB_CLIENT_CONFIG != config:
        _GITHUB_CLIENT = GitHubClient(*config)
        _GITHUB_CLIENT_CONFIG = config
    return _GITHUB_CLIENT


def _validated_max_results(value: object) -> int:
    try:
        max_results = int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError("max_results must be an integer") from exc
    if not 1 <= max_results <= MAX_RESULTS:
        raise ValueError(f"max_results must be between 1 and {MAX_RESULTS}")
    return max_results




def _runtime_payload(status: dict) -> dict:
    if status["qas_runtime_enabled"]:
        return {
            "mode": "QAS",
            "access": "read-only",
            "status": "enabled_not_verified",
            "writes_exposed": False,
        }
    return {
        "mode": "QAS",
        "access": "read-only",
        "status": "disabled",
        "writes_exposed": False,
    }


def _workbench_payload(
    response: object,
    *,
    request_id: str,
    intent: str,
    started_at: float,
) -> dict:
    legacy = _response_payload(response)
    status = _status_payload()
    runtime = _runtime_payload(status)

    if not isinstance(response, ConsultationResult):
        return {
            "request_id": request_id,
            "query": getattr(response, "request", ""),
            "intent": intent,
            **legacy,
            "workbench": {
                "request_id": request_id,
                "query": getattr(response, "request", ""),
                "intent": intent,
                "runtime": runtime,
                "diagnostics": {
                    "request_id": request_id,
                    "trace_id": None,
                    "intent": intent,
                    "evidence_count": 0,
                    "conflicts": 0,
                    "gaps": 0,
                    "llm_used": False,
                    "llm_latency_ms": None,
                    "retrieval_latency_ms": None,
                    "total_latency_ms": round((time.perf_counter() - started_at) * 1000, 2),
                    "runtime_status": runtime["status"],
                },
            },
            "diagnostics": {
                "request_id": request_id,
                "trace_id": None,
                "intent": intent,
                "evidence_count": 0,
                "conflicts": 0,
                "gaps": 0,
                "llm_used": False,
                "llm_latency_ms": None,
                "retrieval_latency_ms": None,
                "total_latency_ms": round((time.perf_counter() - started_at) * 1000, 2),
                "runtime_status": runtime["status"],
            },
        }

    diagnostics = {
        "request_id": request_id,
        "trace_id": response.traceability.trace_id,
        "intent": intent,
        "sources_retrieved": tuple(
            sorted({item.source_layer for item in response.traceability.evidence})
        ),
        "evidence_count": len(response.traceability.evidence),
        "conflicts": len(response.evidence.conflicts),
        "gaps": len(response.traceability.gaps),
        "llm_used": bool(response.model),
        "llm_model": response.model,
        "llm_latency_ms": None,
        "retrieval_latency_ms": None,
        "total_latency_ms": round((time.perf_counter() - started_at) * 1000, 2),
        "runtime_status": runtime["status"],
    }
    structured = build_workbench_analysis(
        response,
        request_id=request_id,
        intent=intent,
        diagnostics=diagnostics,
        runtime=runtime,
    )
    return {
        **legacy,
        "workbench": asdict(structured),
    }

def _status_payload() -> dict:
    client = _github_client()
    return {
        "agent": "ready",
        "mode": "local-read-only",
        "github_owner": client.owner,
        "github_repo": client.repo,
        "github_ref": os.getenv("GITHUB_REF", "main"),
        "github_token_configured": client.authenticated,
        "openai_api_key_configured": bool(os.getenv("OPENAI_API_KEY")),
        "github_cache_files": len(client._file_cache),
        "github_cache_trees": len(client._tree_cache),
        "qas_runtime_enabled": os.getenv(
            "AGENTESAP_SAP_RUNTIME_ENABLED", "false"
        ).lower() in {"1", "true", "yes", "on"},
        "sap_writes_exposed": False,
    }


class AgentRequestHandler(BaseHTTPRequestHandler):
    server_version = "AgenteSAPLocal/0.2"

    def _send_json(self, status: int, payload: dict) -> None:
        encoded = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(encoded)

    def _send_html(self) -> None:
        encoded = INDEX.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def do_GET(self) -> None:  # noqa: N802
        path = urlparse(self.path).path
        if path == "/":
            self._send_html()
            return
        if path == "/health":
            self._send_json(200, {
                "status": "ok",
                "mode": "local-read-only",
                "sap_writes_exposed": False,
            })
            return
        if path == "/api/status":
            self._send_json(200, _status_payload())
            return
        self._send_json(404, {"error": "not_found"})

    def do_POST(self) -> None:  # noqa: N802
        if urlparse(self.path).path != "/api/consult":
            self._send_json(404, {"error": "not_found"})
            return

        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length <= 0 or length > 64_000:
                raise ValueError("request body must be between 1 and 64000 bytes")
            body = json.loads(self.rfile.read(length).decode("utf-8"))
            request = str(body.get("request", "")).strip()
            if not request:
                raise ValueError("request is required")

            request_id = "REQ-" + uuid.uuid4().hex[:12].upper()
            started_at = time.perf_counter()
            response = run_agent(
                _github_client(),
                request,
                ref=os.getenv("GITHUB_REF", "main"),
                ticket_id=body.get("ticket_id"),
                max_results=_validated_max_results(body.get("max_results", 8)),
            )
            self._send_json(200, _workbench_payload(response, request_id=request_id, intent=getattr(getattr(response, "plan", None), "intent", "unknown"), started_at=started_at))
        except (ValueError, json.JSONDecodeError) as exc:
            self._send_json(400, {"error": str(exc)})
        except GitHubAPIError as exc:
            payload = {
                "error": str(exc),
                "error_type": "github_api",
                "status_code": exc.status_code,
            }
            if exc.rate_limit.remaining is not None:
                payload["github_rate_limit_remaining"] = exc.rate_limit.remaining
            if exc.rate_limit.reset_epoch is not None:
                payload["github_rate_limit_reset_epoch"] = exc.rate_limit.reset_epoch
            if exc.rate_limit.retry_after is not None:
                payload["github_retry_after_seconds"] = exc.rate_limit.retry_after
            self._send_json(503 if exc.status_code in {403, 429, 500, 502, 503, 504} else 502, payload)
        except LLMConfigurationError as exc:
            self._send_json(503, {"error": str(exc), "error_type": "llm_configuration"})
        except TimeoutError as exc:
            self._send_json(504, {"error": f"agent_timeout: {exc}"})
        except Exception as exc:  # local shell: expose failure without claiming SAP execution
            self._send_json(500, {"error": f"agent_error: {exc}"})

    def log_message(self, format: str, *args: object) -> None:
        return


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the local AgenteSAP web app.")
    parser.add_argument("--host", default=os.getenv("AGENTESAP_APP_HOST", "127.0.0.1"))
    parser.add_argument("--port", type=int, default=int(os.getenv("AGENTESAP_APP_PORT", "8765")))
    args = parser.parse_args()

    if args.host not in {"127.0.0.1", "localhost", "::1"}:
        parser.error("The local app must bind to localhost only.")

    server = ThreadingHTTPServer((args.host, args.port), AgentRequestHandler)
    print(f"AgenteSAP local app: http://{args.host}:{args.port}")
    print("Mode: read-only consultant; SAP writes are not exposed.")
    print(
        "GitHub token: "
        + ("configured" if _github_client().authenticated else "not configured")
    )
    print("")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
