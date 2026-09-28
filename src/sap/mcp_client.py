"""Read-only MCP client adapter supporting stdio and Streamable HTTP."""

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
    def __init__(self, target: McpTarget) -> None:
        target.validate()
        if target.transport == "stdio" and not target.command:
            raise ValueError("stdio targets require command")
        if target.transport == "streamable_http" and not target.url:
            raise ValueError("streamable_http targets require url")
        if target.transport not in {"stdio", "streamable_http"}:
            raise ValueError(f"unsupported MCP transport: {target.transport}")
        self.target = target
        self._client: Client | None = None
        self._context_manager: Any | None = None

    async def __aenter__(self) -> "SapMcpClient":
        transport = (
            StdioServerParameters(command=self.target.command, args=list(self.target.args))
            if self.target.transport == "stdio"
            else self.target.url
        )
        self._context_manager = Client(transport)
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
        result = await self._require_connected().list_tools()
        return tuple(
            McpToolDescriptor(
                name=tool.name,
                description=str(getattr(tool, "description", "") or ""),
                input_schema=getattr(tool, "inputSchema", {}),
                read_only_hint=getattr(getattr(tool, "annotations", None), "readOnlyHint", None),
                destructive_hint=getattr(getattr(tool, "annotations", None), "destructiveHint", None),
            )
            for tool in result.tools
        )

    def server_info(self) -> McpServerInfo | None:
        info = self._require_connected().server_info
        return None if info is None else McpServerInfo(name=info.name, version=info.version)

    async def call_read_tool(self, tool_name: str, arguments: dict[str, Any] | None = None) -> SapMcpEvidence:
        if tool_name not in self.target.allowed_tools:
            raise PermissionError(
                f"MCP tool '{tool_name}' is not allowed for provider '{self.target.provider}'"
            )
        descriptor = next((x for x in await self.list_tool_descriptors() if x.name == tool_name), None)
        if descriptor is None:
            raise PermissionError(f"MCP tool '{tool_name}' is not advertised by the connected server")
        if descriptor.read_only_hint is False:
            raise PermissionError(f"MCP tool '{tool_name}' is not marked read-only by the server")
        if self.target.observation_type in {"runtime_observation", "custom_runtime_observation"}                 and descriptor.read_only_hint is not True:
            raise PermissionError(f"MCP tool '{tool_name}' requires an explicit read-only hint for runtime execution")
        if descriptor.destructive_hint is True:
            raise PermissionError(f"MCP tool '{tool_name}' is marked destructive by the server")
        result = await self._require_connected().call_tool(tool_name, arguments or {})
        content = [getattr(item, "text", item) for item in getattr(result, "content", ())]
        return SapMcpEvidence(
            provider=self.target.provider, operation=tool_name, content=content,
            source=f"MCP provider: {self.target.provider}",
            system=self.target.metadata.get("system"),
            landscape=self.target.metadata.get("landscape"),
            certainty=("partial" if self.target.observation_type in {"runtime_observation", "custom_runtime_observation"}
                       else "external_source"),
            observation_type=self.target.observation_type,
            provenance={
                "transport": self.target.transport,
                "tool_description": descriptor.description,
                "tool_read_only_hint": descriptor.read_only_hint,
                "tool_destructive_hint": descriptor.destructive_hint,
                "tool_input_schema": descriptor.input_schema,
            },
        )
