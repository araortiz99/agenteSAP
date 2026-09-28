"""Evidence evaluation layer for retrieved SAP knowledge."""

from __future__ import annotations

from dataclasses import dataclass
from collections import defaultdict

from src.tools.search_unified import UnifiedResult, UnifiedSearchResult


CERTAINTY_WEIGHT = {
    "confirmed": 1.0,
    "partial": 0.7,
    "under_validation": 0.4,
    "inferred": 0.3,
    "not_confirmed": 0.0,
    "unknown": 0.0,
}

SOURCE_PRIORITY = {
    "sap_standard": 4,
    "internal": 3,
}


@dataclass(frozen=True)
class EvidenceItem:
    path: str
    source_layer: str
    source_id: str | None
    knowledge_type: str
    knowledge_scope: str
    certainty: str
    weight: float
    supports: bool
    reason: str


@dataclass(frozen=True)
class EvidenceAssessment:
    query: str
    items: tuple[EvidenceItem, ...]
    confirmed: tuple[EvidenceItem, ...]
    partial: tuple[EvidenceItem, ...]
    under_validation: tuple[EvidenceItem, ...]
    unsupported: tuple[EvidenceItem, ...]
    conflicts: tuple[str, ...]
    gaps: tuple[str, ...]
    requires_analysis: bool


def _item(result: UnifiedResult) -> EvidenceItem:
    certainty = result.certainty if result.certainty in CERTAINTY_WEIGHT else "unknown"
    weight = CERTAINTY_WEIGHT[certainty] * SOURCE_PRIORITY.get(result.source_layer, 1)
    supports = certainty in {"confirmed", "partial"}
    reason = (
        f"{result.source_layer} evidence with certainty={certainty} "
        f"and source_id={result.source_id or 'unknown'}"
    )
    return EvidenceItem(
        path=result.path,
        source_layer=result.source_layer,
        source_id=result.source_id,
        knowledge_type=result.knowledge_type,
        knowledge_scope=result.knowledge_scope,
        certainty=certainty,
        weight=weight,
        supports=supports,
        reason=reason,
    )


def assess_evidence(retrieval: UnifiedSearchResult) -> EvidenceAssessment:
    """Evaluate provenance and certainty without inventing semantic conclusions."""
    items = tuple(_item(result) for result in retrieval.results)

    confirmed = tuple(x for x in items if x.certainty == "confirmed")
    partial = tuple(x for x in items if x.certainty == "partial")
    under_validation = tuple(x for x in items if x.certainty == "under_validation")
    unsupported = tuple(
        x for x in items if x.certainty in {"inferred", "not_confirmed", "unknown"}
    )

    conflicts: list[str] = []
    by_source: dict[str, set[str]] = defaultdict(set)
    for item in items:
        if item.source_id:
            by_source[item.source_id].add(item.knowledge_type)
    for source_id, types in by_source.items():
        if len(types) > 1:
            conflicts.append(
                f"Source {source_id} has inconsistent knowledge_type values: "
                + ", ".join(sorted(types))
            )

    gaps: list[str] = []
    if not retrieval.sap_standard:
        gaps.append("No SAP Standard evidence was retrieved.")
    if not retrieval.internal:
        gaps.append("No internal evidence was retrieved.")
    if not confirmed:
        gaps.append("No confirmed evidence was retrieved.")

    requires_analysis = bool(
        retrieval.sap_standard and retrieval.internal
    ) and not conflicts

    if retrieval.sap_standard and retrieval.internal:
        gaps.append(
            "Presence of both layers requires functional comparison; "
            "retrieval alone does not establish equivalence or difference."
        )

    return EvidenceAssessment(
        query=retrieval.query,
        items=items,
        confirmed=confirmed,
        partial=partial,
        under_validation=under_validation,
        unsupported=unsupported,
        conflicts=tuple(conflicts),
        gaps=tuple(dict.fromkeys(gaps)),
        requires_analysis=requires_analysis,
    )
