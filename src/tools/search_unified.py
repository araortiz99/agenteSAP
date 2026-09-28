"""Unified retrieval across SAP Standard, internal Knowledge and optional MCP evidence."""

from __future__ import annotations

from dataclasses import dataclass

from src.github.client import GitHubClient
from src.tools.search_knowledge import SearchResult, _parse_front_matter, search_knowledge
from src.tools.search_sap_standard import SAPStandardResult, search_sap_standard
from src.tools.source_selection import EvidenceSource, select_evidence_sources


@dataclass(frozen=True)
class UnifiedResult:
    path: str
    score: float
    matched_terms: tuple[str, ...]
    content: str
    source_layer: str
    match_type: str
    source_id: str | None
    knowledge_type: str
    knowledge_scope: str
    certainty: str
    provenance: tuple[tuple[str, str], ...] = ()


@dataclass(frozen=True)
class UnifiedSearchResult:
    query: str
    results: tuple[UnifiedResult, ...]
    sap_standard: tuple[UnifiedResult, ...]
    internal: tuple[UnifiedResult, ...]
    mcp: tuple[UnifiedResult, ...] = ()


def unified_result_key(result: UnifiedResult) -> tuple[str, str, str, tuple[tuple[str, str], ...]]:
    """Return a provenance-aware identity for a retrieved evidence record."""
    return (
        result.source_layer,
        result.path,
        result.source_id or "",
        tuple(sorted(result.provenance)),
    )


def _evidence_source_id(metadata: dict[str, str]) -> str | None:
    """Return the provenance source without confusing it with entity source_id."""
    return metadata.get("evidence_source_id") or metadata.get("source_id")


def _internal_result(result: SearchResult) -> UnifiedResult:
    metadata = _parse_front_matter(result.content)
    return UnifiedResult(
        path=result.path,
        score=result.score,
        matched_terms=result.matched_terms,
        content=result.content,
        source_layer="internal",
        match_type=result.match_type,
        source_id=_evidence_source_id(metadata),
        knowledge_type=metadata.get("knowledge_type", "unknown"),
        knowledge_scope=metadata.get("knowledge_scope", "unknown"),
        certainty=metadata.get("certainty", "unknown"),
    )


def _standard_result(result: SAPStandardResult) -> UnifiedResult:
    metadata = _parse_front_matter(result.content)
    return UnifiedResult(
        path=result.path,
        score=result.score,
        matched_terms=result.matched_terms,
        content=result.content,
        source_layer="sap_standard",
        match_type="content",
        source_id=_evidence_source_id(metadata),
        knowledge_type=metadata.get("knowledge_type", "standard"),
        knowledge_scope=metadata.get("knowledge_scope", "global"),
        certainty=metadata.get("certainty", "unknown"),
    )


def _merge_evidence_results(
    standard: list[UnifiedResult],
    internal: list[UnifiedResult],
    mcp: list[UnifiedResult],
    *,
    requested: tuple[EvidenceSource, ...],
    max_results: int,
) -> list[UnifiedResult]:
    """Bound retrieval while reserving representation for requested layers."""
    groups = {
        "sap_standard": standard,
        "internal": internal,
        "runtime": [item for item in mcp if item.knowledge_type == "runtime_observation"],
        "external": [item for item in mcp if item.knowledge_type != "runtime_observation"],
    }
    selected: list[UnifiedResult] = []
    seen: set[tuple[str, str, str, tuple[tuple[str, str], ...]]] = set()

    def add(item: UnifiedResult) -> None:
        key = unified_result_key(item)
        if key not in seen and len(selected) < max_results:
            selected.append(item)
            seen.add(key)

    for source in requested:
        for item in groups[source]:
            add(item)
            break

    remaining = sorted(
        standard + internal + mcp,
        key=lambda x: (
            -x.score,
            0 if x.source_layer == "sap_standard"
            else 1 if x.source_layer == "internal"
            else 2,
            x.path,
        ),
    )
    for item in remaining:
        add(item)

    return selected


def search_unified(
    client: GitHubClient,
    query: str,
    *,
    max_results: int = 10,
    ref: str = "main",
    mcp_gateway=None,
) -> UnifiedSearchResult:
    """Retrieve standard, internal and optional MCP evidence without merging their meaning."""
    if not query or not query.strip():
        raise ValueError("query must not be empty")
    if max_results < 1:
        raise ValueError("max_results must be greater than zero")

    standard = [
        _standard_result(x)
        for x in search_sap_standard(client, query, max_results=max_results, ref=ref)
    ]
    internal = [
        _internal_result(x)
        for x in search_knowledge(client, query, max_results=max_results, ref=ref)
    ]
    mcp = list(mcp_gateway.search_resources(query) if mcp_gateway else ())

    selection = select_evidence_sources(query)
    combined = _merge_evidence_results(
        standard,
        internal,
        mcp,
        requested=selection.requested,
        max_results=max_results,
    )

    return UnifiedSearchResult(
        query=query.strip(),
        results=tuple(combined),
        sap_standard=tuple(standard),
        internal=tuple(internal),
        mcp=tuple(mcp),
    )
