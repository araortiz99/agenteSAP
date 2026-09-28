"""Minimal read-only MCP client adapter for AgenteSAP.

The adapter deliberately stays provider-agnostic at the contract level while
using the official Python MCP SDK for stdio sessions.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from mcp import Client, StdioServerParameters

from src.sap.mcp_contracts import McpTarget, SapMcpEvidence


@dataclass(frozen=True)
class McpServerInfo:
    name: str
    version: str


@dataclass(frozen=True)
class McpToolDescriptor:
    name: str
    description: str
    input_schema: object
    read_only_hint: bool | None = None
    destructive_hint: bool | None = None


class SapMcpClient:
    """Async read-only client for an MCP stdio target."""

    def __init__(self, target: McpTarget) -> None:
        target.validate()
        if target.transport != "stdio":
            raise ValueError("SapMcpClient currently supports stdio targets only")
        if not target.command:
            raise ValueError("stdio target requires command")

        self.target = target
        self._client: Client | None = None
        self._context_manager: Any | None = None

    async def __aenter__(self) -> "SapMcpClient":
        server = StdioServerParameters(
            command=self.target.command,
            args=list(self.target.args),
        )
        self._context_manager = Client(server)
        self._client = await self._context_manager.__aenter__()
        return self

    async def __aexit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
        if self._context_manager is not None:
            await self._context_manager.__aexit__(exc_type, exc, tb)
        self._client = None
        self._context_manager = None

    def _require_connected(self) -> Client:
        if self._client is None:
            raise RuntimeError("MCP client is not connected")
        return self._client

    async def list_tools(self) -> tuple[str, ...]:
        result = await self._require_connected().list_tools()
        return tuple(tool.name for tool in result.tools)

    async def list_tool_descriptors(self) -> tuple[McpToolDescriptor, ...]:
        """Return the provider's tool catalog without executing any tool."""
        result = await self._require_connected().list_tools()
        descriptors = []
        for tool in result.tools:
            annotations = getattr(tool, "annotations", None)
            descriptors.append(
                McpToolDescriptor(
                    name=tool.name,
                    description=str(getattr(tool, "description", "") or ""),
                    input_schema=getattr(tool, "inputSchema", {}),
                    read_only_hint=getattr(annotations, "readOnlyHint", None)
                    if annotations is not None
                    else None,
                    destructive_hint=getattr(annotations, "destructiveHint", None)
                    if annotations is not None
                    else None,
                )
            )
        return tuple(descriptors)

    def server_info(self) -> McpServerInfo | None:
        info = self._require_connected().server_info
        if info is None:
            return None
        return McpServerInfo(name=info.name, version=info.version)

    async def call_read_tool(
        self,
        tool_name: str,
        arguments: dict[str, Any] | None = None,
    ) -> SapMcpEvidence:
        """Call one explicitly allowlisted read tool and normalize its output."""

        if tool_name not in self.target.allowed_tools:
            raise PermissionError(
                f"MCP tool '{tool_name}' is not allowed for provider "
                f"'{self.target.provider}'"
            )

        descriptors = await self.list_tool_descriptors()
        descriptor = next(
            (item for item in descriptors if item.name == tool_name),
            None,
        )
        if descriptor is None:
            raise PermissionError(
                f"MCP tool '{tool_name}' is not advertised by the connected server"
            )
        if descriptor.read_only_hint is not True:
            raise PermissionError(
                f"MCP tool '{tool_name}' does not explicitly advertise readOnlyHint=true"
            )
        if descriptor.destructive_hint is True:
            raise PermissionError(
                f"MCP tool '{tool_name}' is marked destructive by the server"
            )

        result = await self._require_connected().call_tool(
            tool_name,
            arguments or {},
        )

        content = [
            getattr(item, "text", item)
            for item in getattr(result, "content", ())
        ]

        return SapMcpEvidence(
            provider=self.target.provider,
            operation=tool_name,
            content=content,
            source=f"MCP provider: {self.target.provider}",
            system=self.target.metadata.get("system"),
            landscape=self.target.metadata.get("landscape"),
            certainty="partial"
            if self.target.observation_type
            in {"runtime_observation", "custom_runtime_observation"}
            else "external_source",
            observation_type=self.target.observation_type,
            provenance={"transport": self.target.transport},
        )
