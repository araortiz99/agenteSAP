"""Provider profiles for SAP MCP integrations."""

from __future__ import annotations
from dataclasses import dataclass
from src.sap.mcp_contracts import McpObservationType, McpProvider, McpTarget, McpTransport

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
        "sap_devs", "Current curated SAP developer knowledge and SAP resources.",
        "stdio", ("list_packs", "get_context", "search_resources", "get_known_errors",
                   "get_samples", "search_tutorials", "search_learning_journeys"),
        "developer_context", "sap-devs", ("mcp", "serve"),
    ),
    "sap_developer_public": ProviderProfile(
        "sap_developer_public",
        "Official public SAP Developer Center knowledge via hosted MCP.",
        "streamable_http",
        ("search_tutorials", "get_tutorial", "list_missions", "get_mission",
         "kg_shared_concepts", "kg_neighborhood", "kg_search_concepts", "kg_community"),
        "external_source",
    ),
    "sap_mcp_server": ProviderProfile(
        "sap_mcp_server",
        "Read-only runtime access to SAP ABAP/BTP services through a compatible backend.",
        "stdio", (), "runtime_observation",
    ),
    "abap_ai": ProviderProfile(
        "abap_ai", "Organization-specific MCP servers hosted in ABAP.",
        "streamable_http", (), "custom_runtime_observation",
    ),
}

def get_provider(provider: McpProvider) -> ProviderProfile:
    return PROVIDERS[provider]

def build_target(provider: McpProvider, *, command: str | None = None,
                 args: tuple[str, ...] = (), url: str | None = None,
                 allowed_tools: tuple[str, ...] | None = None, profile: str | None = None,
                 discovery_only: bool = False, metadata: dict[str, str] | None = None) -> McpTarget:
    definition = get_provider(provider)
    target = McpTarget(
        provider=provider,
        transport=definition.transport,
        command=definition.default_command if command is None else command,
        args=definition.default_args if not args else args,
        url=url,
        allowed_tools=definition.default_read_tools if allowed_tools is None else allowed_tools,
        profile=profile, read_only=True, discovery_only=discovery_only,
        observation_type=definition.observation_type, metadata=metadata or {},
    )
    target.validate()
    return target
