from src.tools.evidence import assess_evidence
from src.tools.search_unified import UnifiedResult, UnifiedSearchResult


def _result(
    path: str,
    layer: str,
    certainty: str,
    source_id: str,
    knowledge_type: str,
    content: str = "content",
) -> UnifiedResult:
    return UnifiedResult(
        path=path,
        score=1.0,
        matched_terms=("material",),
        content=content,
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
    assert assessment.conflicts[0].conflict_type == "metadata_conflict"
    assert assessment.conflicts[0].status == "requires_analysis"
    assert assessment.requires_analysis is True


def test_evidence_detects_explicit_documented_conflict():
    content = """# Relationship

## 7. Conflictos
Existe material posterior que utiliza 31426 para un escenario K4.

## 8. Información pendiente
Validar contra el registro original.
"""
    item = _result(
        "rel-31426-snc-k1.md",
        "internal",
        "partial",
        "SRC-31426-KB-20260918",
        "custom",
        content,
    )
    retrieval = UnifiedSearchResult(
        query="ticket 31426 K1",
        results=(item,),
        sap_standard=(),
        internal=(item,),
    )

    assessment = assess_evidence(retrieval)

    assert len(assessment.conflicts) == 1
    conflict = assessment.conflicts[0]
    assert conflict.conflict_type == "explicit_documented_conflict"
    assert conflict.status == "requires_analysis"
    assert "K4" in conflict.description
    assert conflict.evidence_paths == ("rel-31426-snc-k1.md",)
    assert assessment.requires_analysis is True


def test_evidence_does_not_infer_conflict_from_cooccurrence():
    content = """# Relationship

## 4. Descripción
El proceso puede considerar escenarios K1 y K4 según el circuito.

## 5. Evidencia
Fuente interna.
"""
    item = _result(
        "process.md",
        "internal",
        "confirmed",
        "SRC-1",
        "custom",
        content,
    )
    retrieval = UnifiedSearchResult(
        query="K1 K4",
        results=(item,),
        sap_standard=(),
        internal=(item,),
    )

    assessment = assess_evidence(retrieval)

    assert not assessment.conflicts
    assert assessment.requires_analysis is False
