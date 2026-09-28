from pathlib import Path

from src.agent.consultant import ConsultationResult, build_context, consult
from src.tools.search_unified import UnifiedResult, UnifiedSearchResult


class FakeClient:
    def __init__(self):
        self.files = {
            "knowledge/sap-standard/mm/material-master.md":
                """---
knowledge_type: standard
knowledge_scope: global
source_id: SAP-MM-MATERIAL
certainty: confirmed
---
# Material Master
SAP standard material master information.""",
            "knowledge/custom/material.md":
                """---
knowledge_type: custom
knowledge_scope: process
source_id: INT-MATERIAL
certainty: partial
---
# Local Material
Internal process for material master.""",
        }

    def get_tree(self, ref="main"):
        return [{"path": p, "type": "blob"} for p in self.files]

    def get_file(self, path, ref="main"):
        return self.files[path]


class FakeLLM:
    model = "fake-model"

    def __init__(self):
        self.system_prompt = ""
        self.user_prompt = ""

    def generate(self, *, system_prompt, user_prompt):
        self.system_prompt = system_prompt
        self.user_prompt = user_prompt
        import re
        evidence_id = re.search(r"(EVD-[A-Z0-9]+)", user_prompt).group(1)
        return (
            "## Resumen\n"
            "Respuesta basada en [" + evidence_id + "].\n\n"
            "## Qué está confirmado\n"
            "Información confirmada [" + evidence_id + "].\n\n"
            "## Qué corresponde a nuestra implementación\n"
            "La evidencia interna correspondiente [" + evidence_id + "].\n\n"
            "## Qué no está confirmado\n"
            "No hay información adicional confirmada.\n\n"
            "## Evidencias\n"
            "[" + evidence_id + "]\n\n"
            "## Ticket\n"
            "No se suministró contexto de ticket.\n\n"
            "## Próximos pasos\n"
            "Validar la información pendiente según la evidencia."
        )


def test_consult_builds_traceable_context_and_calls_llm():
    llm = FakeLLM()
    result = consult(FakeClient(), "Consultá sobre material master", llm)

    assert isinstance(result, ConsultationResult)
    assert result.answer.startswith("Respuesta basada en [EVD-")
    assert result.traceability.evidence
    assert "certainty:" in llm.user_prompt
    assert "source_layer:" in llm.user_prompt
    assert "EVD-" in llm.user_prompt
    assert "SAP-MM-MATERIAL" in llm.user_prompt
    assert result.citations
    assert result.citations[0].evidence_id in {item.evidence_id for item in result.traceability.evidence}
    assert result.uncited_evidence_ids


def test_build_context_contains_gaps_and_conflicts():
    evidence = UnifiedResult(
        path="x.md",
        score=1.0,
        matched_terms=("x",),
        content="x",
        source_layer="internal",
        match_type="content",
        source_id="INT-1",
        knowledge_type="custom",
        knowledge_scope="ticket",
        certainty="partial",
    )
    retrieval = UnifiedSearchResult("x", (evidence,), (), (evidence,))
    from src.tools.evidence import assess_evidence
    from src.tools.reason import reason_from_evidence
    from src.tools.evidence_trace import build_traceability

    trace = build_traceability(reason_from_evidence(assess_evidence(retrieval)))
    context = build_context(retrieval, trace)

    assert "Gaps" in context
    assert "Conflicts" in context


class InvalidStructureLLM(FakeLLM):
    def generate(self, *, system_prompt, user_prompt):
        return "Respuesta sin estructura requerida."

class HallucinatingLLM(FakeLLM):
    def generate(self, *, system_prompt, user_prompt):
        return "Respuesta con [EVD-NOEXISTE]."


def test_consult_rejects_invalid_answer_structure():
    import pytest

    from src.agent.consultant import ConsultationFormatError

    with pytest.raises(ConsultationFormatError, match="missing required section"):
        consult(FakeClient(), "Consultá sobre material master", InvalidStructureLLM())

def test_consult_rejects_unknown_evidence_citation():
    import pytest

    with pytest.raises(ValueError, match="unknown evidence id"):
        consult(FakeClient(), "Consultá sobre material master", HallucinatingLLM())


class TicketFakeClient(FakeClient):
    def __init__(self):
        super().__init__()
        self.files.update({
            "tickets/31426/ticket.md": """---
ticket_id: "31426"
title: "Error de XML SNC K1"
---
# Ticket
ZMM_IMX_0004
EKPO-LOEKZ
""",
            "knowledge/relationships/rel-31426-zmm-imx-0004.md": """---
relationship_id: "REL-31426-001"
source_id: "31426"
source_type: "TICKET"
relation_type: "relacionado_con"
target_id: "ZMM_IMX_0004"
target_type: "SAP_OBJECT"
---
# Relationship
""",
        })

    def get_tree(self, ref="main"):
        return [{"path": p, "type": "blob"} for p in self.files]


def test_consult_includes_ticket_context_and_relationships():
    llm = FakeLLM()
    result = consult(
        TicketFakeClient(),
        "Consultá el ticket 31426 y explicame qué está confirmado",
        llm,
        ticket_id="31426",
    )

    assert result.ticket_context
    assert result.ticket_context[0].ticket_id == "31426"
    assert result.ticket_context[0].reference_id.startswith("TKT-")
    assert result.ticket_relationships is not None
    assert result.ticket_relationships.relationships
    assert "Ticket context" in llm.user_prompt
    assert "31426" in llm.user_prompt


def test_consult_ticket_context_does_not_replace_evidence():
    llm = FakeLLM()
    result = consult(
        TicketFakeClient(),
        "Consultá el ticket 31426",
        llm,
        ticket_id="31426",
    )

    assert result.traceability.evidence
    assert result.citations
