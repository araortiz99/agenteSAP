"""Structured response contracts for the AgenteSAP Workbench.

The workbench consumes these structures as its primary UI state while the
legacy result payload remains available for backward compatibility.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from src.agent.consultant import ConsultationResult


@dataclass(frozen=True)
class WorkbenchAnalysisResponse:
    request_id: str
    trace_id: str
    query: str
    intent: str
    summary: str
    confirmed: tuple[str, ...]
    implementation: tuple[str, ...]
    not_confirmed: tuple[str, ...]
    hypotheses: tuple[str, ...]
    evidence: tuple[dict[str, Any], ...]
    relationships: tuple[dict[str, Any], ...]
    conflicts: tuple[dict[str, Any], ...]
    gaps: tuple[str, ...]
    ticket: dict[str, Any] | None
    diagnostics: dict[str, Any]
    runtime: dict[str, Any]
    answer: str


def _section(answer: str, title: str, next_titles: tuple[str, ...]) -> str:
    start = answer.find(title)
    if start < 0:
        return ""
    body = answer[start + len(title):]
    end = len(body)
    for next_title in next_titles:
        position = body.find(next_title)
        if position >= 0:
            end = min(end, position)
    return body[:end].strip()


def _items(text: str) -> tuple[str, ...]:
    if not text:
        return ()
    lines = tuple(
        line.strip()[2:].strip()
        for line in text.splitlines()
        if line.strip().startswith(("- ", "* "))
    )
    return tuple(line for line in lines if line)


def _evidence(result: ConsultationResult) -> tuple[dict[str, Any], ...]:
    return tuple(asdict(item) for item in result.traceability.evidence)


def _relationships(result: ConsultationResult) -> tuple[dict[str, Any], ...]:
    related = result.ticket_relationships
    if related is None:
        return ()
    return tuple(asdict(item) for item in related.relationships)


def build_workbench_analysis(
    result: ConsultationResult,
    *,
    request_id: str,
    intent: str,
    diagnostics: dict[str, Any],
    runtime: dict[str, Any],
) -> WorkbenchAnalysisResponse:
    answer = result.answer
    confirmed = _section(
        answer,
        "## Qué está confirmado",
        ("## Qué corresponde a nuestra implementación", "## Qué no está confirmado"),
    )
    implementation = _section(
        answer,
        "## Qué corresponde a nuestra implementación",
        ("## Qué no está confirmado", "## Evidencias"),
    )
    not_confirmed = _section(
        answer,
        "## Qué no está confirmado",
        ("## Evidencias", "## Ticket"),
    )
    summary = _section(
        answer,
        "## Resumen",
        ("## Qué está confirmado",),
    )
    hypotheses = ()

    ticket = None
    if result.ticket_context:
        ticket = {
            "references": [asdict(item) for item in result.ticket_context],
            "ticket_id": result.ticket_context[0].ticket_id,
        }

    return WorkbenchAnalysisResponse(
        request_id=request_id,
        trace_id=result.traceability.trace_id,
        query=result.request,
        intent=intent,
        summary=summary,
        confirmed=_items(confirmed) or ((confirmed,) if confirmed else ()),
        implementation=_items(implementation) or ((implementation,) if implementation else ()),
        not_confirmed=_items(not_confirmed) or ((not_confirmed,) if not_confirmed else ()),
        hypotheses=hypotheses,
        evidence=_evidence(result),
        relationships=_relationships(result),
        conflicts=tuple(asdict(item) for item in result.evidence.conflicts),
        gaps=result.traceability.gaps,
        ticket=ticket,
        diagnostics=diagnostics,
        runtime=runtime,
        answer=answer,
    )
