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
    hypotheses: tuple[dict[str, Any], ...]
    findings: tuple[str, ...]
    conclusion_status: str
    conclusion_reason: str
    investigation_report: dict[str, Any] | None
    evidence_states: tuple[dict[str, Any], ...]
    evidence: tuple[dict[str, Any], ...]
    retrieval: tuple[dict[str, Any], ...]
    knowledge_intelligence: dict[str, Any]
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


def _retrieval(result: ConsultationResult) -> tuple[dict[str, Any], ...]:
    return tuple(
        {
            "path": item.path,
            "score": item.score,
            "matched_terms": item.matched_terms,
            "source_layer": item.source_layer,
            "match_type": item.match_type,
            "source_id": item.source_id,
            "knowledge_type": item.knowledge_type,
            "knowledge_scope": item.knowledge_scope,
            "certainty": item.certainty,
            "provenance": item.provenance,
        }
        for item in result.retrieval.results
    )



def _knowledge_intelligence(result: ConsultationResult) -> dict[str, Any]:
    context = result.knowledge_context
    if context is None:
        return {
            "query": result.request,
            "entities": (),
            "relationships": (),
            "evidence": (),
            "gaps": (),
            "conflicts": (),
            "max_hops": 0,
        }
    return {
        "query": context.query,
        "max_hops": context.max_hops,
        "entities": tuple(asdict(item) for item in context.entities),
        "relationships": tuple(
            {
                **asdict(item.relationship),
                "hop": item.hop,
            }
            for item in context.relationships
        ),
        "evidence": tuple(
            {
                "path": item.result.path,
                "score": item.result.score,
                "source_layer": item.result.source_layer,
                "source_id": item.result.source_id,
                "knowledge_type": item.result.knowledge_type,
                "knowledge_scope": item.result.knowledge_scope,
                "certainty": item.result.certainty,
                "hop": item.hop,
                "discovery": item.discovery,
            }
            for item in context.evidence
        ),
        "gaps": context.gaps,
        "conflicts": tuple(asdict(item) for item in context.conflicts),
    }


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
    hypotheses = tuple(
        {
            "hypothesis_id": item.hypothesis_id,
            "statement": item.statement,
            "status": item.status,
            "evidence_ids": item.evidence_ids,
            "reason": item.reason,
        }
        for item in (result.investigation.hypotheses if result.investigation else ())
    )
    findings = tuple(result.investigation.findings if result.investigation else ())
    conclusion_status = result.investigation.conclusion_status if result.investigation else "UNVERIFIED"
    conclusion_reason = result.investigation.conclusion_reason if result.investigation else "No investigation was executed."
    investigation_report = result.investigation.report.as_dict() if result.investigation and result.investigation.report else None
    evidence_states = tuple(
        {
            "evidence_id": item.evidence_id,
            "state": item.state,
            "reason": item.reason,
        }
        for item in (result.investigation.evidence_states if result.investigation else ())
    )

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
        findings=findings,
        conclusion_status=conclusion_status,
        conclusion_reason=conclusion_reason,
        investigation_report=investigation_report,
        evidence_states=evidence_states,
        evidence=_evidence(result),
        retrieval=_retrieval(result),
        knowledge_intelligence=_knowledge_intelligence(result),
        relationships=_relationships(result),
        conflicts=tuple(asdict(item) for item in result.evidence.conflicts),
        gaps=result.traceability.gaps,
        ticket=ticket,
        diagnostics=diagnostics,
        runtime=runtime,
        answer=answer,
    )
