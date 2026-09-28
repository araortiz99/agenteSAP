"""Serializable contracts for consultative SAP investigations."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from src.investigation.correlation import EvidenceCorrelation


@dataclass(frozen=True)
class InvestigationEntity:
    entity_type: str
    value: str
    source: str = "user"
    required: bool = True


@dataclass(frozen=True)
class InvestigationEvidence:
    evidence_id: str
    provider: str
    operation: str
    landscape: str
    system: str | None
    object_type: str
    object_id: str | None
    observation_type: str
    content: str
    certainty: str
    provenance: tuple[tuple[str, str], ...] = ()


@dataclass(frozen=True)
class InvestigationStep:
    step_id: str
    purpose: str
    evidence_type: str
    required_entities: tuple[str, ...]
    capability: str | None = None
    status: str = "planned"


@dataclass
class Investigation:
    case_id: str
    user_question: str
    intent: str
    entities: tuple[InvestigationEntity, ...] = ()
    required_evidence: tuple[str, ...] = ()
    evidence_collected: list[InvestigationEvidence] = field(default_factory=list)
    evidence_missing: list[str] = field(default_factory=list)
    hypotheses: list[str] = field(default_factory=list)
    findings: list[str] = field(default_factory=list)
    conclusion: str = ""
    confidence: str = "LOW"
    confidence_reason: str = ""
    provenance: list[dict[str, Any]] = field(default_factory=list)
    correlation: EvidenceCorrelation = field(default_factory=EvidenceCorrelation)
    stop_reason: str | None = None
    steps: list[InvestigationStep] = field(default_factory=list)

    def as_dict(self) -> dict[str, Any]:
        return {
            "case_id": self.case_id,
            "user_question": self.user_question,
            "intent": self.intent,
            "entities": [entity.__dict__ for entity in self.entities],
            "required_evidence": list(self.required_evidence),
            "evidence_collected": [item.__dict__ for item in self.evidence_collected],
            "evidence_missing": list(self.evidence_missing),
            "hypotheses": list(self.hypotheses),
            "findings": list(self.findings),
            "conclusion": self.conclusion,
            "confidence": self.confidence,
            "confidence_reason": self.confidence_reason,
            "provenance": list(self.provenance),
            "correlation": self.correlation.as_dict(),
            "stop_reason": self.stop_reason,
            "steps": [step.__dict__ for step in self.steps],
        }


def serialize_investigation(investigation: Investigation) -> dict[str, Any]:
    """Return a stable JSON-compatible representation."""
    return investigation.as_dict()
