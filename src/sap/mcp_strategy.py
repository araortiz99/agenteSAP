"""Deterministic provider strategy for MCP evidence retrieval.

The strategy decides which MCP provider is eligible for an evidence layer.
It does not connect, execute tools, or promote evidence. Runtime providers
remain unavailable until an explicit read-only tool contract is configured.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from src.sap.mcp_contracts import McpProvider
from src.sap.mcp_registry import get_provider


McpEvidenceLayer = Literal["runtime", "external"]


@dataclass(frozen=True)
class McpProviderPlan:
    """Provider decision for one MCP evidence layer."""

    layer: McpEvidenceLayer
    provider: McpProvider | None
    ready: bool
    reason: str


_RUNTIME_PROVIDERS: tuple[McpProvider, ...] = (
    "sap_mcp_server",
    "abap_ai",
)


def plan_mcp_provider(
    layer: McpEvidenceLayer,
    *,
    configured_provider: McpProvider | None = None,
) -> McpProviderPlan:
    """Resolve an MCP provider without treating the plan as evidence.

    Runtime access is fail-closed: a runtime provider may be identified as the
    intended target, but it is not considered ready until its explicit
    read-only tool contract is configured. Developer context is intentionally
    not eligible for runtime evidence.
    """
    if layer == "external":
        provider = configured_provider or "sap_devs"
        profile = get_provider(provider)
        if profile.observation_type not in {"developer_context", "external_source"}:
            raise ValueError(
                f"Provider '{provider}' is not valid for external/developer context"
            )
        return McpProviderPlan(
            layer=layer,
            provider=provider,
            ready=True,
            reason="developer/external MCP context may be used as supplemental evidence",
        )

    provider = configured_provider or "sap_mcp_server"
    if provider not in _RUNTIME_PROVIDERS:
        raise ValueError(
            f"Provider '{provider}' is not approved for runtime evidence"
        )

    profile = get_provider(provider)
    return McpProviderPlan(
        layer=layer,
        provider=provider,
        ready=False,
        reason=(
            f"Runtime provider '{provider}' is registered but has no explicit "
            "read-only tool contract configured in AgenteSAP"
        ),
    )
