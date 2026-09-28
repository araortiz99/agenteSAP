from src.tools.evidence import assess_evidence
from src.tools.evidence_trace import build_traceability, render_traceability
from src.tools.reason import reason_from_evidence
from src.tools.search_unified import UnifiedResult, UnifiedSearchResult


def result(layer, certainty, source_id, knowledge_type, path):
    return UnifiedResult(
        path=path,
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


def test_trace_ids_are_stable_and_source_derived():
    a = result("sap_standard", "confirmed", "SAP-1", "standard", "sap.md")
    retrieval = UnifiedSearchResult("x", (a,), (a,), ())
    reasoning = reason_from_evidence(assess_evidence(retrieval))

    first = build_traceability(reasoning)
    second = build_traceability(reasoning)

    assert first.trace_id == second.trace_id
    assert first.evidence[0].evidence_id == second.evidence[0].evidence_id
    assert first.supporting_evidence_ids == (first.evidence[0].evidence_id,)


def test_trace_marks_partial_as_unresolved():
    a = result("internal", "partial", "INT-1", "custom", "internal.md")
    retrieval = UnifiedSearchResult("x", (a,), (), (a,))
    report = build_traceability(reason_from_evidence(assess_evidence(retrieval)))

    assert report.unresolved_evidence_ids == (report.evidence[0].evidence_id,)
    assert report.evidence[0].role == "unresolved"


def test_trace_render_contains_provenance():
    a = result("sap_standard", "confirmed", "SAP-1", "standard", "sap.md")
    retrieval = UnifiedSearchResult("x", (a,), (a,), ())
    report = build_traceability(reason_from_evidence(assess_evidence(retrieval)))
    rendered = render_traceability(report)

    assert report.evidence[0].evidence_id in rendered
    assert "SAP-1" in rendered
    assert "sap_standard" in rendered
