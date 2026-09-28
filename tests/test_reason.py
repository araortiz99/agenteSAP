from src.tools.evidence import assess_evidence
from src.tools.reason import reason_from_evidence
from src.tools.search_unified import UnifiedResult, UnifiedSearchResult


def result(layer, certainty, source_id, knowledge_type):
    return UnifiedResult(
        path=f"{source_id}.md",
        score=1.0,
        matched_terms=("x",),
        content="x",
        source_layer=layer,
        match_type="content",
        source_id=source_id,
        knowledge_type=knowledge_type,
        knowledge_scope="global",
        certainty=certainty,
    )


def test_reason_requires_analysis_for_two_layers():
    a = result("sap_standard", "confirmed", "SAP-1", "standard")
    b = result("internal", "confirmed", "INT-1", "custom")
    assessment = assess_evidence(
        UnifiedSearchResult("x", (a, b), (a,), (b,))
    )
    reasoning = reason_from_evidence(assessment)
    assert reasoning.conclusion_status == "requires_analysis"


def test_reason_blocks_conflicting_metadata():
    a = result("internal", "confirmed", "SAME", "custom")
    b = result("internal", "confirmed", "SAME", "standard")
    assessment = assess_evidence(
        UnifiedSearchResult("x", (a, b), (), (a, b))
    )
    reasoning = reason_from_evidence(assessment)
    assert reasoning.conclusion_status == "conflict"
    assert reasoning.conflicts == assessment.conflicts
    assert reasoning.conflicts[0].conflict_type == "metadata_conflict"
