"""Deterministic reasoning over evidence assessments."""

from __future__ import annotations

from dataclasses import dataclass

from src.tools.evidence import ConflictRecord, EvidenceAssessment


@dataclass(frozen=True)
class ReasoningResult:
    query: str
    conclusion_status: str
    conclusion: str
    evidence: EvidenceAssessment
    conflicts: tuple[ConflictRecord, ...]


def reason_from_evidence(evidence: EvidenceAssessment) -> ReasoningResult:
    """Produce a bounded conclusion status; never invent functional semantics."""
    conflicts = evidence.conflicts

    if conflicts:
        conclusion_status = "conflict"
        conclusion = (
            "The retrieved evidence contains explicit metadata or documented "
            "conflicts. A functional conclusion must not be produced until "
            "the conflict is resolved."
        )
    elif evidence.requires_analysis:
        conclusion_status = "requires_analysis"
        conclusion = (
            "SAP Standard and internal evidence are both available. "
            "They must be compared functionally; their coexistence does not establish equivalence."
        )
    elif evidence.confirmed:
        conclusion_status = "supported"
        conclusion = (
            "The retrieved evidence contains confirmed information, but the conclusion "
            "is limited to what those sources explicitly support."
        )
    elif evidence.partial or evidence.under_validation:
        conclusion_status = "partial"
        conclusion = (
            "The retrieved evidence is incomplete or still under validation. "
            "A confirmed conclusion is not supported."
        )
    else:
        conclusion_status = "insufficient"
        conclusion = "The retrieved evidence is insufficient for a confirmed conclusion."

    return ReasoningResult(
        query=evidence.query,
        conclusion_status=conclusion_status,
        conclusion=conclusion,
        evidence=evidence,
        conflicts=conflicts,
    )
