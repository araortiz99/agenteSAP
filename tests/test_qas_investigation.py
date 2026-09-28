from src.agent.investigation import investigate
from src.sap.mcp_contracts import SapMcpEvidence
from src.sap.mcp_gateway import McpEvidenceGateway
from src.tools.search_unified import UnifiedResult


class FixtureClient:
    def __init__(self):
        self.files = {
            "knowledge/sap-standard/mm/runtime-case.md": """---
source_id: SAP-MM-RUNTIME-CASE
knowledge_type: standard
knowledge_scope: global
certainty: confirmed
---
# SAP Standard
MARA and movement type semantics are standard SAP knowledge.
""",
            "knowledge/internal/runtime-case.md": """---
source_id: INT-MM-RUNTIME-CASE
knowledge_type: custom
knowledge_scope: organization
certainty: confirmed
---
# Internal
The customer has a custom inventory process involving MARA.
""",
        }

    def get_tree(self, ref="main"):
        return [{"path": p, "type": "blob"} for p in self.files]

    def get_file(self, path, ref="main"):
        return self.files[path]


class FakeQasGateway:
    def supports_source(self, source):
        return source == "runtime"

    def search_resources(self, query):
        return (
            UnifiedResult(
                path="mcp://sap_mcp_server/read_table",
                score=1.0,
                matched_terms=tuple(query.split()),
                content='{"system":"S4QAS","landscape":"QAS","object":"MARA","rows":[]}',
                source_layer="mcp",
                match_type="mcp",
                source_id="MARA",
                knowledge_type="runtime_observation",
                knowledge_scope="runtime",
                certainty="partial",
                provenance=(
                    ("provider", "sap_mcp_server"),
                    ("operation", "read_table"),
                    ("system", "S4QAS"),
                    ("landscape", "QAS"),
                    ("observation_type", "runtime_observation"),
                ),
            ),
        )


def test_runtime_investigation_keeps_runtime_separate_from_standard_and_internal(monkeypatch):
    monkeypatch.setattr(
        "src.agent.investigation.McpEvidenceGateway.from_qas_runtime_env",
        lambda: FakeQasGateway(),
    )

    result = investigate(
        FixtureClient(),
        "¿Cuál es el estado actual de MARA en QAS?",
        max_results=8,
    )

    assert any(item.knowledge_type == "runtime_observation" for item in result.retrieval.mcp)
    assert all(item.knowledge_scope == "runtime" for item in result.retrieval.mcp)
    assert any(item.source_layer == "sap_standard" for item in result.retrieval.results)
    assert any(item.source_layer == "internal" for item in result.retrieval.results)
    assert result.reasoning.query == "¿Cuál es el estado actual de MARA en QAS?"


def test_qas_gateway_executes_only_explicit_runtime_query_tool(monkeypatch):
    monkeypatch.setenv("AGENTESAP_SAP_RUNTIME_ENABLED", "true")
    monkeypatch.setenv("AGENTESAP_SAP_RUNTIME_LANDSCAPE", "QAS")
    monkeypatch.setenv("AGENTESAP_SAP_RUNTIME_SCOPE", "mcp_readonly")
    monkeypatch.setenv("AGENTESAP_SAP_RUNTIME_READ_TOOLS", "read_query")
    monkeypatch.setenv("AGENTESAP_SAP_RUNTIME_QUERY_TOOL", "read_query")
    monkeypatch.setenv("AGENTESAP_SAP_MCP_COMMAND", "fake-qas")
    monkeypatch.setenv("AGENTESAP_SAP_MCP_ARGS", "serve")

    gateway = McpEvidenceGateway.from_qas_runtime_env()
    assert gateway is not None
    assert gateway.target.metadata["landscape"] == "QAS"
    assert gateway.target.metadata["query_tool"] == "read_query"
    assert gateway.target.allowed_tools == ("read_query",)
    assert gateway.target.read_only is True


def test_qas_gateway_rejects_query_tool_outside_allowlist(monkeypatch):
    monkeypatch.setenv("AGENTESAP_SAP_RUNTIME_ENABLED", "true")
    monkeypatch.setenv("AGENTESAP_SAP_RUNTIME_LANDSCAPE", "QAS")
    monkeypatch.setenv("AGENTESAP_SAP_RUNTIME_SCOPE", "mcp_readonly")
    monkeypatch.setenv("AGENTESAP_SAP_RUNTIME_READ_TOOLS", "other_read")
    monkeypatch.setenv("AGENTESAP_SAP_RUNTIME_QUERY_TOOL", "read_query")

    try:
        McpEvidenceGateway.from_qas_runtime_env()
    except ValueError as exc:
        assert "explicitly allowlisted" in str(exc)
    else:
        raise AssertionError("runtime query tool must be allowlisted")
