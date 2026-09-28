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
        return f"Respuesta basada en [{evidence_id}]."


def test_consult_builds_traceable_context_and_calls_llm():
    llm = FakeLLM()
    result = consult(FakeClient(), "Consultá sobre material master", llm)

    assert isinstance(result, ConsultationResult)
    assert result.answer == "Respuesta basada en [EVD-TEST]."
    assert result.traceability.evidence
    assert "certainty:" in llm.user_prompt
    assert "source_layer:" in llm.user_prompt
    assert "EVD-" in llm.user_prompt
    assert "SAP-MM-MATERIAL" in llm.user_prompt
    assert result.citations
    assert result.citations[0].evidence_id == result.traceability.evidence[0].evidence_id
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


class HallucinatingLLM(FakeLLM):
    def generate(self, *, system_prompt, user_prompt):
        return "Respuesta con [EVD-NOEXISTE]."


def test_consult_rejects_unknown_evidence_citation():
    import pytest

    with pytest.raises(ValueError, match="unknown evidence id"):
        consult(FakeClient(), "Consultá sobre material master", HallucinatingLLM())
