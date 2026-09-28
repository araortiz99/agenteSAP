import pytest

from src.sap.mcp_gateway import McpEvidenceGateway


def test_public_sap_gateway_is_disabled_by_default(monkeypatch):
    monkeypatch.delenv("AGENTESAP_SAP_PUBLIC_MCP_ENABLED", raising=False)
    assert McpEvidenceGateway.from_public_sap_env() is None


def test_public_sap_gateway_builds_official_readonly_target(monkeypatch):
    monkeypatch.setenv("AGENTESAP_SAP_PUBLIC_MCP_ENABLED", "true")
    monkeypatch.setenv("AGENTESAP_SAP_PUBLIC_MCP_READ_TOOLS", "search_tutorials,get_tutorial")
    gateway = McpEvidenceGateway.from_public_sap_env()

    assert gateway is not None
    assert gateway.target.provider == "sap_developer_public"
    assert gateway.target.transport == "streamable_http"
    assert gateway.target.url == "https://developers.sap.com/mcp/search"
    assert gateway.target.read_only is True
    assert gateway.target.observation_type == "external_source"


def test_public_sap_gateway_requires_query_tool_in_allowlist(monkeypatch):
    monkeypatch.setenv("AGENTESAP_SAP_PUBLIC_MCP_ENABLED", "true")
    monkeypatch.setenv("AGENTESAP_SAP_PUBLIC_MCP_READ_TOOLS", "get_tutorial")
    monkeypatch.setenv("AGENTESAP_SAP_PUBLIC_MCP_QUERY_TOOL", "search_tutorials")

    with pytest.raises(ValueError, match="explicitly allowlisted"):
        McpEvidenceGateway.from_public_sap_env()


def test_public_sap_read_preserves_external_observation(monkeypatch):
    monkeypatch.setenv("AGENTESAP_SAP_PUBLIC_MCP_ENABLED", "true")
    gateway = McpEvidenceGateway.from_public_sap_env()

    class FakeEvidence:
        provider = "sap_developer_public"
        observation_type = "external_source"

    async def fake_call(tool_name, arguments):
        assert tool_name == "search_tutorials"
        assert arguments == {"query": "material master"}
        return FakeEvidence()

    gateway._call_public_tool = fake_call
    evidence = gateway.read_public("search_tutorials", {"query": "material master"})
    assert evidence.observation_type == "external_source"


def test_public_sap_read_rejects_unallowlisted_tool(monkeypatch):
    monkeypatch.setenv("AGENTESAP_SAP_PUBLIC_MCP_ENABLED", "true")
    gateway = McpEvidenceGateway.from_public_sap_env()

    with pytest.raises(PermissionError, match="not allowlisted"):
        gateway.read_public("unknown_tool", {})


def test_request_router_prefers_public_sap_mcp_when_enabled(monkeypatch):
    monkeypatch.setenv("AGENTESAP_SAP_PUBLIC_MCP_ENABLED", "true")
    gateway = McpEvidenceGateway.for_request("¿Cómo funciona el material master en SAP?")
    assert gateway is not None
    assert gateway.target.provider == "sap_developer_public"
    assert gateway.target.observation_type == "external_source"
