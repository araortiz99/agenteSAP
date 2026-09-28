"""LLM-backed consultative layer over bounded SAP evidence."""

from __future__ import annotations

from dataclasses import dataclass

from src.github.client import GitHubClient
from src.llm.client import LLMClient
from src.tools.evidence import EvidenceAssessment, assess_evidence
from src.tools.evidence_trace import TraceabilityReport, build_traceability
from src.tools.reason import ReasoningResult, reason_from_evidence
from src.tools.search_unified import UnifiedResult, UnifiedSearchResult, search_unified


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

Prefer concise, structured answers suitable for a senior SAP functional analyst.
"""


@dataclass(frozen=True)
class ConsultationResult:
    request: str
    retrieval: UnifiedSearchResult
    evidence: EvidenceAssessment
    reasoning: ReasoningResult
    traceability: TraceabilityReport
    answer: str
    model: str


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
        f"Bounded conclusion: {traceability.conclusion}",
        "",
        "## Evidence records",
    ]
    trace_by_path = {item.path: item for item in traceability.evidence}
    for result in retrieval.results:
        trace = trace_by_path[result.path]
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
                f"role: {trace.role}",
                "content:",
                _snippet(result),
            ]
        )
    lines.extend(["", "## Gaps"])
    lines.extend(f"- {gap}" for gap in traceability.gaps)
    lines.extend(["", "## Conflicts"])
    lines.extend(f"- {conflict}" for conflict in traceability.conflicts)
    return "\n".join(lines)


def consult(
    client: GitHubClient,
    request: str,
    llm: LLMClient,
    *,
    ref: str = "main",
    max_results: int = 8,
) -> ConsultationResult:
    """Retrieve, assess, trace and synthesize a consultative answer."""
    if not request or not request.strip():
        raise ValueError("request must not be empty")

    retrieval = search_unified(client, request, max_results=max_results, ref=ref)
    evidence = assess_evidence(retrieval)
    reasoning = reason_from_evidence(evidence)
    traceability = build_traceability(reasoning)
    context = build_context(retrieval, traceability)

    user_prompt = (
        "User request:\n"
        f"{request.strip()}\n\n"
        "Use only the following bounded repository evidence.\n\n"
        f"{context}"
    )
    answer = llm.generate(system_prompt=SYSTEM_PROMPT, user_prompt=user_prompt)
    model = getattr(llm, "model", llm.__class__.__name__)

    return ConsultationResult(
        request=request.strip(),
        retrieval=retrieval,
        evidence=evidence,
        reasoning=reasoning,
        traceability=traceability,
        answer=answer,
        model=str(model),
    )
