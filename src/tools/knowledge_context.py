"""Knowledge Intelligence Layer: entity, relationship and multi-hop context."""

from __future__ import annotations

from dataclasses import dataclass

from src.github.client import GitHubClient
from src.tools.entity_resolution import ResolvedEntity, resolve_entities
from src.tools.evidence import ConflictRecord, assess_evidence
from src.tools.get_related_knowledge import Relationship, get_related_knowledge
from src.tools.search_unified import UnifiedResult, UnifiedSearchResult, search_unified


@dataclass(frozen=True)
class ContextRelationship:
    relationship: Relationship
    hop: int



@dataclass(frozen=True)
class ContextEvidence:
    result: UnifiedResult
    hop: int
    discovery: str


@dataclass(frozen=True)
class KnowledgeContext:
    query: str
    entities: tuple[ResolvedEntity, ...]
    relationships: tuple[ContextRelationship, ...]
    evidence: tuple[ContextEvidence, ...]
    gaps: tuple[str, ...]
    conflicts: tuple[ConflictRecord, ...]
    max_hops: int


def _relationship_key(
    relation: Relationship,
) -> tuple[str, str, str, str, str]:
    return (
        relation.source_type.lower(),
        relation.source_id.lower(),
        relation.relation_type.lower(),
        relation.target_type.lower(),
        relation.target_id.lower(),
    )


def _entity_key(entity_type: str, entity_id: str) -> tuple[str, str]:
    return entity_type.lower(), entity_id.lower()


def _add_relationship(
    relations: dict[tuple[str, str, str, str, str], ContextRelationship],
    relation: Relationship,
    hop: int,
) -> None:
    key = _relationship_key(relation)
    existing = relations.get(key)
    if existing is None or hop < existing.hop:
        relations[key] = ContextRelationship(relationship=relation, hop=hop)


def _related_results(
    client: GitHubClient,
    entity: ResolvedEntity,
    *,
    hop: int,
    max_results: int,
    ref: str,
    mcp_gateway=None,
) -> tuple[ContextEvidence, ...]:
    retrieved = search_unified(
        client,
        entity.entity_id,
        max_results=max_results,
        ref=ref,
        mcp_gateway=mcp_gateway,
    )
    return tuple(
        ContextEvidence(result=result, hop=hop, discovery="relationship")
        for result in retrieved.results
    )


def build_knowledge_context(
    client: GitHubClient,
    query: str,
    *,
    max_hops: int = 2,
    max_entities: int = 8,
    max_relationships: int = 16,
    max_evidence: int = 12,
    ref: str = "main",
    direct_retrieval: UnifiedSearchResult | None = None,
    mcp_gateway=None,
) -> KnowledgeContext:
    """Build a bounded, provenance-preserving knowledge context."""
    if not query or not query.strip():
        raise ValueError("query must not be empty")
    if max_hops < 0:
        raise ValueError("max_hops must be >= 0")
    if max_entities < 1 or max_relationships < 1 or max_evidence < 1:
        raise ValueError("context limits must be greater than zero")

    entities = resolve_entities(
        client,
        query,
        max_entities=max_entities,
        ref=ref,
    )

    direct = direct_retrieval or search_unified(
        client,
        query,
        max_results=max_evidence,
        ref=ref,
        mcp_gateway=mcp_gateway,
    )

    evidence: dict[str, ContextEvidence] = {
        result.path: ContextEvidence(result=result, hop=0, discovery="direct")
        for result in direct.results
    }

    relations: dict[tuple[str, str, str, str, str], ContextRelationship] = {}
    visited = {
        _entity_key(entity.entity_type, entity.entity_id)
        for entity in entities
    }
    frontier = list(entities)
    gaps: list[str] = []

    for hop in range(1, max_hops + 1):
        if not frontier:
            break

        next_frontier: list[ResolvedEntity] = []

        for entity in frontier:
            related = get_related_knowledge(
                client,
                entity.entity_type,
                entity.entity_id,
                ref=ref,
            )

            for relation in related.relationships:
                key = _relationship_key(relation)
                if len(relations) >= max_relationships and key not in relations:
                    continue

                _add_relationship(relations, relation, hop)

                entity_key = _entity_key(entity.entity_type, entity.entity_id)
                source_key = _entity_key(
                    relation.source_type,
                    relation.source_id,
                )
                target_key = _entity_key(
                    relation.target_type,
                    relation.target_id,
                )

                if source_key == entity_key:
                    candidate_type, candidate_id = (
                        relation.target_type,
                        relation.target_id,
                    )
                elif target_key == entity_key:
                    candidate_type, candidate_id = (
                        relation.source_type,
                        relation.source_id,
                    )
                else:
                    continue

                candidate_key = _entity_key(candidate_type, candidate_id)

                # The relationship itself is explicit and therefore confirmed
                # as a relationship. The entity's own certainty is not upgraded.
                candidate = ResolvedEntity(
                    entity_id=candidate_id,
                    entity_type=candidate_type,
                    path=relation.path,
                    score=1.0 / hop,
                    match_type="relationship",
                    certainty="unknown",
                    source_layer="internal",
                )

                if candidate_key not in visited:
                    visited.add(candidate_key)
                    next_frontier.append(candidate)

                if len(evidence) < max_evidence:
                    for context_evidence in _related_results(
                        client,
                        candidate,
                        hop=hop,
                        max_results=max(1, max_evidence - len(evidence)),
                        ref=ref,
                        mcp_gateway=mcp_gateway,
                    ):
                        existing = evidence.get(context_evidence.result.path)
                        if existing is None or context_evidence.hop < existing.hop:
                            evidence[context_evidence.result.path] = context_evidence
                        if len(evidence) >= max_evidence:
                            break

                if len(relations) >= max_relationships:
                    break

            if len(relations) >= max_relationships:
                break

        frontier = next_frontier

    if not entities:
        gaps.append("No canonical repository entity was resolved from the query.")

    if max_hops == 0:
        gaps.append("Relationship traversal disabled by max_hops=0.")

    ordered_evidence = sorted(
        evidence.values(),
        key=lambda item: (
            item.hop,
            -item.result.score,
            0 if item.result.source_layer == "sap_standard" else 1,
            item.result.path,
        ),
    )[:max_evidence]

    evidence_results = tuple(item.result for item in ordered_evidence)
    assessment = assess_evidence(
        UnifiedSearchResult(
            query=query.strip(),
            results=evidence_results,
            sap_standard=tuple(
                item for item in evidence_results
                if item.source_layer == "sap_standard"
            ),
            internal=tuple(
                item for item in evidence_results
                if item.source_layer == "internal"
            ),
            mcp=tuple(
                item for item in evidence_results
                if item.source_layer == "mcp"
            ),
        )
    )

    return KnowledgeContext(
        query=query.strip(),
        entities=entities,
        relationships=tuple(
            sorted(
                relations.values(),
                key=lambda item: (item.hop, item.relationship.path),
            )
        ),
        evidence=tuple(ordered_evidence),
        gaps=tuple(dict.fromkeys((*gaps, *assessment.gaps))),
        conflicts=assessment.conflicts,
        max_hops=max_hops,
    )


def render_knowledge_context(
    context: KnowledgeContext,
    *,
    content_limit: int = 2200,
) -> str:
    """Render deterministic context for an LLM without changing provenance."""
    lines = [
        "## Knowledge Intelligence Context",
        f"Query: {context.query}",
        f"Max hops: {context.max_hops}",
        "",
        "### Entities",
    ]

    for entity in context.entities:
        lines.append(
            f"- {entity.entity_type}:{entity.entity_id} "
            f"(score={entity.score:.3f}, match={entity.match_type}, "
            f"certainty={entity.certainty}, path={entity.path})"
        )

    lines.extend(["", "### Relationships"])
    for item in context.relationships:
        relation = item.relationship
        lines.append(
            f"- hop={item.hop} {relation.source_type}:{relation.source_id} "
            f"--{relation.relation_type}--> "
            f"{relation.target_type}:{relation.target_id} "
            f"(certainty={relation.certainty}, status={relation.status}, "
            f"path={relation.path})"
        )

    lines.extend(["", "### Evidence"])
    for item in context.evidence:
        result = item.result
        content = result.content.strip()
        if len(content) > content_limit:
            content = content[:content_limit].rstrip() + "\n[contenido truncado]"
        lines.extend(
            [
                "",
                f"- path: {result.path}",
                f"  hop: {item.hop}",
                f"  discovery: {item.discovery}",
                f"  source_layer: {result.source_layer}",
                f"  source_id: {result.source_id or 'unknown'}",
                f"  knowledge_type: {result.knowledge_type}",
                f"  knowledge_scope: {result.knowledge_scope}",
                f"  certainty: {result.certainty}",
                f"  score: {result.score:.3f}",
                "  content:",
                content,
            ]
        )

    lines.extend(["", "### Gaps"])
    lines.extend(f"- {gap}" for gap in context.gaps)

    lines.extend(["", "### Conflicts"])
    for conflict in context.conflicts:
        lines.extend(
            [
                f"- type: {conflict.conflict_type}",
                f"  status: {conflict.status}",
                f"  description: {conflict.description}",
                "  evidence_paths:",
                *[f"    - {path}" for path in conflict.evidence_paths],
            ]
        )

    return "\n".join(lines)
