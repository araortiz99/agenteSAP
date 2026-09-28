"""LLM-backed consultative layer over bounded SAP evidence."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import re

from src.github.client import GitHubClient
from src.llm.client import LLMClient
from src.sap.mcp_gateway import McpEvidenceGateway
from src.tools.evidence import EvidenceAssessment, assess_evidence
from src.tools.evidence_trace import TraceabilityReport, build_traceability
from src.tools.reason import ReasoningResult, reason_from_evidence
from src.tools.search_unified import UnifiedResult, UnifiedSearchResult, search_unified, unified_result_key
from src.tools.source_selection import select_evidence_sources
from src.tools.get_ticket import TicketContext, get_ticket
from src.tools.get_related_knowledge import RelatedKnowledge, get_related_knowledge
from src.tools.knowledge_context import KnowledgeContext, build_knowledge_context, render_knowledge_context
from src.agent.investigation import InvestigationResult, investigate


SYSTEM_PROMPT = """You are agenteSAP, a consultative SAP functional assistant.

Answer in Spanish unless the user explicitly asks for another language.
Your knowledge boundary is the evidence supplied in the user context. Do not invent
SAP behavior, configuration, custom development, tickets, objects, causes, or fixes.

Rules:
1. Treat SAP Standard and internal/customer knowledge as different evidence layers.
2. Preserve every certainty value supplied in the context. Never upgrade partial,
   under_validation, inferred, or not_confirmed information to confirmed.
3. A missing source is not proof that something does not exist.
4. When evidence is insufficient, say exactly what is missing.
5. When Standard and internal evidence coexist, compare them only when the supplied
   evidence supports the comparison; do not assume equivalence.
6. Cite evidence inline using its EVD identifier, for example [EVD-ABC123].
7. Distinguish documented facts, functional interpretation, and proposed next steps.
8. You are read-only: never claim to have executed SAP, changed configuration,
   changed code, modified GitHub, or validated something in a real SAP system.

Return the answer using exactly these Markdown sections, in this order:
## Resumen
## Qué está confirmado
## Qué corresponde a nuestra implementación
## Qué no está confirmado
## Evidencias
## Ticket
## Próximos pasos

Do not omit sections. If a section has no information, explicitly state that the
available evidence does not provide it. Cite relevant evidence inline using [EVD-*].
For Ticket, use the supplied TKT-* identifier when ticket context exists.
Separate SAP Standard from internal/custom evidence. Never claim execution.
Never invent causes, solutions, configuration, objects or facts.

Prefer concise, structured answers suitable for a senior SAP functional analyst.
"""


@dataclass(frozen=True)
class Citation:
    citation_id: str
    evidence_id: str
    path: str
    source_id: str | None
    certainty: str


@dataclass(frozen=True)
class TicketContextReference:
    reference_id: str
    ticket_id: str
    path: str
    content: str


@dataclass(frozen=True)
class ConsultationResult:
    request: str
    retrieval: UnifiedSearchResult
    evidence: EvidenceAssessment
    reasoning: ReasoningResult
    traceability: TraceabilityReport
    answer: str
    model: str
    citations: tuple[Citation, ...]
    uncited_evidence_ids: tuple[str, ...]
    ticket_context: tuple[TicketContextReference, ...]
    ticket_relationships: RelatedKnowledge | None
    knowledge_context: KnowledgeContext | None = None
    investigation: InvestigationResult | None = None


def _ticket_reference(ticket_id: str, path: str) -> str:
    raw = f"{ticket_id}|{path}"
    return "TKT-" + hashlib.sha256(raw.encode("utf-8")).hexdigest()[:12].upper()


_REQUIRED_SECTIONS = (
    "## Resumen",
    "## Qué está confirmado",
    "## Qué corresponde a nuestra implementación",
    "## Qué no está confirmado",
    "## Evidencias",
    "## Ticket",
    "## Próximos pasos",
)


class ConsultationFormatError(ValueError):
    """Raised when the LLM response violates the MVP 4.2 answer contract."""


def _validate_answer_structure(answer: str) -> None:
    positions = []
    for section in _REQUIRED_SECTIONS:
        position = answer.find(section)
        if position < 0:
            raise ConsultationFormatError(
                f"LLM answer is missing required section: {section}"
            )
        positions.append(position)

    if positions != sorted(positions):
        raise ConsultationFormatError(
            "LLM answer sections are not in the required order."
        )


def _validate_ticket_reference(
    answer: str,
    ticket_context: tuple[TicketContextReference, ...],
) -> None:
    if ticket_context and not any(
        reference.reference_id in answer for reference in ticket_context
    ):
        raise ConsultationFormatError(
            "LLM answer does not reference the supplied TKT-* ticket context."
        )

def _parse_citations(
    answer: str,
    traceability: TraceabilityReport,
) -> tuple[Citation, ...]:
    by_evidence = {item.evidence_id: item for item in traceability.evidence}
    cited_ids = dict.fromkeys(re.findall(r"\[(EVD-[A-Z0-9]+)\]", answer))
    citations = []
    for evidence_id in cited_ids:
        item = by_evidence.get(evidence_id)
        if item is None:
            raise ValueError(f"LLM cited unknown evidence id: {evidence_id}")
        citations.append(
            Citation(
                citation_id=evidence_id,
                evidence_id=evidence_id,
                path=item.path,
                source_id=item.source_id,
                certainty=item.certainty,
            )
        )
    return tuple(citations)


def _ticket_context(
    client: GitHubClient,
    ticket_id: str | None,
    ref: str,
) -> tuple[tuple[TicketContextReference, ...], RelatedKnowledge | None]:
    if not ticket_id:
        return (), None
    ticket = get_ticket(client, ticket_id, ref=ref)
    references = tuple(
        TicketContextReference(
            reference_id=_ticket_reference(ticket.ticket_id, document.path),
            ticket_id=ticket.ticket_id,
            path=document.path,
            content=document.content,
        )
        for document in ticket.documents
    )
    relationships = get_related_knowledge(client, "TICKET", ticket.ticket_id, ref=ref)
    return references, relationships


def _snippet(result: UnifiedResult, limit: int = 3500) -> str:
    content = result.content.strip()
    if len(content) <= limit:
        return content
    return content[:limit].rstrip() + "\n[contenido truncado]"


def build_context(
    retrieval: UnifiedSearchResult,
    traceability: TraceabilityReport,
) -> str:
    lines = [
        "## Evidence assessment",
        f"Query: {retrieval.query}",
        f"Conclusion status: {traceability.conclusion_status}",
        "",
        "## Source selection requirement",
        "Requested evidence layers: " + ", ".join(select_evidence_sources(retrieval.query).requested),
        "Rationale: " + " | ".join(select_evidence_sources(retrieval.query).rationale),
        "This is a retrieval requirement, not evidence or a conclusion.",
        f"Bounded conclusion: {traceability.conclusion}",
        "",
        "## Evidence records",
    ]
    trace_by_key = {
        (
            item.source_layer,
            item.path,
            item.source_id or "",
            tuple(sorted(item.provenance)),
        ): item
        for item in traceability.evidence
    }
    for result in retrieval.results:
        trace = trace_by_key[unified_result_key(result)]
        lines.extend(
            [
                "",
                f"### {trace.evidence_id}",
                f"path: {result.path}",
                f"source_layer: {result.source_layer}",
                f"source_id: {result.source_id or 'unknown'}",
                f"knowledge_type: {result.knowledge_type}",
                f"knowledge_scope: {result.knowledge_scope}",
                f"certainty: {result.certainty}",
                f"provenance: {dict(result.provenance)}",
                f"role: {trace.role}",
                "content:",
                _snippet(result),
            ]
        )
    lines.extend(["", "## Gaps"])
    lines.extend(f"- {gap}" for gap in traceability.gaps)
    lines.extend(["", "## Conflicts"])
    for conflict in traceability.conflicts:
        lines.extend(
            [
                "",
                f"- Type: {conflict.conflict_type}",
                f"  Status: {conflict.status}",
                f"  Description: {conflict.description}",
                "  Evidence paths:",
                *[f"    - {path}" for path in conflict.evidence_paths],
            ]
        )
    return "\n".join(lines)


def consult(
    client: GitHubClient,
    request: str,
    llm: LLMClient,
    *,
    ref: str = "main",
    max_results: int = 8,
    ticket_id: str | None = None,
    mcp_gateway: McpEvidenceGateway | None = None,
) -> ConsultationResult:
    """Retrieve, assess, trace and synthesize a consultative answer."""
    if not request or not request.strip():
        raise ValueError("request must not be empty")

    mcp_gateway = mcp_gateway if mcp_gateway is not None else McpEvidenceGateway.from_env()
    investigation = investigate(
        client,
        request,
        ref=ref,
        max_results=max_results,
        mcp_gateway=mcp_gateway,
    )
    retrieval = investigation.retrieval
    evidence = investigation.evidence
    reasoning = investigation.reasoning
    traceability = build_traceability(reasoning)
    ticket_context, ticket_relationships = _ticket_context(client, ticket_id, ref)
    context = build_context(retrieval, traceability)
    context += "\n\n## Query plan\n"
    context += f"Intent: {investigation.plan.intent}\n"
    context += f"Max steps: {investigation.plan.max_steps}\n"
    context += "Subqueries (retrieval hypotheses only):\n"
    context += "\n".join(f"- {item}" for item in investigation.plan.subqueries)
    knowledge_context = investigation.knowledge_context
    context += "\n\n" + render_knowledge_context(knowledge_context)
    if ticket_context:
        context += "\n\n## Ticket context\n"
        for item in ticket_context:
            context += f"\n### {item.reference_id}\npath: {item.path}\n{item.content.strip()}\n"
    if ticket_context:
        context += "\n## Ticket reference requirements\n"
        context += (
            "Use the supplied ticket reference IDs in the Ticket section: "
            + ", ".join(item.reference_id for item in ticket_context)
            + ".\n"
        )
    if ticket_relationships and ticket_relationships.relationships:
        context += "\n## Ticket relationships\n"
        for relation in ticket_relationships.relationships:
            context += f"\n- {relation.source_id} --{relation.relation_type}--> {relation.target_id}\n"

    user_prompt = (
        "User request:\n"
        f"{request.strip()}\n\n"
        "Use only the following bounded repository evidence.\n\n"
        f"{context}"
    )
    answer = llm.generate(system_prompt=SYSTEM_PROMPT, user_prompt=user_prompt).strip()
    _validate_answer_structure(answer)
    _validate_ticket_reference(answer, ticket_context)
    citations = _parse_citations(answer, traceability)
    cited_ids = {citation.evidence_id for citation in citations}
    uncited = tuple(
        item.evidence_id for item in traceability.evidence
        if item.role == "supporting" and item.evidence_id not in cited_ids
    )
    model = getattr(llm, "model", llm.__class__.__name__)

    return ConsultationResult(
        request=request.strip(),
        retrieval=retrieval,
        evidence=evidence,
        reasoning=reasoning,
        traceability=traceability,
        answer=answer,
        model=str(model),
        citations=citations,
        uncited_evidence_ids=uncited,
        ticket_context=ticket_context,
        ticket_relationships=ticket_relationships,
        knowledge_context=knowledge_context,
        investigation=investigation,
    )
