"""Deterministic, bounded correlation of investigation evidence.

This module deliberately performs structural correlation only. It does not
infer root cause, invoke an LLM, or choose which conflicting observation is true.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
from typing import Any

from src.investigation.contracts import InvestigationEvidence


_ALLOWED_RELATIONS = frozenset({"supports", "explains", "contradicts", "related_to"})


@dataclass(frozen=True)
class EvidenceRelation:
    source_evidence_id: str
    target_evidence_id: str
    relation: str
    certainty: str
    reason: str

    def __post_init__(self) -> None:
        if self.relation not in _ALLOWED_RELATIONS:
            raise ValueError(f"unsupported evidence relation: {self.relation}")
        if self.source_evidence_id == self.target_evidence_id:
            raise ValueError("evidence relation cannot target itself")


@dataclass(frozen=True)
class EvidenceCorrelation:
    evidence_ids: tuple[str, ...] = ()
    relations: tuple[EvidenceRelation, ...] = ()
    contradictions: tuple[tuple[str, str], ...] = ()
    gaps: tuple[str, ...] = ()
    unresolved_relationships: tuple[str, ...] = ()

    def as_dict(self) -> dict[str, Any]:
        return {
            "evidence_ids": list(self.evidence_ids),
            "relations": [
                {
                    "source_evidence_id": item.source_evidence_id,
                    "target_evidence_id": item.target_evidence_id,
                    "relation": item.relation,
                    "certainty": item.certainty,
                    "reason": item.reason,
                }
                for item in self.relations
            ],
            "contradictions": [list(item) for item in self.contradictions],
            "gaps": list(self.gaps),
            "unresolved_relationships": list(self.unresolved_relationships),
        }


def _structured_content(content: str) -> Any:
    if not isinstance(content, str):
        return None
    try:
        return json.loads(content)
    except (TypeError, json.JSONDecodeError):
        return None


def _flatten(value: Any, prefix: str = "") -> dict[str, Any]:
    if isinstance(value, dict):
        result: dict[str, Any] = {}
        for key, child in value.items():
            path = f"{prefix}.{key}" if prefix else str(key)
            if isinstance(child, (dict, list)):
                result.update(_flatten(child, path))
            else:
                result[path.lower()] = child
        return result
    if isinstance(value, list):
        result = {}
        for index, child in enumerate(value):
            result.update(_flatten(child, f"{prefix}[{index}]"))
        return result
    return {prefix.lower(): value} if prefix else {}


def _field(values: dict[str, Any], names: tuple[str, ...]) -> Any:
    for key, value in values.items():
        normalized = key.split(".")[-1].lower()
        if normalized in names:
            return value
    return None


def _identity(evidence: InvestigationEvidence) -> dict[str, Any]:
    values = _flatten(_structured_content(evidence.content))
    return {
        "material": _field(values, ("material", "matnr", "material_number")),
        "plant": _field(values, ("plant", "center", "centro", "werks")),
        "document": _field(values, ("material_document", "materialdocument", "mblnr", "document")),
        "object": evidence.object_id,
        "object_type": evidence.object_type,
    }


def _observations(evidence: InvestigationEvidence) -> dict[str, Any]:
    values = _flatten(_structured_content(evidence.content))
    return {
        "stock": _field(values, ("stock", "quantity", "qty", "labst", "unrestricted_stock")),
        "movement_quantity": _field(values, ("movement_quantity", "movement_qty", "menge")),
    }


def _same_entity(left: dict[str, Any], right: dict[str, Any]) -> tuple[bool, list[str]]:
    if left.get("material") is not None and right.get("material") is not None and str(left["material"]) != str(right["material"]):
        return False, []
    if left.get("plant") is not None and right.get("plant") is not None and str(left["plant"]) != str(right["plant"]):
        return False, []

    if (
        left.get("material") is not None
        and right.get("material") is not None
        and left.get("plant") is not None
        and right.get("plant") is not None
        and str(left["material"]) == str(right["material"])
        and str(left["plant"]) == str(right["plant"])
    ):
        return True, ["material", "plant"]

    if (
        left.get("document") is not None
        and right.get("document") is not None
        and str(left["document"]) == str(right["document"])
    ):
        return True, ["document"]

    if (
        left.get("object") is not None
        and right.get("object") is not None
        and str(left["object"]) == str(right["object"])
        and str(left.get("object_type")) == str(right.get("object_type"))
    ):
        return True, ["object"]

    return False, []


def correlate_evidence(
    evidence: tuple[InvestigationEvidence, ...] | list[InvestigationEvidence],
) -> EvidenceCorrelation:
    """Correlate evidence using explicit structural rules only.

    Pair evaluation is O(n²) and bounded by the evidence supplied by the
    investigation engine. No external state, timestamps, randomness, or LLM
    calls are involved.
    """
    items = tuple(evidence)
    ids = tuple(item.evidence_id for item in items)
    relations: list[EvidenceRelation] = []
    contradictions: list[tuple[str, str]] = []
    gaps: list[str] = []
    unresolved: list[str] = []

    duplicate_ids = sorted({evidence_id for evidence_id in ids if ids.count(evidence_id) > 1})
    if duplicate_ids:
        gaps.append("duplicate_evidence_id")
        unresolved.append("Se detectaron IDs de evidencia duplicados; las relaciones entre esos registros se omiten para preservar la trazabilidad.")

    for index, left in enumerate(items):
        left_identity = _identity(left)
        left_observations = _observations(left)
        for right in items[index + 1 :]:
            if left.evidence_id == right.evidence_id:
                continue
            right_identity = _identity(right)
            right_observations = _observations(right)
            same_entity, shared = _same_entity(left_identity, right_identity)
            if not same_entity:
                continue

            left_stock = left_observations.get("stock")
            right_stock = right_observations.get("stock")
            if (
                left_stock is not None
                and right_stock is not None
                and str(left_stock) != str(right_stock)
                and "material" in shared
                and "plant" in shared
            ):
                contradictions.append((left.evidence_id, right.evidence_id))
                relations.append(
                    EvidenceRelation(
                        left.evidence_id,
                        right.evidence_id,
                        "contradicts",
                        "high",
                        "Las evidencias identifican la misma entidad y reportan valores de stock incompatibles.",
                    )
                )
                continue

            movement_left = left.observation_type.lower().find("movement") >= 0
            movement_right = right.observation_type.lower().find("movement") >= 0
            stock_left = left_stock is not None
            stock_right = right_stock is not None
            if (movement_left and stock_right) or (movement_right and stock_left):
                movement = left if movement_left else right
                stock = right if movement_left else left
                relations.append(
                    EvidenceRelation(
                        movement.evidence_id,
                        stock.evidence_id,
                        "explains",
                        "medium",
                        "Una evidencia identifica movimiento y la otra observa stock para la misma entidad.",
                    )
                )
                continue

            relations.append(
                EvidenceRelation(
                    left.evidence_id,
                    right.evidence_id,
                    "related_to",
                    "medium",
                    "Las evidencias comparten una entidad funcional explícita: " + ", ".join(shared) + ".",
                )
            )

    structured = sum(_structured_content(item.content) is not None for item in items)
    if len(items) >= 2 and structured < 2:
        gaps.append("structured_fields_missing_for_correlation")
        unresolved.append("No se pudo evaluar toda la evidencia no estructurada de forma segura.")

    return EvidenceCorrelation(
        evidence_ids=ids,
        relations=tuple(relations),
        contradictions=tuple(contradictions),
        gaps=tuple(gaps),
        unresolved_relationships=tuple(unresolved),
    )
