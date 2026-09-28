"""Provider profiles for SAP MCP integrations.

Profiles describe how AgenteSAP may connect; they never contain credentials.
Live credentials remain in the provider/client environment.
"""

from __future__ import annotations

from dataclasses import dataclass

from src.sap.mcp_contracts import (
    McpObservationType,
    McpProvider,
    McpTarget,
    McpTransport,
)


@dataclass(frozen=True)
class ProviderProfile:
    provider: McpProvider
    purpose: str
    transport: McpTransport
    default_read_tools: tuple[str, ...]
    observation_type: McpObservationType
    default_command: str | None = None
    default_args: tuple[str, ...] = ()


PROVIDERS: dict[McpProvider, ProviderProfile] = {
    "sap_devs": ProviderProfile(
        provider="sap_devs",
        purpose="Current curated SAP developer knowledge and SAP resources.",
        transport="stdio",
        observation_type="developer_context",
        default_read_tools=(
            "list_packs",
            "get_context",
            "search_resources",
            "get_known_errors",
            "get_samples",
            "search_tutorials",
            "search_learning_journeys",
        ),
        default_command="sap-devs",
        default_args=("mcp", "serve"),
    ),
    "sap_mcp_server": ProviderProfile(
        provider="sap_mcp_server",
        purpose="Read-only runtime access to SAP ABAP/BTP services through a compatible backend.",
        transport="stdio",
        observation_type="runtime_observation",
        default_read_tools=(),
    ),
    "abap_ai": ProviderProfile(
        provider="abap_ai",
        purpose="Organization-specific MCP servers hosted in ABAP.",
        transport="streamable_http",
        observation_type="custom_runtime_observation",
        default_read_tools=(),
    ),
}


def get_provider(provider: McpProvider) -> ProviderProfile:
    return PROVIDERS[provider]


def build_target(
    provider: McpProvider,
    *,
    command: str | None = None,
    args: tuple[str, ...] = (),
    url: str | None = None,
    allowed_tools: tuple[str, ...] | None = None,
    profile: str | None = None,
    metadata: dict[str, str] | None = None,
) -> McpTarget:
    definition = get_provider(provider)
    resolved_command = (
        definition.default_command if command is None else command
    )
    resolved_args = (
        definition.default_args if not args else args
    )
    target = McpTarget(
        provider=provider,
        transport=definition.transport,
        command=resolved_command,
        args=resolved_args,
        url=url,
        allowed_tools=(
            definition.default_read_tools
            if allowed_tools is None
            else allowed_tools
        ),
        profile=profile,
        read_only=True,
        observation_type=definition.observation_type,
        metadata=metadata or {},
    )
    target.validate()
    return target
