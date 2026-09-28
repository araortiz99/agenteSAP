"""Deterministic SAP entity resolution over repository metadata."""

from __future__ import annotations

from dataclasses import dataclass

from src.github.client import GitHubClient
from src.tools.search_knowledge import SearchResult, _parse_front_matter, search_knowledge
from src.tools.search_sap_standard import search_sap_standard


ENTITY_FIELDS = (
    ("object_id", "SAP_OBJECT"),
    ("process_id", "PROCESS"),
    ("rule_id", "BUSINESS_RULE"),
    ("ticket_id", "TICKET"),
    ("source_id", "SOURCE"),
    ("relationship_id", "RELATIONSHIP"),
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


def _entities_from_result(result: SearchResult) -> tuple[ResolvedEntity, ...]:
    metadata = _parse_front_matter(result.content)
    entities: list[ResolvedEntity] = []

    for field, entity_type in ENTITY_FIELDS:
        entity_id = metadata.get(field, "").strip()
        if not entity_id:
            continue
        entities.append(
            ResolvedEntity(
                entity_id=entity_id,
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
            entity_id=source_id,
            entity_type="SOURCE",
            path=path,
            score=score,
            match_type="content",
            certainty=metadata.get("certainty", "unknown"),
            source_layer="sap_standard",
        ),
    )


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
        key = (entity.entity_type, entity.entity_id.lower())
        current = unique.get(key)
        if current is None or (entity.score, entity.path) > (
            current.score,
            current.path,
        ):
            unique[key] = entity

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
