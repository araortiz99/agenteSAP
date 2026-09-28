from src.tools.evidence import assess_evidence
from src.tools.search_unified import UnifiedResult, UnifiedSearchResult


def _result(
    path: str,
    layer: str,
    certainty: str,
    source_id: str,
    knowledge_type: str,
) -> UnifiedResult:
    return UnifiedResult(
        path=path,
        score=1.0,
        matched_terms=("material",),
        content="content",
        source_layer=layer,
        match_type="content",
        source_id=source_id,
        knowledge_type=knowledge_type,
        knowledge_scope="global",
        certainty=certainty,
    )


def test_evidence_keeps_standard_and_internal_separate():
    retrieval = UnifiedSearchResult(
        query="material",
        results=(
            _result("sap.md", "sap_standard", "confirmed", "SAP-1", "standard"),
            _result("internal.md", "internal", "confirmed", "INT-1", "custom"),
        ),
        sap_standard=(
            _result("sap.md", "sap_standard", "confirmed", "SAP-1", "standard"),
        ),
        internal=(
            _result("internal.md", "internal", "confirmed", "INT-1", "custom"),
        ),
    )
    assessment = assess_evidence(retrieval)
    assert len(assessment.confirmed) == 2
    assert assessment.requires_analysis is True
    assert not assessment.conflicts


def test_evidence_marks_missing_layers():
    retrieval = UnifiedSearchResult(
        query="material",
        results=(
            _result("internal.md", "internal", "partial", "INT-1", "custom"),
        ),
        sap_standard=(),
        internal=(
            _result("internal.md", "internal", "partial", "INT-1", "custom"),
        ),
    )
    assessment = assess_evidence(retrieval)
    assert "No SAP Standard evidence was retrieved." in assessment.gaps
    assert not assessment.confirmed
    assert assessment.partial


def test_evidence_detects_metadata_conflict():
    a = _result("a.md", "internal", "confirmed", "SAME", "custom")
    b = _result("b.md", "internal", "confirmed", "SAME", "standard")
    retrieval = UnifiedSearchResult(
        query="x",
        results=(a, b),
        sap_standard=(),
        internal=(a, b),
    )
    assessment = assess_evidence(retrieval)
    assert assessment.conflicts
    assert assessment.requires_analysis is False
