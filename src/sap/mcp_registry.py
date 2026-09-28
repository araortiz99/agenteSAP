"""Provider profiles for SAP MCP integrations.

Profiles describe how AgenteSAP may connect; they never contain credentials.
Live credentials remain in the provider/client environment.
"""

from __future__ import annotations

from dataclasses import dataclass

from src.sap.mcp_contracts import McpProvider, McpTarget


@dataclass(frozen=True)
class ProviderProfile:
    provider: McpProvider
    purpose: str
    transport: str
    default_read_tools: tuple[str, ...]


PROVIDERS: dict[McpProvider, ProviderProfile] = {
    "sap_devs": ProviderProfile(
        provider="sap_devs",
        purpose="Current curated SAP developer knowledge and SAP resources.",
        transport="stdio",
        default_read_tools=(
            "list_packs",
            "get_context",
            "search_resources",
            "get_known_errors",
            "get_samples",
            "search_tutorials",
            "search_learning_journeys",
        ),
    ),
    "sap_mcp_server": ProviderProfile(
        provider="sap_mcp_server",
        purpose="Read-only runtime access to SAP ABAP/BTP services through a compatible backend.",
        transport="stdio",
        default_read_tools=(),
    ),
    "abap_ai": ProviderProfile(
        provider="abap_ai",
        purpose="Organization-specific MCP servers hosted in ABAP.",
        transport="streamable_http",
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
    target = McpTarget(
        provider=provider,
        transport=definition.transport,  # type: ignore[arg-type]
        command=command,
        args=args,
        url=url,
        allowed_tools=allowed_tools or definition.default_read_tools,
        profile=profile,
        read_only=True,
        metadata=metadata or {},
    )
    target.validate()
    return target
