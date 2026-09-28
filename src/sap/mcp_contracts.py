"""Contracts for controlled SAP MCP integrations.

The repository keeps MCP providers behind an explicit read-only boundary.
Credentials and live connection settings never belong in Git.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal


McpProvider = Literal["sap_devs", "sap_mcp_server", "abap_ai"]
McpTransport = Literal["stdio", "streamable_http"]
McpObservationType = Literal[
    "developer_context",
    "runtime_observation",
    "custom_runtime_observation",
    "external_source",
]


@dataclass(frozen=True)
class McpTarget:
    """A configured MCP endpoint with an explicit read-tool allowlist."""

    provider: McpProvider
    transport: McpTransport
    command: str | None = None
    args: tuple[str, ...] = ()
    url: str | None = None
    allowed_tools: tuple[str, ...] = ()
    profile: str | None = None
    read_only: bool = True
    observation_type: McpObservationType = "external_source"
    metadata: dict[str, str] = field(default_factory=dict)

    def validate(self) -> None:
        if self.transport == "stdio" and not self.command:
            raise ValueError("stdio targets require command")
        if self.transport == "streamable_http" and not self.url:
            raise ValueError("streamable_http targets require url")
        if not self.allowed_tools:
            raise ValueError("allowed_tools must be explicit; empty means deny-all")
        if not self.read_only:
            raise ValueError(
                "AgenteSAP currently permits only read-only MCP integration"
            )


@dataclass(frozen=True)
class SapMcpEvidence:
    """Normalized provenance envelope for evidence returned by an MCP provider."""

    provider: str
    operation: str
    content: object
    source: str
    system: str | None = None
    landscape: str | None = None
    object_id: str | None = None
    certainty: str = "under_validation"
    observation_type: str = "external_source"
    provenance: dict[str, str] = field(default_factory=dict)

    def as_metadata(self) -> dict[str, str]:
        result = {
            "provider": self.provider,
            "operation": self.operation,
            "source": self.source,
            "certainty": self.certainty,
            "observation_type": self.observation_type,
        }
        if self.system:
            result["system"] = self.system
        if self.landscape:
            result["landscape"] = self.landscape
        if self.object_id:
            result["object_id"] = self.object_id
        result.update(self.provenance)
        return result
