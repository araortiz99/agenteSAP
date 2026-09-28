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
