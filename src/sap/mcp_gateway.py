"""Evidence gateway for controlled MCP retrieval.

The gateway converts provider-specific MCP results into the same evidence
shape used by AgenteSAP retrieval. It is read-only and does not promote
results to Knowledge automatically.
"""

from __future__ import annotations

import asyncio
import json
import os
import shlex
import threading
from dataclasses import dataclass
from typing import Coroutine, TypeVar

from src.sap.mcp_client import SapMcpClient
from src.sap.mcp_registry import build_target
from src.sap.qas_runtime import SapQasRuntimeConfig
from src.sap.mcp_strategy import McpEvidenceLayer, McpProviderPlan, plan_mcp_provider
from src.tools.search_unified import UnifiedResult


T = TypeVar("T")


@dataclass(frozen=True)
class McpGatewayConfig:
    command: str = "sap-devs"
    args: tuple[str, ...] = ("mcp", "serve")
    max_results: int = 5


class McpEvidenceGateway:
    """Single entry point for read-only MCP evidence retrieval."""

    def __init__(self, config: McpGatewayConfig | None = None) -> None:
        self.config = config or McpGatewayConfig()
        self.target = build_target(
            "sap_devs",
            command=self.config.command,
            args=self.config.args,
        )

    @classmethod
    def from_env(cls) -> "McpEvidenceGateway | None":
        enabled = os.getenv("AGENTESAP_MCP_ENABLED", "").lower() in {
            "1", "true", "yes", "on"
        }
        if not enabled:
            return None
        raw_limit = os.getenv("AGENTESAP_MCP_MAX_RESULTS", "5")
        try:
            max_results = max(1, min(int(raw_limit), 10))
        except ValueError as exc:
            raise ValueError("AGENTESAP_MCP_MAX_RESULTS must be an integer") from exc
        return cls(
            McpGatewayConfig(
                command=os.getenv("AGENTESAP_MCP_COMMAND", "sap-devs"),
                args=tuple(shlex.split(os.getenv("AGENTESAP_MCP_ARGS", "mcp serve"))),
                max_results=max_results,
            )
        )

    async def _search_resources(self, query: str):
        async with SapMcpClient(self.target) as client:
            return await client.call_read_tool(
                "search_resources",
                {"query": query, "limit": self.config.max_results},
            )

    def provider_plan(self, source: McpEvidenceLayer) -> McpProviderPlan:
        """Expose the fail-closed provider decision without connecting to MCP."""
        return plan_mcp_provider(
            source,
            configured_provider=self.target.provider,
        )

    def supports_source(self, source: str) -> bool:
        """Return whether this gateway can provide the requested evidence layer."""
        if source not in {"runtime", "external"}:
            return False
        return self.provider_plan(source).ready

    @classmethod
    def from_qas_runtime_env(cls) -> "McpEvidenceGateway | None":
        """Build the opt-in QAS runtime gateway without exposing credentials."""
        config = SapQasRuntimeConfig.from_env()
        if not config.enabled:
            return None

        gateway = cls.__new__(cls)
        gateway.config = McpGatewayConfig(
            command=config.command,
            args=config.args,
            max_results=5,
        )
        gateway.target = build_target(
            "sap_mcp_server",
            command=config.command,
            args=config.args,
            allowed_tools=config.allowed_tools,
            metadata={
                "landscape": config.landscape,
                **({"system": config.system} if config.system else {}),
            },
        )
        return gateway

    def read_runtime(
        self,
        tool_name: str,
        arguments: dict[str, object] | None = None,
    ) -> SapMcpEvidence:
        """Execute one explicitly allowlisted QAS read tool."""
        if self.target.provider != "sap_mcp_server":
            raise PermissionError("runtime reads require sap_mcp_server")
        if self.target.metadata.get("landscape") != "QAS":
            raise PermissionError("runtime reads are restricted to QAS")
        if tool_name not in self.target.allowed_tools:
            raise PermissionError(
                f"MCP runtime tool '{tool_name}' is not allowlisted"
            )

        evidence = _run_async(
            self._call_runtime_tool(tool_name, arguments or {})
        )
        if evidence.landscape != "QAS":
            raise ValueError("runtime evidence must identify landscape QAS")
        return evidence

    async def _call_runtime_tool(
        self,
        tool_name: str,
        arguments: dict[str, object],
    ) -> SapMcpEvidence:
        async with SapMcpClient(self.target) as client:
            return await client.call_read_tool(tool_name, arguments)

    def search_resources(self, query: str) -> tuple[UnifiedResult, ...]:
        if not query or not query.strip():
            raise ValueError("query must not be empty")

        evidence = _run_async(self._search_resources(query.strip()))
        if _has_zero_results(evidence.content):
            return ()

        rendered = _render_content(evidence.content)
        return (
            UnifiedResult(
                path=f"mcp://{evidence.provider}/{evidence.operation}",
                score=0.9,
                matched_terms=tuple(query.strip().split()),
                content=rendered,
                source_layer="mcp",
                match_type="mcp",
                source_id=(
                    getattr(evidence, "object_id", None)
                    or f"{evidence.provider}:{evidence.operation}"
                ),
                knowledge_type=(
                    "runtime_observation"
                    if getattr(evidence, "observation_type", None)
                    in {"runtime_observation", "custom_runtime_observation"}
                    else "developer_context"
                ),
                knowledge_scope=(
                    "runtime"
                    if getattr(evidence, "observation_type", None)
                    in {"runtime_observation", "custom_runtime_observation"}
                    else "external"
                ),
                certainty=evidence.certainty,
                provenance=tuple(
                    (
                        (key, value)
                        for key, value in (
                            ("provider", evidence.provider),
                            ("operation", evidence.operation),
                            ("system", getattr(evidence, "system", None)),
                            ("landscape", getattr(evidence, "landscape", None)),
                            ("object_id", getattr(evidence, "object_id", None)),
                            ("observation_type", getattr(evidence, "observation_type", None)),
                        )
                        if value
                    )
                ),
            ),
        )



def _run_async(coro: Coroutine[object, object, T]) -> T:
    """Run an MCP coroutine from sync code, including an active event loop."""
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        return asyncio.run(coro)

    result: list[T] = []
    error: list[BaseException] = []

    def runner() -> None:
        try:
            result.append(asyncio.run(coro))
        except BaseException as exc:
            error.append(exc)

    thread = threading.Thread(target=runner, name="agentesap-mcp", daemon=True)
    thread.start()
    thread.join()

    if error:
        raise error[0]
    if not result:
        raise RuntimeError("MCP coroutine completed without a result")
    return result[0]


def _has_zero_results(content: object) -> bool:
    items = content if isinstance(content, (list, tuple)) else [content]
    for item in items:
        if isinstance(item, str):
            try:
                item = json.loads(item)
            except json.JSONDecodeError:
                continue
        if isinstance(item, dict):
            if item.get("count") == 0 or item.get("total") == 0:
                return True
            results = item.get("results")
            if isinstance(results, list) and not results:
                return True
    return False


def _render_content(content: object) -> str:
    if isinstance(content, (list, tuple)):
        parts = []
        for item in content:
            if isinstance(item, str):
                try:
                    parts.append(json.dumps(json.loads(item), ensure_ascii=False, indent=2))
                except json.JSONDecodeError:
                    parts.append(item)
            else:
                parts.append(str(item))
        return "\n".join(parts)
    if isinstance(content, str):
        return content
    return json.dumps(content, ensure_ascii=False, indent=2)
