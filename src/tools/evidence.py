"""Evidence evaluation layer for retrieved SAP knowledge."""

from __future__ import annotations

from dataclasses import dataclass
from collections import defaultdict
import re

from src.tools.search_unified import UnifiedResult, UnifiedSearchResult
from src.tools.source_selection import select_evidence_sources


CERTAINTY_WEIGHT = {
    "confirmed": 1.0,
    "partial": 0.7,
    "under_validation": 0.4,
    "inferred": 0.3,
    "not_confirmed": 0.0,
    "unknown": 0.0,
    # External provider provenance is not equivalent to repository-confirmed
    # knowledge. It receives a bounded weight but cannot support a confirmed
    # conclusion unless corroborated by stronger evidence.
    "external_source": 0.4,
}

SOURCE_PRIORITY = {
    "sap_standard": 4,
    "internal": 3,
    # MCP developer context is external evidence: useful and traceable,
    # but intentionally weighted below repository-owned evidence.
    "mcp": 2,
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
    provenance: tuple[tuple[str, str], ...] = ()


@dataclass(frozen=True)
class ConflictRecord:
    conflict_type: str
    status: str
    description: str
    evidence_paths: tuple[str, ...]


@dataclass(frozen=True)
class EvidenceAssessment:
    query: str
    items: tuple[EvidenceItem, ...]
    confirmed: tuple[EvidenceItem, ...]
    partial: tuple[EvidenceItem, ...]
    under_validation: tuple[EvidenceItem, ...]
    unsupported: tuple[EvidenceItem, ...]
    conflicts: tuple[ConflictRecord, ...]
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
        provenance=result.provenance,
    )


def _conflict_section(content: str) -> str:
    """Extract an explicit Markdown conflict section, if present."""
    match = re.search(
        r"(?ims)^##\s+(?:\d+[.)]\s*)?(?:Conflictos|Contradicciones|Discrepancias)\s*$"
        r"(.*?)(?=^##\s+|\Z)",
        content,
    )
    return match.group(1).strip() if match else ""


def _explicit_conflict_records(
    results: tuple[UnifiedResult, ...],
) -> tuple[ConflictRecord, ...]:
    """Detect only contradictions explicitly declared by retrieved evidence."""
    candidates: dict[tuple[str | None, str], list[str]] = defaultdict(list)

    for result in results:
        section = _conflict_section(result.content)
        if not section:
            continue

        # A dedicated conflict/contradiction/discrepancy section is
        # itself explicit documentation of unresolved conflict. Do not infer
        # conflicts merely from terms appearing elsewhere in a document.
        lowered = section.lower()
        marker = bool(section.strip()) or any(
            token in lowered
            for token in (
                "contradic",
                "discrep",
                "conflict",
                "no resuelve",
                "pendiente de validación",
                "pendiente de validar",
            )
        )
        if not marker:
            continue

        scenarios = tuple(dict.fromkeys(re.findall(r"\bK\d+\b", result.content, re.IGNORECASE)))
        key = (result.source_id, "|".join(sorted(s.upper() for s in scenarios)))
        candidates[key].append(result.path)

    records: list[ConflictRecord] = []
    for (source_id, scenarios), paths in candidates.items():
        scenario_text = (
            f" Escenarios explícitamente mencionados: {scenarios.replace('|', ', ')}."
            if scenarios
            else ""
        )
        source_text = source_id or "fuente no identificada"
        description = (
            f"La fuente {source_text} documenta explícitamente una contradicción o "
            f"discrepancia no resuelta en la evidencia recuperada.{scenario_text}"
        )
        records.append(
            ConflictRecord(
                conflict_type="explicit_documented_conflict",
                status="requires_analysis",
                description=description,
                evidence_paths=tuple(dict.fromkeys(paths)),
            )
        )

    return tuple(records)


def assess_evidence(retrieval: UnifiedSearchResult) -> EvidenceAssessment:
    """Evaluate provenance, certainty and explicitly documented conflicts."""
    items = tuple(_item(result) for result in retrieval.results)

    confirmed = tuple(x for x in items if x.certainty == "confirmed")
    partial = tuple(x for x in items if x.certainty == "partial")
    under_validation = tuple(x for x in items if x.certainty == "under_validation")
    unsupported = tuple(
        x for x in items if x.certainty in {"inferred", "not_confirmed", "unknown"}
    )

    conflicts: list[ConflictRecord] = []

    by_source: dict[str, set[str]] = defaultdict(set)
    source_paths: dict[str, list[str]] = defaultdict(list)
    for item in items:
        if item.source_id:
            by_source[item.source_id].add(item.knowledge_type)
            source_paths[item.source_id].append(item.path)

    for source_id, types in by_source.items():
        if len(types) > 1:
            conflicts.append(
                ConflictRecord(
                    conflict_type="metadata_conflict",
                    status="requires_analysis",
                    description=(
                        f"Source {source_id} has inconsistent knowledge_type values: "
                        + ", ".join(sorted(types))
                    ),
                    evidence_paths=tuple(dict.fromkeys(source_paths[source_id])),
                )
            )

    conflicts.extend(_explicit_conflict_records(retrieval.results))

    # Deduplicate equivalent conflict records deterministically.
    unique_conflicts: dict[tuple[str, str, tuple[str, ...]], ConflictRecord] = {}
    for conflict in conflicts:
        key = (
            conflict.conflict_type,
            conflict.description,
            conflict.evidence_paths,
        )
        unique_conflicts[key] = conflict
    conflicts = list(unique_conflicts.values())

    gaps: list[str] = []
    selection = select_evidence_sources(retrieval.query)
    selected = set(selection.requested)

    retrieved_layers = {item.source_layer for item in items}

    if "sap_standard" in selected and "sap_standard" not in retrieved_layers:
        gaps.append("No SAP Standard evidence was retrieved.")
        gaps.append(
            "Source-selection policy: SAP Standard evidence is expected for this query."
        )
    if "internal" in selected and "internal" not in retrieved_layers:
        gaps.append("No internal evidence was retrieved.")
        gaps.append(
            "Source-selection policy: internal implementation evidence is expected for this query."
        )
    if "runtime" in selected and not any(
        item.knowledge_type == "runtime_observation" for item in items
    ):
        gaps.append(
            "The query asks about current/runtime state, but no runtime observation was retrieved."
        )
    if not confirmed:
        gaps.append("No confirmed evidence was retrieved.")

    has_standard = "sap_standard" in retrieved_layers
    has_internal = "internal" in retrieved_layers
    # Any explicit or metadata conflict is a hard governance signal. A
    # mixed-layer comparison also requires analysis, but conflicts must never
    # downgrade that state back to False.
    requires_analysis = bool(conflicts) or (has_standard and has_internal)

    if has_standard and has_internal:
        gaps.append(
            "Presence of both layers requires functional comparison; "
            "retrieval alone does not establish equivalence or difference."
        )

    if conflicts:
        gaps.append(
            "One or more explicit evidence conflicts require functional validation "
            "before a definitive conclusion."
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
