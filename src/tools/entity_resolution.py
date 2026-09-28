"""Deterministic SAP entity resolution over repository metadata."""

from __future__ import annotations

from dataclasses import dataclass

from src.github.client import GitHubClient
from src.tools.search_knowledge import SearchResult, _parse_front_matter, search_knowledge
from src.tools.search_sap_standard import search_sap_standard


ENTITY_FIELDS = (
    ("object_id", "SAP_OBJECT"),
    ("object_name", "SAP_OBJECT"),
    ("process_id", "PROCESS"),
    ("rule_id", "BUSINESS_RULE"),
    ("ticket_id", "TICKET"),
    ("source_id", "SOURCE"),
)


@dataclass(frozen=True)
class ResolvedEntity:
    entity_id: str
    entity_type: str
    path: str
    score: float
    match_type: str
    certainty: str
    source_layer: str
    provenance_paths: tuple[str, ...] = ()
    provenance_layers: tuple[str, ...] = ()


def _entities_from_result(result: SearchResult) -> tuple[ResolvedEntity, ...]:
    metadata = _parse_front_matter(result.content)
    entities: list[ResolvedEntity] = []

    for field, entity_type in ENTITY_FIELDS:
        entity_id = metadata.get(field, "").strip()
        if not entity_id:
            continue
        entities.append(
            ResolvedEntity(
                entity_id=_normalize_id(entity_id),
                entity_type=entity_type,
                path=result.path,
                score=result.score,
                match_type=result.match_type,
                certainty=metadata.get("certainty", "unknown"),
                source_layer="internal",
            )
        )

    return tuple(entities)


def _standard_entities(
    path: str,
    content: str,
    score: float,
) -> tuple[ResolvedEntity, ...]:
    metadata = _parse_front_matter(content)
    source_id = metadata.get("source_id", "").strip()
    if not source_id:
        return ()
    return (
        ResolvedEntity(
            entity_id=_normalize_id(source_id),
            entity_type="SOURCE",
            path=path,
            score=score,
            match_type="content",
            certainty=metadata.get("certainty", "unknown"),
            source_layer="sap_standard",
        ),
    )



def _normalize_id(value: str) -> str:
    return " ".join(value.strip().split()).upper()


def _match_rank(match_type: str) -> int:
    return {"exact": 3, "metadata": 3, "content": 2, "path": 1}.get(match_type.lower(), 0)


def _merge_candidate(current: ResolvedEntity | None, candidate: ResolvedEntity) -> ResolvedEntity:
    if current is None:
        return ResolvedEntity(**{**candidate.__dict__, "provenance_paths": (candidate.path,), "provenance_layers": (candidate.source_layer,)})
    paths = tuple(dict.fromkeys((*current.provenance_paths, candidate.path)))
    layers = tuple(dict.fromkeys((*current.provenance_layers, candidate.source_layer)))
    current_rank = (_match_rank(current.match_type), current.score)
    candidate_rank = (_match_rank(candidate.match_type), candidate.score)
    preferred = candidate if candidate_rank > current_rank else current
    return ResolvedEntity(**{**preferred.__dict__, "provenance_paths": paths, "provenance_layers": layers})

def resolve_entities(
    client: GitHubClient,
    query: str,
    *,
    max_entities: int = 8,
    ref: str = "main",
) -> tuple[ResolvedEntity, ...]:
    """Resolve only canonical entities supported by repository metadata."""
    if not query or not query.strip():
        raise ValueError("query must not be empty")
    if max_entities < 1:
        raise ValueError("max_entities must be greater than zero")

    candidates: list[ResolvedEntity] = []

    internal = search_knowledge(
        client, query, max_results=max_entities * 2, ref=ref
    )
    for result in internal:
        candidates.extend(_entities_from_result(result))

    standard = search_sap_standard(
        client, query, max_results=max_entities * 2, ref=ref
    )
    for result in standard:
        candidates.extend(
            _standard_entities(result.path, result.content, result.score)
        )

    unique: dict[tuple[str, str], ResolvedEntity] = {}
    for entity in candidates:
        key = (entity.entity_type.upper(), _normalize_id(entity.entity_id))
        unique[key] = _merge_candidate(unique.get(key), entity)

    return tuple(
        sorted(
            unique.values(),
            key=lambda item: (
                -item.score,
                item.entity_type,
                item.entity_id.lower(),
                item.path,
            ),
        )[:max_entities]
    )
