"""SAP Object Workspace orchestration over existing Knowledge Intelligence contracts."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from src.github.client import GitHubClient
from src.sap.qas_runtime import SapQasRuntimeConfig
from src.tools.knowledge_context import KnowledgeContext, build_knowledge_context


SUPPORTED_ENTITY_TYPES = frozenset({"SAP_OBJECT", "TICKET"})


@dataclass(frozen=True)
class ObjectIdentity:
    object_id: str
    object_type: str | None
    display_name: str
    status: str
    match_type: str | None
    score: float | None
    certainty: str
    source_layer: str | None
    path: str | None
    candidates: tuple[dict[str, Any], ...] = ()


@dataclass(frozen=True)
class ObjectWorkspace:
    query: str
    object: dict[str, Any] | None
    identity: ObjectIdentity
    overview: tuple[str, ...]
    relationships: tuple[dict[str, Any], ...]
    dependencies: tuple[dict[str, Any], ...]
    evidence: tuple[dict[str, Any], ...]
    tickets: tuple[dict[str, Any], ...]
    runtime: dict[str, Any]
    gaps: tuple[str, ...]
    conflicts: tuple[dict[str, Any], ...]
    diagnostics: dict[str, Any]


def _normalize(value: str) -> str:
    return " ".join(value.strip().lower().split())


def _candidate_payload(entity: Any) -> dict[str, Any]:
    return {
        "entity_id": entity.entity_id,
        "entity_type": entity.entity_type,
        "path": entity.path,
        "score": entity.score,
        "match_type": entity.match_type,
        "certainty": entity.certainty,
        "source_layer": entity.source_layer,
    }


def _select_identity(
    query: str,
    context: KnowledgeContext,
) -> ObjectIdentity:
    candidates = tuple(
        entity
        for entity in context.entities
        if entity.entity_type in SUPPORTED_ENTITY_TYPES
    )
    normalized_query = _normalize(query)
    exact = tuple(
        entity for entity in candidates
        if _normalize(entity.entity_id) == normalized_query
    )

    if len(exact) == 1:
        entity = exact[0]
        return ObjectIdentity(
            object_id=entity.entity_id,
            object_type=entity.entity_type,
            display_name=entity.entity_id,
            status="resolved",
            match_type="exact",
            score=entity.score,
            certainty=entity.certainty,
            source_layer=entity.source_layer,
            path=entity.path,
            candidates=tuple(_candidate_payload(item) for item in candidates),
        )

    if len(exact) > 1:
        return ObjectIdentity(
            object_id=query.strip(),
            object_type=None,
            display_name=query.strip(),
            status="ambiguous",
            match_type="exact",
            score=None,
            certainty="unknown",
            source_layer=None,
            path=None,
            candidates=tuple(_candidate_payload(item) for item in exact),
        )

    if len(candidates) == 1:
        entity = candidates[0]
        if entity.match_type == "identifier":
            return ObjectIdentity(
                object_id=entity.entity_id,
                object_type=entity.entity_type,
                display_name=entity.entity_id,
                status="resolved",
                match_type=entity.match_type,
                score=entity.score,
                certainty=entity.certainty,
                source_layer=entity.source_layer,
                path=entity.path,
                candidates=tuple(_candidate_payload(item) for item in candidates),
            )
        return ObjectIdentity(
            object_id=query.strip(),
            object_type=None,
            display_name=query.strip(),
            status="unresolved",
            match_type=entity.match_type,
            score=entity.score,
            certainty="unknown",
            source_layer=entity.source_layer,
            path=entity.path,
            candidates=tuple(_candidate_payload(item) for item in candidates),
        )

    if len(candidates) > 1:
        return ObjectIdentity(
            object_id=query.strip(),
            object_type=None,
            display_name=query.strip(),
            status="ambiguous",
            match_type=None,
            score=None,
            certainty="unknown",
            source_layer=None,
            path=None,
            candidates=tuple(_candidate_payload(item) for item in candidates),
        )

    return ObjectIdentity(
        object_id=query.strip(),
        object_type=None,
        display_name=query.strip(),
        status="unresolved",
        match_type=None,
        score=None,
        certainty="unknown",
        source_layer=None,
        path=None,
    )


def _relationship_payload(item: Any) -> dict[str, Any]:
    return {
        **asdict(item.relationship),
        "hop": item.hop,
    }


def _runtime_payload(context: KnowledgeContext) -> dict[str, Any]:
    runtime_items = tuple(
        item for item in context.evidence
        if item.result.knowledge_scope == "runtime"
        or item.result.knowledge_type == "runtime_observation"
    )
    config = SapQasRuntimeConfig.from_env()
    if runtime_items:
        status = "observed"
    elif config.enabled:
        status = "enabled_not_verified"
    else:
        status = "disabled"

    return {
        "status": status,
        "landscape": "QAS",
        "access": "read-only",
        "evidence_count": len(runtime_items),
        "observations": tuple(
            {
                "path": item.result.path,
                "source_id": item.result.source_id,
                "certainty": item.result.certainty,
                "hop": item.hop,
                "discovery": item.discovery,
                "provenance": item.result.provenance,
            }
            for item in runtime_items
        ),
    }


def build_object_workspace(
    client: GitHubClient,
    query: str,
    *,
    ref: str = "main",
    max_results: int = 8,
    max_hops: int = 2,
    mcp_gateway=None,
) -> ObjectWorkspace:
    """Build an auditable SAP object view without introducing new retrieval logic."""
    if not query or not query.strip():
        raise ValueError("object query must not be empty")
    if max_results < 1:
        raise ValueError("max_results must be greater than zero")
    if max_hops < 0:
        raise ValueError("max_hops must be >= 0")

    context = build_knowledge_context(
        client,
        query.strip(),
        ref=ref,
        max_hops=max_hops,
        max_evidence=max_results,
        mcp_gateway=mcp_gateway,
    )
    identity = _select_identity(query, context)

    relationships = tuple(
        _relationship_payload(item)
        for item in context.relationships
        if (
            identity.status == "resolved"
            and (
                item.relationship.source_id.lower() == identity.object_id.lower()
                or item.relationship.target_id.lower() == identity.object_id.lower()
            )
        )
    )

    dependencies = relationships

    tickets = tuple(
        relation
        for relation in relationships
        if relation["source_type"].upper() == "TICKET"
        or relation["target_type"].upper() == "TICKET"
    )

    evidence = tuple(
        {
            "path": item.result.path,
            "score": item.result.score,
            "matched_terms": item.result.matched_terms,
            "source_layer": item.result.source_layer,
            "match_type": item.result.match_type,
            "source_id": item.result.source_id,
            "knowledge_type": item.result.knowledge_type,
            "knowledge_scope": item.result.knowledge_scope,
            "certainty": item.result.certainty,
            "hop": item.hop,
            "discovery": item.discovery,
            "provenance": item.result.provenance,
        }
        for item in context.evidence
    )

    gaps = list(context.gaps)
    if identity.status == "unresolved":
        gaps.append("No existe evidencia suficiente para resolver el objeto solicitado.")
    elif identity.status == "ambiguous":
        gaps.append("La entrada puede representar múltiples entidades soportadas.")

    overview: tuple[str, ...]
    if identity.status == "resolved":
        overview = (
            f"Objeto resuelto: {identity.object_id}.",
            f"Tipo: {identity.object_type}.",
            f"Certainty: {identity.certainty}.",
            f"Capa: {identity.source_layer or 'unknown'}.",
        )
    else:
        overview = (
            f"Estado de identidad: {identity.status}.",
            "No se genera un resumen funcional no respaldado por evidencia.",
        )

    return ObjectWorkspace(
        query=query.strip(),
        object=(
            {
                "id": identity.object_id,
                "type": identity.object_type,
                "display_name": identity.display_name,
                "source_layer": identity.source_layer,
                "certainty": identity.certainty,
                "path": identity.path,
            }
            if identity.status == "resolved"
            else None
        ),
        identity=identity,
        overview=overview,
        relationships=relationships,
        dependencies=dependencies,
        evidence=evidence,
        tickets=tickets,
        runtime=_runtime_payload(context),
        gaps=tuple(dict.fromkeys(gaps)),
        conflicts=tuple(asdict(item) for item in context.conflicts),
        diagnostics={
            "max_hops": context.max_hops,
            "entity_count": len(context.entities),
            "relationship_count": len(context.relationships),
            "evidence_count": len(context.evidence),
            "source_layers": tuple(
                sorted({item.result.source_layer for item in context.evidence})
            ),
            "read_only": True,
        },
    )
