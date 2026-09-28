from src.investigation.conclusion import build_conclusion
from src.investigation.evidence_state import EvidenceState
from src.investigation.hypothesis import Hypothesis


def hyp(status="SUPPORTED", ids=("E1",)):
    return Hypothesis(
        "H1",
        "Relación funcional observada.",
        status,
        ids,
        "evidence supports relation",
    )


def test_conclusion_gate_blocks_conflicting_evidence():
    result = build_conclusion(
        (hyp(),),
        (EvidenceState("E1", "CONFLICTING", "conflict"),),
    )
    assert result.status == "BLOCKED"
    assert "conflicto" in result.statement


def test_missing_evidence_prevents_confirmed_conclusion():
    result = build_conclusion(
        (hyp(),),
        (EvidenceState("E1", "AVAILABLE", "observed"),),
        missing=("capability:relevant_movements",),
    )
    assert result.status == "QUALIFIED"
    assert "causa raíz" in result.statement


def test_supported_hypothesis_is_confirmed_without_claiming_root_cause():
    result = build_conclusion(
        (hyp(),),
        (EvidenceState("E1", "AVAILABLE", "observed"),),
    )
    assert result.status == "CONFIRMED"
    assert "causa raíz" in result.statement


def test_partial_hypothesis_remains_qualified():
    result = build_conclusion(
        (hyp("PARTIALLY_SUPPORTED"),),
        (EvidenceState("E1", "AVAILABLE", "observed"),),
    )
    assert result.status == "QUALIFIED"


def test_no_hypothesis_is_unverified():
    result = build_conclusion(
        (),
        (),
    )
    assert result.status == "UNVERIFIED"



def test_supported_hypothesis_requires_explicit_available_state_for_every_evidence():
    result = build_conclusion(
        (Hypothesis("H1", "Relación funcional observada.", "SUPPORTED", ("E1", "E2"), "evidence supports relation"),),
        (EvidenceState("E1", "AVAILABLE", "observed"), EvidenceState("E2", "MISSING", "not retrieved")),
    )
    assert result.status == "QUALIFIED"
    assert "AVAILABLE" in result.reason


def test_supported_hypothesis_with_unknown_state_is_not_confirmed():
    result = build_conclusion(
        (hyp(),),
        (),
    )
    assert result.status == "QUALIFIED"
