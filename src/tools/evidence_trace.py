"""Stable evidence traceability for retrieval and reasoning results."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib

from src.tools.evidence import ConflictRecord, EvidenceAssessment, EvidenceItem
from src.tools.reason import ReasoningResult


@dataclass(frozen=True)
class EvidenceTrace:
    evidence_id: str
    path: str
    source_layer: str
    source_id: str | None
    knowledge_type: str
    knowledge_scope: str
    certainty: str
    weight: float
    role: str
    reason: str


@dataclass(frozen=True)
class TraceabilityReport:
    trace_id: str
    query: str
    conclusion_status: str
    conclusion: str
    evidence: tuple[EvidenceTrace, ...]
    supporting_evidence_ids: tuple[str, ...]
    unresolved_evidence_ids: tuple[str, ...]
    gaps: tuple[str, ...]
    conflicts: tuple[ConflictRecord, ...]


def _evidence_id(item: EvidenceItem) -> str:
    """Create a deterministic ID from provenance, not from retrieval order."""
    raw = "|".join(
        (
            item.source_layer,
            item.source_id or "",
            item.path,
            item.knowledge_type,
            item.knowledge_scope,
            item.certainty,
        )
    )
    return "EVD-" + hashlib.sha256(raw.encode("utf-8")).hexdigest()[:12].upper()


def _role(item: EvidenceItem) -> str:
    if item.certainty == "confirmed" and item.supports:
        return "supporting"
    if item.certainty in {"partial", "under_validation"}:
        return "unresolved"
    return "non_supporting"


def build_traceability(reasoning: ReasoningResult) -> TraceabilityReport:
    traces = tuple(
        EvidenceTrace(
            evidence_id=_evidence_id(item),
            path=item.path,
            source_layer=item.source_layer,
            source_id=item.source_id,
            knowledge_type=item.knowledge_type,
            knowledge_scope=item.knowledge_scope,
            certainty=item.certainty,
            weight=item.weight,
            role=_role(item),
            reason=item.reason,
        )
        for item in reasoning.evidence.items
    )

    supporting = tuple(x.evidence_id for x in traces if x.role == "supporting")
    unresolved = tuple(x.evidence_id for x in traces if x.role == "unresolved")

    return TraceabilityReport(
        trace_id="TRACE-" + hashlib.sha256(
            reasoning.query.encode("utf-8")
        ).hexdigest()[:12].upper(),
        query=reasoning.query,
        conclusion_status=reasoning.conclusion_status,
        conclusion=reasoning.conclusion,
        evidence=traces,
        supporting_evidence_ids=supporting,
        unresolved_evidence_ids=unresolved,
        gaps=reasoning.evidence.gaps,
        conflicts=reasoning.conflicts,
    )


def render_traceability(report: TraceabilityReport) -> str:
    """Render an auditable, human-readable evidence report."""
    lines = [
        f"# Evidence Trace {report.trace_id}",
        "",
        "## Query",
        report.query,
        "",
        "## Conclusion Status",
        report.conclusion_status,
        "",
        "## Conclusion",
        report.conclusion,
        "",
        "## Evidence",
    ]
    for item in report.evidence:
        lines.extend(
            [
                "",
                f"### {item.evidence_id}",
                f"- Path: {item.path}",
                f"- Source layer: {item.source_layer}",
                f"- Source ID: {item.source_id or 'unknown'}",
                f"- Knowledge type: {item.knowledge_type}",
                f"- Knowledge scope: {item.knowledge_scope}",
                f"- Certainty: {item.certainty}",
                f"- Weight: {item.weight}",
                f"- Role: {item.role}",
                f"- Reason: {item.reason}",
            ]
        )

    lines.extend(["", "## Supporting Evidence IDs"])
    lines.extend(f"- {x}" for x in report.supporting_evidence_ids)
    lines.extend(["", "## Unresolved Evidence IDs"])
    lines.extend(f"- {x}" for x in report.unresolved_evidence_ids)
    lines.extend(["", "## Gaps"])
    lines.extend(f"- {x}" for x in report.gaps)
    lines.extend(["", "## Conflicts"])
    for conflict in report.conflicts:
        lines.extend(
            [
                "",
                f"### {conflict.conflict_type}",
                f"- Status: {conflict.status}",
                f"- Description: {conflict.description}",
                "- Evidence paths:",
                *[f"  - {path}" for path in conflict.evidence_paths],
            ]
        )
    return "\n".join(lines) + "\n"
