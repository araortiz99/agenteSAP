"""Documented relationship traversal capability."""

from __future__ import annotations

from dataclasses import dataclass

from src.github.client import GitHubClient


RELATIONSHIP_ROOT = "knowledge/relationships/"


@dataclass(frozen=True)
class Relationship:
    path: str
    source_id: str
    source_type: str
    relation_type: str
    target_id: str
    target_type: str
    content: str
    certainty: str
    status: str
    evidence_source_id: str | None


@dataclass(frozen=True)
class RelatedKnowledge:
    entity_type: str
    entity_id: str
    relationships: tuple[Relationship, ...]


def _normalize(value: str) -> str:
    return value.strip().lower()


def _metadata(content: str) -> dict[str, str]:
    """Parse the simple YAML-like front matter used by repository documents."""
    lines = content.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}

    values: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        values[key.strip()] = value.strip().strip('"')
    return values


def _matches_entity(
    metadata: dict[str, str],
    entity_type: str,
    entity_id: str,
) -> bool:
    requested_type = _normalize(entity_type)
    requested_id = _normalize(entity_id)

    source_type = _normalize(metadata.get("source_type", ""))
    target_type = _normalize(metadata.get("target_type", ""))
    source_id = _normalize(metadata.get("source_id", ""))
    target_id = _normalize(metadata.get("target_id", ""))

    return (
        source_type == requested_type
        and source_id == requested_id
    ) or (
        target_type == requested_type
        and target_id == requested_id
    )


def get_related_knowledge(
    client: GitHubClient,
    entity_type: str,
    entity_id: str,
    ref: str = "main",
) -> RelatedKnowledge:
    """Return only explicitly documented relationships for an entity."""

    if not entity_type.strip():
        raise ValueError("entity_type must not be empty")

    if not entity_id.strip():
        raise ValueError("entity_id must not be empty")

    tree = client.get_tree(ref=ref)
    relationships: list[Relationship] = []

    for item in tree:
        path = item.get("path", "")
        if not (
            path.startswith(RELATIONSHIP_ROOT)
            and path.endswith(".md")
            and item.get("type") == "blob"
        ):
            continue

        content = client.get_file(path, ref=ref)
        metadata = _metadata(content)

        if not _matches_entity(metadata, entity_type, entity_id):
            continue

        relationships.append(
            Relationship(
                path=path,
                source_id=metadata.get("source_id", ""),
                source_type=metadata.get("source_type", ""),
                relation_type=metadata.get("relation_type", ""),
                target_id=metadata.get("target_id", ""),
                target_type=metadata.get("target_type", ""),
                content=content,
                certainty=metadata.get("certainty", "unknown"),
                status=metadata.get("status", "unknown"),
                evidence_source_id=metadata.get("evidence_source_id"),
            )
        )

    relationships.sort(key=lambda relationship: relationship.path)

    return RelatedKnowledge(
        entity_type=entity_type.strip(),
        entity_id=entity_id.strip(),
        relationships=tuple(relationships),
    )
