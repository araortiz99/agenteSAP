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
