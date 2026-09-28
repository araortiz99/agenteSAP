from src.tools.entity_resolution import resolve_entities
from src.tools.knowledge_context import build_knowledge_context, render_knowledge_context


class FakeClient:
    def __init__(self):
        self.files = {
            "knowledge/sap-objects/zmm-imx-0004.md": """---
object_id: ZMM_IMX_0004
knowledge_type: custom
knowledge_scope: ticket
certainty: confirmed
---
# ZMM_IMX_0004
Solicitud de Nota de Crédito Logístico.
""",
            "knowledge/processes/snc-k1-xml-generation.md": """---
process_id: SNC-K1
knowledge_type: custom
knowledge_scope: process
certainty: confirmed
---
# SNC K1
Generación XML.
""",
            "knowledge/relationships/rel-object-process.md": """---
relationship_id: REL-1
source_id: ZMM_IMX_0004
source_type: SAP_OBJECT
relation_type: implements
target_id: SNC-K1
target_type: PROCESS
certainty: partial
status: candidate
evidence_source_id: SRC-TEST-001
---
# Relationship
ZMM_IMX_0004 implements SNC-K1.
""",
            "knowledge/business-rules/rule.md": """---
rule_id: RULE-1
knowledge_type: custom
knowledge_scope: process
certainty: partial
---
# Rule
No ajustar A001.
""",
            "knowledge/sap-standard/mm.md": """---
source_id: SAP-MM-GM
knowledge_type: standard
knowledge_scope: global
certainty: confirmed
---
# Goods Movement
SAP Standard inventory movement.
""",
        }

    def get_tree(self, ref="main"):
        return [{"path": path, "type": "blob"} for path in self.files]

    def get_file(self, path, ref="main"):
        return self.files[path]


def test_resolve_entities_returns_only_canonical_metadata_entities():
    result = resolve_entities(FakeClient(), "ZMM_IMX_0004")
    assert result
    assert result[0].entity_id == "ZMM_IMX_0004"
    assert result[0].entity_type == "SAP_OBJECT"
    assert result[0].certainty == "confirmed"
    assert all(item.entity_type != "RELATIONSHIP" for item in result)


def test_knowledge_context_traverses_explicit_relationships_only():
    context = build_knowledge_context(
        FakeClient(),
        "ZMM_IMX_0004",
        max_hops=2,
        max_entities=4,
        max_relationships=4,
        max_evidence=6,
    )
    assert context.entities
    assert any(
        item.relationship.target_id == "SNC-K1"
        and item.relationship.certainty == "partial"
        and item.relationship.status == "candidate"
        for item in context.relationships
    )
    assert any(
        item.result.path == "knowledge/processes/snc-k1-xml-generation.md"
        for item in context.evidence
    )


def test_knowledge_context_respects_hop_limit():
    context = build_knowledge_context(
        FakeClient(),
        "ZMM_IMX_0004",
        max_hops=0,
        max_entities=4,
        max_relationships=4,
        max_evidence=6,
    )
    assert context.relationships == ()
    assert any("max_hops=0" in gap for gap in context.gaps)


def test_render_preserves_provenance_and_hop():
    context = build_knowledge_context(FakeClient(), "ZMM_IMX_0004")
    rendered = render_knowledge_context(context)
    assert "source_layer:" in rendered
    assert "source_id:" in rendered
    assert "certainty:" in rendered
    assert "hop=" in rendered
    assert "### Conflicts" in rendered


def test_unknown_query_does_not_fabricate_entity():
    context = build_knowledge_context(FakeClient(), "ENTIDAD_INEXISTENTE_999")
    assert context.entities == ()
    assert any("No canonical repository entity" in gap for gap in context.gaps)


def test_related_entity_does_not_escalate_certainty():
    context = build_knowledge_context(FakeClient(), "ZMM_IMX_0004")
    related = [e for e in context.entities if e.entity_id == "SNC-K1"]
    assert related == [] or all(e.certainty != "confirmed" for e in related)


def test_relationship_limit_is_enforced():
    context = build_knowledge_context(
        FakeClient(), "ZMM_IMX_0004", max_relationships=1
    )
    assert len(context.relationships) <= 1


def test_second_hop_cannot_be_exceeded():
    context = build_knowledge_context(FakeClient(), "ZMM_IMX_0004", max_hops=1)
    assert all(item.hop <= 1 for item in context.relationships)
    assert all(item.hop <= 1 for item in context.evidence)


def test_knowledge_context_preserves_mcp_evidence():
    from src.tools.search_unified import UnifiedResult

    class FakeGateway:
        def search_resources(self, query):
            return (
                UnifiedResult(
                    path="mcp://sap_devs/search_resources",
                    score=0.9,
                    matched_terms=("SAP",),
                    content="MCP developer context",
                    source_layer="mcp",
                    match_type="mcp",
                    source_id="sap_devs:search_resources",
                    knowledge_type="developer_context",
                    knowledge_scope="external",
                    certainty="external_source",
                ),
            )

    context = build_knowledge_context(
        FakeClient(),
        "ZMM_IMX_0004",
        max_hops=0,
        max_evidence=6,
        mcp_gateway=FakeGateway(),
    )
    assert any(item.result.source_layer == "mcp" for item in context.evidence)
    assert any(item.result.path.startswith("mcp://") for item in context.evidence)



def test_knowledge_context_enforces_expansion_budget():
    context = build_knowledge_context(
        FakeClient(),
        "ZMM_IMX_0004",
        max_hops=3,
        max_expansions=1,
    )
    assert any("max_expansions=1" in gap for gap in context.gaps)


def test_knowledge_context_rejects_invalid_expansion_budget():
    try:
        build_knowledge_context(FakeClient(), "ZMM_IMX_0004", max_expansions=0)
    except ValueError as exc:
        assert "context limits" in str(exc)
    else:
        raise AssertionError("expected ValueError")
