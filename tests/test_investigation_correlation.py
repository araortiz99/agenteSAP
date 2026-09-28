from src.investigation.contracts import InvestigationEvidence
from src.investigation.correlation import correlate_evidence


def evidence(evidence_id: str, content: str, observation_type: str, object_id: str = "100123") -> InvestigationEvidence:
    return InvestigationEvidence(
        evidence_id=evidence_id,
        provider="fixture",
        operation="read",
        landscape="QAS",
        system="QAS",
        object_type="SAP_RUNTIME",
        object_id=object_id,
        observation_type=observation_type,
        content=content,
        certainty="high",
        provenance=(("fixture", evidence_id),),
    )


def test_basic_evidence_is_related_and_preserves_provenance():
    result = correlate_evidence([
        evidence("EV-001", '{"material":"100123","plant":"5023","stock":125}', "stock"),
        evidence("EV-002", '{"material":"100123","plant":"5023","description":"Material"}', "master"),
    ])
    assert ("EV-001", "EV-002") not in result.contradictions
    assert any(item.relation == "related_to" for item in result.relations)
    assert result.evidence_ids == ("EV-001", "EV-002")


def test_movement_and_stock_are_correlated_without_claiming_causality():
    result = correlate_evidence([
        evidence("EV-001", '{"material":"100123","plant":"5023","stock":125}', "stock"),
        evidence("EV-002", '{"material":"100123","plant":"5023","movement_quantity":10}', "movement"),
    ])
    relation = next(item for item in result.relations if item.relation == "explains")
    assert relation.certainty == "medium"
    assert "movimiento" in relation.reason.lower()
    assert "causa" not in relation.reason.lower()


def test_missing_structured_fields_create_gap_without_invention():
    result = correlate_evidence([
        evidence("EV-001", "stock observed for material 100123 at plant 5023", "stock"),
        evidence("EV-002", "movement observed", "movement"),
    ])
    assert "structured_fields_missing_for_correlation" in result.gaps
    assert result.unresolved_relationships


def test_conflicting_stock_values_are_explicit():
    result = correlate_evidence([
        evidence("EV-001", '{"material":"100123","plant":"5023","stock":120}', "stock"),
        evidence("EV-002", '{"material":"100123","plant":"5023","stock":80}', "stock"),
    ])
    assert result.contradictions == (("EV-001", "EV-002"),)
    assert any(item.relation == "contradicts" for item in result.relations)


def test_correlation_is_deterministic():
    items = [
        evidence("EV-001", '{"material":"100123","plant":"5023","stock":120}', "stock"),
        evidence("EV-002", '{"material":"100123","plant":"5023","stock":80}', "stock"),
    ]
    assert correlate_evidence(items).as_dict() == correlate_evidence(items).as_dict()
