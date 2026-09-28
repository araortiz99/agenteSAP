from src.investigation.conclusion import ConclusionDecision
from src.investigation.contracts import InvestigationEvidence
from src.investigation.evidence_state import EvidenceState
from src.investigation.hypothesis import Hypothesis
from src.investigation.report import build_report, render_report


def ev():
    return InvestigationEvidence(
        "E1", "test", "read", "QAS", "QAS", "SAP_RUNTIME", "100123",
        "stock", '{"stock":10}', "confirmed"
    )


def test_report_is_structured_and_deterministic():
    report = build_report(
        case_id="INV-20260928-ABC",
        intent="stock_discrepancy",
        evidence=(ev(),),
        states=(EvidenceState("E1", "AVAILABLE", "observed"),),
        hypotheses=(Hypothesis("H1", "Relation", "SUPPORTED", ("E1",), "ok"),),
        findings=("runtime observed", "runtime observed"),
        decision=ConclusionDecision("CONFIRMED", "Conclusion", "reason", ("E1",)),
        missing_information=("capability:x", "capability:x"),
        provenance=({"evidence_id": "E1"},),
    )
    assert report.evidence[0]["state"] == "AVAILABLE"
    assert report.findings == ("runtime observed",)
    assert report.missing_information == ("capability:x",)
    assert report.as_dict()["conclusion_status"] == "CONFIRMED"


def test_report_render_preserves_gate_status_and_gaps():
    report = build_report(
        case_id="INV-20260928-ABC",
        intent="stock_discrepancy",
        evidence=(),
        states=(),
        hypotheses=(),
        findings=(),
        decision=ConclusionDecision("UNVERIFIED", "No conclusion", "missing evidence"),
        missing_information=("capability:current_stock",),
        provenance=(),
    )
    rendered = render_report(report)
    assert "Conclusion status: UNVERIFIED" in rendered
    assert "capability:current_stock" in rendered
