from src.agent.consultant import ConsultationResult, consult
from src.tools.evidence import assess_evidence
from src.tools.search_unified import UnifiedResult, UnifiedSearchResult


class FinalGateClient:
    def __init__(self):
        self.files = {
            "knowledge/sap-standard/mm/material.md": """---
source_id: SAP-MM-MATERIAL
knowledge_type: standard
knowledge_scope: global
certainty: confirmed
---
SAP Standard: el maestro de materiales contiene datos de material.
""",
            "knowledge/internal/inventory-rule.md": """---
source_id: INT-MP-RULE
knowledge_type: business_rule
knowledge_scope: organization
certainty: confirmed
authority: authoritative
version: 1.0
origin: business_document
---
La implementación empresarial define el universo de Inventario Materia Prima.
""",
            "knowledge/internal/inventory-rule-old.md": """---
source_id: INT-MP-RULE-OLD
knowledge_type: business_rule
knowledge_scope: organization
certainty: confirmed
authority: superseded
version: 0.9
origin: business_document
---
Regla histórica reemplazada.
""",
        }

    def get_tree(self, ref="main"):
        return [{"path": p, "type": "blob"} for p in self.files]

    def get_file(self, path, ref="main"):
        return self.files[path]


class FinalGateLLM:
    model = "fake-final-gate"

    def generate(self, *, system_prompt, user_prompt):
        import re
        ids = list(dict.fromkeys(re.findall(r"EVD-[A-Z0-9]+", user_prompt)))
        cites = " ".join(f"[{x}]" for x in ids[:3])
        return (
            "## Resumen\nLa consulta se responde con evidencia separada. " + cites + "\n\n"
            "## Qué está confirmado\nExiste evidencia SAP Standard y una regla empresarial vigente. " + cites + "\n\n"
            "## Qué corresponde a nuestra implementación\nLa regla interna vigente corresponde a la implementación empresarial. " + cites + "\n\n"
            "## Qué no está confirmado\nNo se dispone de observación runtime de QAS.\n\n"
            "## Evidencias\n" + cites + "\n\n"
            "## Ticket\nNo se suministró ticket.\n\n"
            "## Próximos pasos\nValidar en QAS si se requiere conocer el estado actual."
        )


def test_final_gate_consultant_preserves_authority_and_read_only_boundary():
    result = consult(
        FinalGateClient(),
        "¿Qué establece SAP y qué corresponde a nuestra implementación de Inventario Materia Prima?",
        FinalGateLLM(),
    )

    assert isinstance(result, ConsultationResult)
    assert result.answer.startswith("## Resumen")
    internal = {item.source_id: item for item in result.retrieval.internal}
    assert internal["INT-MP-RULE"].authority == "authoritative"
    assert internal["INT-MP-RULE-OLD"].authority == "superseded"
    assert any(
        item.source_id == "INT-MP-RULE" and item.authority == "authoritative"
        for item in result.evidence.items
    )
    assert all(
        item.source_id != "INT-MP-RULE-OLD" or not item.supports
        for item in result.evidence.items
    )
    assert result.citations
    assert result.investigation is not None


def test_final_gate_does_not_invent_runtime_observation():
    retrieval = UnifiedSearchResult(
        query="estado actual QAS",
        results=(
            UnifiedResult(
                path="knowledge/internal/rule.md",
                score=1.0,
                matched_terms=("QAS",),
                content="Regla documental.",
                source_layer="internal",
                match_type="content",
                source_id="INT-1",
                knowledge_type="business_rule",
                knowledge_scope="organization",
                certainty="confirmed",
                authority="authoritative",
            ),
        ),
        sap_standard=(),
        internal=(),
        mcp=(),
    )
    assessment = assess_evidence(retrieval)
    assert any("runtime" in gap.lower() for gap in assessment.gaps)
