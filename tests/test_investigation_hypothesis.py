from src.investigation.correlation import EvidenceCorrelation, EvidenceRelation
from src.investigation.evidence_state import (
    EvidenceState,
    assess_investigation_evidence_state,
    summarize_states,
)
from src.investigation.hypothesis import build_hypotheses
from src.investigation.contracts import InvestigationEvidence


def ev(evidence_id, observation_type, certainty="confirmed", content='{"material":"100123","plant":"5023","stock":10}'):
    return InvestigationEvidence(
        evidence_id=evidence_id,
        provider="test",
        operation="read",
        landscape="QAS",
        system="QAS",
        object_type="SAP_RUNTIME",
        object_id=None,
        observation_type=observation_type,
        content=content,
        certainty=certainty,
    )


def test_evidence_state_precedence_is_deterministic():
    assert assess_investigation_evidence_state("E1", available=False).state == "MISSING"
    assert assess_investigation_evidence_state("E1", available=True, sufficient=False).state == "INSUFFICIENT"
    assert assess_investigation_evidence_state("E1", available=True, conflicting=True).state == "CONFLICTING"
    assert assess_investigation_evidence_state("E1", available=True, valid=False).state == "INVALID"
    assert assess_investigation_evidence_state("E1", available=True, applicable=False).state == "NOT_APPLICABLE"


def test_missing_is_not_false_and_states_are_counted():
    states = (
        EvidenceState(None, "MISSING", "runtime not available"),
        EvidenceState("E1", "AVAILABLE", "observed"),
    )
    summary = summarize_states(states)
    assert summary["MISSING"] == 1
    assert summary["AVAILABLE"] == 1


def test_movement_stock_hypothesis_is_partial_when_certainty_is_unknown():
    evidence = (
        ev("E1", "movement", certainty="unknown"),
        ev("E2", "stock", certainty="confirmed"),
    )
    correlation = EvidenceCorrelation(
        evidence_ids=("E1", "E2"),
        relations=(
            EvidenceRelation(
                "E1",
                "E2",
                "explains",
                "medium",
                "same entity",
            ),
        ),
    )
    states = tuple(EvidenceState(item.evidence_id, "AVAILABLE", "observed") for item in evidence)

    hypotheses = build_hypotheses(evidence, states, correlation)

    assert hypotheses[0].status == "PARTIALLY_SUPPORTED"
    assert "causa raíz" in hypotheses[0].reason


def test_conflicting_observations_are_not_supported():
    evidence = (
        ev("E1", "stock", content='{"material":"100123","plant":"5023","stock":10}'),
        ev("E2", "stock", content='{"material":"100123","plant":"5023","stock":20}'),
    )
    correlation = EvidenceCorrelation(
        evidence_ids=("E1", "E2"),
        relations=(
            EvidenceRelation(
                "E1",
                "E2",
                "contradicts",
                "high",
                "same entity with incompatible stock",
            ),
        ),
        contradictions=(("E1", "E2"),),
    )
    states = (
        EvidenceState("E1", "CONFLICTING", "conflict"),
        EvidenceState("E2", "CONFLICTING", "conflict"),
    )

    hypotheses = build_hypotheses(evidence, states, correlation)

    assert any(item.status == "CONTRADICTED" for item in hypotheses)
