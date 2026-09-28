"""Bounded SAP investigation pipeline shared by the consultant and tests."""

from __future__ import annotations

from dataclasses import dataclass

from src.github.client import GitHubClient
from src.sap.mcp_gateway import McpEvidenceGateway
from src.investigation.correlation import EvidenceCorrelation, correlate_evidence
from src.investigation.evidence_state import EvidenceState
from src.investigation.hypothesis import Hypothesis, build_hypotheses
from src.investigation.semantic import unified_to_investigation_evidence
from src.tools.evidence import EvidenceAssessment, assess_evidence
from src.tools.knowledge_context import KnowledgeContext, build_knowledge_context
from src.tools.query_planner import QueryPlan, decompose_query
from src.tools.reason import ReasoningResult, reason_from_evidence
from src.tools.search_unified import (
    UnifiedResult,
    UnifiedSearchResult,
    search_unified,
    unified_result_key,
)


@dataclass(frozen=True)
class InvestigationResult:
    query: str
    plan: QueryPlan
    retrieval: UnifiedSearchResult
    evidence: EvidenceAssessment
    reasoning: ReasoningResult
    knowledge_context: KnowledgeContext
    evidence_states: tuple[EvidenceState, ...] = ()
    hypotheses: tuple[Hypothesis, ...] = ()
    correlation: EvidenceCorrelation | None = None


def _merge_retrievals(
    query: str,
    retrievals: tuple[UnifiedSearchResult, ...],
    *,
    max_results: int,
) -> UnifiedSearchResult:
    unique: dict[tuple[str, str, str, tuple[tuple[str, str], ...]], UnifiedResult] = {}
    for retrieval in retrievals:
        for result in retrieval.results:
            unique.setdefault(unified_result_key(result), result)

    ordered = sorted(
        unique.values(),
        key=lambda item: (
            -item.score,
            0 if item.source_layer == "sap_standard"
            else 1 if item.source_layer == "internal"
            else 2,
            item.path,
        ),
    )[:max_results]

    return UnifiedSearchResult(
        query=query.strip(),
        results=tuple(ordered),
        sap_standard=tuple(x for x in ordered if x.source_layer == "sap_standard"),
        internal=tuple(x for x in ordered if x.source_layer == "internal"),
        mcp=tuple(x for x in ordered if x.source_layer == "mcp"),
    )


def investigate(
    client: GitHubClient,
    query: str,
    *,
    ref: str = "main",
    max_steps: int = 4,
    max_results: int = 8,
    max_hops: int = 2,
    mcp_gateway: McpEvidenceGateway | None = None,
) -> InvestigationResult:
    """Execute the deterministic investigation chain before LLM synthesis.

    Query planning produces bounded retrieval hypotheses. Each hypothesis is
    retrieved through the normal source-selection policy. Evidence is assessed
    only after retrieval. Knowledge Context then resolves canonical entities
    and traverses only explicit relationships.
    """
    if not query or not query.strip():
        raise ValueError("query must not be empty")
    if max_results < 1:
        raise ValueError("max_results must be greater than zero")

    plan = decompose_query(query, max_steps=max_steps)
    gateway = mcp_gateway
    if gateway is None:
        from src.tools.source_selection import select_evidence_sources
        requested = select_evidence_sources(query).requested
        if "runtime" in requested:
            gateway = McpEvidenceGateway.from_qas_runtime_env()
        else:
            gateway = McpEvidenceGateway.from_env()

    retrievals = tuple(
        search_unified(
            client,
            subquery,
            max_results=max_results,
            ref=ref,
            mcp_gateway=gateway,
        )
        for subquery in plan.subqueries
    )
    retrieval = _merge_retrievals(
        query,
        retrievals,
        max_results=max_results,
    )
    evidence = assess_evidence(retrieval)
    reasoning = reason_from_evidence(evidence)
    knowledge_context = build_knowledge_context(
        client,
        query,
        ref=ref,
        direct_retrieval=retrieval,
        max_hops=max_hops,
        mcp_gateway=gateway,
    )

    semantic_evidence = tuple(unified_to_investigation_evidence(item) for item in retrieval.results)
    correlation = correlate_evidence(semantic_evidence)
    contradiction_ids = {evidence_id for pair in correlation.contradictions for evidence_id in pair}
    evidence_states = tuple(
        EvidenceState(
            item.evidence_id,
            "CONFLICTING" if item.evidence_id in contradiction_ids else "AVAILABLE",
            "La evidencia participa en una contradicción estructural." if item.evidence_id in contradiction_ids else "La evidencia fue recuperada y normalizada.",
        )
        for item in semantic_evidence
    )
    hypotheses = build_hypotheses(semantic_evidence, evidence_states, correlation)

    return InvestigationResult(
        query=query.strip(),
        plan=plan,
        retrieval=retrieval,
        evidence=evidence,
        reasoning=reasoning,
        knowledge_context=knowledge_context,
        evidence_states=evidence_states,
        hypotheses=hypotheses,
        correlation=correlation,
    )
