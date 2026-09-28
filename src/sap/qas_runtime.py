"""Configuration contract for the first SAP runtime integration stage.

This stage is deliberately limited to QAS and read-only MCP access. It does
not contain credentials and it does not infer concrete tool names.
"""

from __future__ import annotations

import os
import shlex
from dataclasses import dataclass


@dataclass(frozen=True)
class SapQasRuntimeConfig:
    """Explicit QAS/read-only runtime MCP configuration."""

    command: str
    args: tuple[str, ...]
    allowed_tools: tuple[str, ...]
    landscape: str
    scope: str
    system: str | None = None
    query_tool: str | None = None
    query_argument: str = "query"
    discovery_only: bool = False
    enabled: bool = False

    def validate(self) -> None:
        if not self.enabled:
            return
        if self.landscape != "QAS":
            raise ValueError(
                "SAP runtime integration is currently restricted to landscape QAS"
            )
        if self.scope != "mcp_readonly":
            raise ValueError(
                "QAS runtime integration requires the mcp_readonly scope"
            )
        if not self.allowed_tools and not self.discovery_only:
            raise ValueError(
                "QAS runtime integration requires an explicit read-tool allowlist "
                "unless discovery_only is enabled"
            )
        if self.discovery_only and self.allowed_tools:
            raise ValueError(
                "discovery_only mode must not pre-authorize runtime tools"
            )
        if not self.command:
            raise ValueError("QAS runtime integration requires a server command")
        if not self.discovery_only and not self.query_tool:
            raise ValueError("QAS runtime integration requires an explicit query tool")
        if (
            not self.discovery_only
            and self.query_tool not in self.allowed_tools
        ):
            raise ValueError("QAS runtime query tool must be explicitly allowlisted")
        if not self.query_argument.strip():
            raise ValueError("QAS runtime integration requires a non-empty query argument")

    @classmethod
    def from_env(cls) -> "SapQasRuntimeConfig":
        enabled = os.getenv("AGENTESAP_SAP_RUNTIME_ENABLED", "").lower() in {
            "1",
            "true",
            "yes",
            "on",
        }
        raw_tools = os.getenv("AGENTESAP_SAP_RUNTIME_READ_TOOLS", "")
        allowed_tools = tuple(
            tool.strip() for tool in raw_tools.split(",") if tool.strip()
        )
        config = cls(
            command=os.getenv("AGENTESAP_SAP_MCP_COMMAND", "sap-mcp-server"),
            args=tuple(
                shlex.split(
                    os.getenv("AGENTESAP_SAP_MCP_ARGS", "")
                )
            ),
            allowed_tools=allowed_tools,
            landscape=os.getenv("AGENTESAP_SAP_RUNTIME_LANDSCAPE", "QAS").upper(),
            scope=os.getenv("AGENTESAP_SAP_RUNTIME_SCOPE", "mcp_readonly"),
            system=os.getenv("AGENTESAP_SAP_RUNTIME_SYSTEM") or None,
            query_tool=os.getenv("AGENTESAP_SAP_RUNTIME_QUERY_TOOL") or None,
            query_argument=os.getenv("AGENTESAP_SAP_RUNTIME_QUERY_ARGUMENT", "query"),
            discovery_only=os.getenv(
                "AGENTESAP_SAP_RUNTIME_DISCOVERY", ""
            ).lower() in {"1", "true", "yes", "on"},
            enabled=enabled,
        )
        config.validate()
        return config
