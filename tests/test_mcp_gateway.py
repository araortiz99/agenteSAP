import pytest

from src.sap.mcp_gateway import McpEvidenceGateway, McpGatewayConfig
from src.tools.search_unified import UnifiedResult, search_unified


class FakeClient:
    def get_tree(self, ref="main"):
        return []

    def get_file(self, path, ref="main"):
        raise KeyError(path)


class FakeGateway:
    def search_resources(self, query):
        return (
            UnifiedResult(
                path="mcp://sap_devs/search_resources",
                score=0.9,
                matched_terms=("MM",),
                content='{"count": 1, "results": [{"title": "MM"}]}',
                source_layer="mcp",
                match_type="mcp",
                source_id="sap_devs:search_resources",
                knowledge_type="developer_context",
                knowledge_scope="external",
                certainty="external_source",
            ),
        )


def test_gateway_is_read_only_and_targets_sap_devs():
    gateway = McpEvidenceGateway(McpGatewayConfig())
    assert gateway.target.provider == "sap_devs"
    assert gateway.target.read_only is True
    assert gateway.target.observation_type == "developer_context"
    assert "search_resources" in gateway.target.allowed_tools


def test_unified_search_preserves_mcp_layer():
    result = search_unified(
        FakeClient(),
        "material master",
        mcp_gateway=FakeGateway(),
    )
    assert result.mcp
    assert result.mcp[0].source_layer == "mcp"
    assert result.results[0].source_layer == "mcp"


def test_gateway_ignores_zero_result_mcp_response(monkeypatch):
    gateway = McpEvidenceGateway(McpGatewayConfig())

    class FakeEvidence:
        provider = "sap_devs"
        operation = "search_resources"
        content = ['{"count": 0, "total": 0, "results": []}']
        certainty = "external_source"

    async def fake_search(query):
        return FakeEvidence()

    monkeypatch.setattr(gateway, "_search_resources", fake_search)
    assert gateway.search_resources("does-not-exist") == ()


def test_mcp_evidence_has_explicit_external_priority():
    from src.tools.evidence import assess_evidence

    gateway_result = UnifiedResult(
        path="mcp://sap_devs/search_resources",
        score=0.9,
        matched_terms=("ABAP",),
        content="MCP developer context",
        source_layer="mcp",
        match_type="mcp",
        source_id="sap_devs:search_resources",
        knowledge_type="developer_context",
        knowledge_scope="external",
        certainty="external_source",
    )
    assessment = assess_evidence(
        search_unified(
            FakeClient(),
            "ABAP",
            mcp_gateway=type(
                "Gateway",
                (),
                {"search_resources": lambda self, query: (gateway_result,)},
            )(),
        )
    )
    assert assessment.items[0].weight == 2 * 0.4
    assert assessment.items[0].supports is False
    assert assessment.items[0].certainty == "external_source"


def test_gateway_search_resources_works_inside_active_event_loop(monkeypatch):
    gateway = McpEvidenceGateway(McpGatewayConfig())

    class FakeEvidence:
        provider = "sap_devs"
        operation = "search_resources"
        content = ['{"count": 1, "results": [{"title": "ABAP"}]}']
        certainty = "external_source"

    async def fake_search(query):
        return FakeEvidence()

    monkeypatch.setattr(gateway, "_search_resources", fake_search)

    async def invoke():
        return gateway.search_resources("ABAP")

    import asyncio

    result = asyncio.run(invoke())
    assert result
    assert result[0].source_layer == "mcp"


def test_gateway_from_env_parses_quoted_args(monkeypatch):
    monkeypatch.setenv("AGENTESAP_MCP_ENABLED", "true")
    monkeypatch.setenv("AGENTESAP_MCP_COMMAND", "sap-devs")
    monkeypatch.setenv("AGENTESAP_MCP_ARGS", 'mcp serve --profile "developer context"')

    gateway = McpEvidenceGateway.from_env()

    assert gateway is not None
    assert gateway.config.args == ("mcp", "serve", "--profile", "developer context")


def test_gateway_maps_runtime_observation_metadata(monkeypatch):
    from src.sap.mcp_contracts import SapMcpEvidence
    from src.sap.mcp_gateway import McpEvidenceGateway

    gateway = McpEvidenceGateway(McpGatewayConfig())

    async def fake_search(query):
        return SapMcpEvidence(
            provider="sap_mcp_server",
            operation="read_table",
            content=['{"rows": 1}'],
            source="runtime",
            system="S4QAS",
            landscape="QAS",
            object_id="MARA",
            certainty="partial",
            observation_type="runtime_observation",
        )

    monkeypatch.setattr(gateway, "_search_resources", fake_search)
    results = gateway.search_resources("MARA")

    assert results[0].knowledge_type == "runtime_observation"
    assert results[0].knowledge_scope == "runtime"
    assert results[0].source_id == "MARA"
    assert results[0].certainty == "partial"
    assert dict(results[0].provenance) == {
        "provider": "sap_mcp_server",
        "operation": "read_table",
        "system": "S4QAS",
        "landscape": "QAS",
        "object_id": "MARA",
        "observation_type": "runtime_observation",
    }


def test_gateway_capability_does_not_advertise_runtime_for_sap_devs():
    gateway = McpEvidenceGateway(McpGatewayConfig())
    assert gateway.supports_source("external") is True
    assert gateway.supports_source("runtime") is False
    assert gateway.provider_plan("runtime").ready is False
    assert gateway.provider_plan("external").ready is True


def test_runtime_tool_inspection_is_allowlist_bound(monkeypatch):
    monkeypatch.setenv("AGENTESAP_SAP_RUNTIME_ENABLED", "true")
    monkeypatch.setenv("AGENTESAP_SAP_RUNTIME_ENABLED", "true")
    monkeypatch.setenv("AGENTESAP_SAP_RUNTIME_LANDSCAPE", "QAS")
    monkeypatch.setenv("AGENTESAP_SAP_RUNTIME_SCOPE", "mcp_readonly")
    monkeypatch.setenv(
        "AGENTESAP_SAP_RUNTIME_READ_TOOLS",
        "verified_table_read",
    )

    gateway = McpEvidenceGateway.from_qas_runtime_env()
    assert gateway is not None

    async def fake_inspect():
        return (
            {"name": "verified_table_read", "description": "read"},
            {"name": "unlisted_tool", "description": "other"},
        )

    gateway._inspect_runtime_tools = fake_inspect
    catalog = gateway.inspect_runtime_tools()

    assert [item["name"] for item in catalog] == ["verified_table_read"]


def test_qas_catalog_inspection_is_readonly_and_not_allowlisted_for_calls(monkeypatch):
    monkeypatch.setenv("AGENTESAP_SAP_RUNTIME_ENABLED", "true")
    monkeypatch.setenv("AGENTESAP_SAP_RUNTIME_LANDSCAPE", "QAS")
    monkeypatch.setenv("AGENTESAP_SAP_RUNTIME_SCOPE", "mcp_readonly")
    monkeypatch.delenv("AGENTESAP_SAP_RUNTIME_READ_TOOLS", raising=False)

    gateway = McpEvidenceGateway.for_qas_catalog_inspection()

    assert gateway.target.allowed_tools == ("__catalog_only__",)
    assert gateway.target.read_only is True

    async def fake_inspect():
        return (
            {"name": "table_read", "description": "read table"},
            {"name": "write_tool", "description": "write"},
        )

    gateway._inspect_runtime_tools = fake_inspect
    catalog = gateway.inspect_runtime_tools()

    assert [item["name"] for item in catalog] == ["table_read", "write_tool"]

    try:
        gateway.read_runtime("table_read", {})
    except PermissionError as exc:
        assert "not allowlisted" in str(exc)
    else:
        raise AssertionError("catalog-only mode must not allow SAP tool calls")


def test_qas_catalog_inspection_requires_explicit_enablement(monkeypatch):
    monkeypatch.delenv("AGENTESAP_SAP_RUNTIME_ENABLED", raising=False)
    with pytest.raises(PermissionError, match="disabled"):
        McpEvidenceGateway.for_qas_catalog_inspection()


def test_runtime_tool_catalog_rejects_non_qas():
    gateway = McpEvidenceGateway.__new__(McpEvidenceGateway)
    gateway.target = type(
        "Target",
        (),
        {
            "provider": "sap_mcp_server",
            "metadata": {"landscape": "PRD"},
        },
    )()

    with pytest.raises(PermissionError, match="restricted to QAS"):
        gateway.runtime_tool_catalog()
