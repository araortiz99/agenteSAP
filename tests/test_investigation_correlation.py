import json
from pathlib import Path

from src.investigation.contracts import InvestigationEvidence
from src.investigation.correlation import correlate_evidence


FIXTURES = Path(__file__).parent / "fixtures" / "investigation"


def load_fixture(name: str) -> list[InvestigationEvidence]:
    payload = json.loads((FIXTURES / name).read_text(encoding="utf-8"))
    return [
        InvestigationEvidence(
            evidence_id=item["evidence_id"],
            provider="fixture",
            operation="read",
            landscape="QAS",
            system="QAS",
            object_type="SAP_RUNTIME",
            object_id=item.get("object_id"),
            observation_type=item["observation_type"],
            content=item["content"],
            certainty="high",
            provenance=(("fixture", item["evidence_id"]),),
        )
        for item in payload["evidence"]
    ]


def test_basic_golden_fixture_is_related_and_preserves_provenance():
    items = load_fixture("stock_discrepancy_basic.json")
    result = correlate_evidence(items)
    assert ("EV-001", "EV-002") not in result.contradictions
    assert any(item.relation == "related_to" for item in result.relations)
    assert result.evidence_ids == ("EV-001", "EV-002")
    assert all(item.provenance for item in items)


def test_movement_golden_fixture_is_correlated_without_claiming_causality():
    result = correlate_evidence(load_fixture("stock_discrepancy_movement.json"))
    relation = next(item for item in result.relations if item.relation == "explains")
    assert relation.source_evidence_id == "EV-002"
    assert relation.target_evidence_id == "EV-001"
    assert relation.certainty == "medium"
    assert "movimiento" in relation.reason.lower()
    assert "causa" not in relation.reason.lower()


def test_missing_evidence_golden_fixture_creates_gap_without_invention():
    result = correlate_evidence(load_fixture("stock_discrepancy_missing_evidence.json"))
    assert "structured_fields_missing_for_correlation" in result.gaps
    assert result.unresolved_relationships


def test_conflicting_golden_fixture_is_explicit():
    result = correlate_evidence(load_fixture("stock_discrepancy_conflict.json"))
    assert result.contradictions == (("EV-001", "EV-002"),)
    assert any(item.relation == "contradicts" for item in result.relations)


def test_correlation_is_deterministic():
    items = load_fixture("stock_discrepancy_conflict.json")
    assert correlate_evidence(items).as_dict() == correlate_evidence(items).as_dict()
