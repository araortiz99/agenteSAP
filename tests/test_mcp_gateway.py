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
