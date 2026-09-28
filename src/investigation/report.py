"""Structured, deterministic report contract for SAP investigations."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable

from src.investigation.conclusion import ConclusionDecision
from src.investigation.contracts import InvestigationEvidence
from src.investigation.evidence_state import EvidenceState
from src.investigation.hypothesis import Hypothesis


@dataclass(frozen=True)
class InvestigationReport:
    case_id: str
    intent: str
    evidence: tuple[dict[str, Any], ...]
    evidence_states: tuple[dict[str, Any], ...]
    hypotheses: tuple[dict[str, Any], ...]
    findings: tuple[str, ...]
    conclusion: str
    conclusion_status: str
    conclusion_reason: str
    missing_information: tuple[str, ...]
    provenance: tuple[dict[str, Any], ...]

    def as_dict(self) -> dict[str, Any]:
        return {
            "case_id": self.case_id,
            "intent": self.intent,
            "evidence": list(self.evidence),
            "evidence_states": list(self.evidence_states),
            "hypotheses": list(self.hypotheses),
            "findings": list(self.findings),
            "conclusion": self.conclusion,
            "conclusion_status": self.conclusion_status,
            "conclusion_reason": self.conclusion_reason,
            "missing_information": list(self.missing_information),
            "provenance": list(self.provenance),
        }


def build_report(
    *,
    case_id: str,
    intent: str,
    evidence: Iterable[InvestigationEvidence],
    states: Iterable[EvidenceState],
    hypotheses: Iterable[Hypothesis],
    findings: Iterable[str],
    decision: ConclusionDecision,
    missing_information: Iterable[str],
    provenance: Iterable[dict[str, Any]],
) -> InvestigationReport:
    evidence = tuple(evidence)
    states = tuple(states)
    hypotheses = tuple(hypotheses)
    state_by_id = {item.evidence_id: item for item in states}

    evidence_rows = tuple(
        {
            "evidence_id": item.evidence_id,
            "provider": item.provider,
            "operation": item.operation,
            "landscape": item.landscape,
            "system": item.system,
            "object_type": item.object_type,
            "object_id": item.object_id,
            "observation_type": item.observation_type,
            "certainty": item.certainty,
            "state": state_by_id.get(
                item.evidence_id,
                EvidenceState(item.evidence_id, "MISSING", "No semantic state was assigned."),
            ).state,
        }
        for item in evidence
    )
    state_rows = tuple(
        {
            "evidence_id": item.evidence_id,
            "state": item.state,
            "reason": item.reason,
        }
        for item in states
    )
    hypothesis_rows = tuple(
        {
            "hypothesis_id": item.hypothesis_id,
            "statement": item.statement,
            "status": item.status,
            "evidence_ids": list(item.evidence_ids),
            "reason": item.reason,
        }
        for item in hypotheses
    )

    return InvestigationReport(
        case_id=case_id,
        intent=intent,
        evidence=evidence_rows,
        evidence_states=state_rows,
        hypotheses=hypothesis_rows,
        findings=tuple(dict.fromkeys(findings)),
        conclusion=decision.statement,
        conclusion_status=decision.status,
        conclusion_reason=decision.reason,
        missing_information=tuple(dict.fromkeys(missing_information)),
        provenance=tuple(provenance),
    )


def render_report(report: InvestigationReport) -> str:
    lines = [
        f"Investigation Report: {report.case_id}",
        f"Intent: {report.intent}",
        "",
        "Evidence:",
    ]
    lines.extend(
        f"- [{item['evidence_id']}] {item['landscape']} · {item['observation_type']} · "
        f"certainty={item['certainty']} · state={item['state']}"
        for item in report.evidence
    ) or lines.append("- None")
    lines.extend(["", "Hypotheses:"])
    lines.extend(
        f"- [{item['hypothesis_id']}] {item['status']}: {item['statement']}"
        for item in report.hypotheses
    ) or lines.append("- None")
    lines.extend(["", "Findings:"])
    lines.extend(f"- {item}" for item in report.findings) or lines.append("- None")
    lines.extend([
        "",
        f"Conclusion status: {report.conclusion_status}",
        report.conclusion,
        f"Reason: {report.conclusion_reason}",
        "",
        "Missing information:",
    ])
    lines.extend(f"- {item}" for item in report.missing_information) or lines.append("- None")
    return "\n".join(lines) + "\n"
