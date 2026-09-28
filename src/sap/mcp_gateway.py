"""Evidence gateway for controlled MCP retrieval.

The gateway converts provider-specific MCP results into the same evidence
shape used by AgenteSAP retrieval. It is read-only and does not promote
results to Knowledge automatically.
"""

from __future__ import annotations

import asyncio
import json
import os
import threading
from dataclasses import dataclass
from typing import Coroutine, TypeVar

from src.sap.mcp_client import SapMcpClient
from src.sap.mcp_registry import build_target
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
                args=tuple(os.getenv("AGENTESAP_MCP_ARGS", "mcp serve").split()),
                max_results=max_results,
            )
        )

    async def _search_resources(self, query: str):
        async with SapMcpClient(self.target) as client:
            return await client.call_read_tool(
                "search_resources",
                {"query": query, "limit": self.config.max_results},
            )

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
                source_id=f"{evidence.provider}:{evidence.operation}",
                knowledge_type="developer_context",
                knowledge_scope="external",
                certainty=evidence.certainty,
            ),
        )


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
