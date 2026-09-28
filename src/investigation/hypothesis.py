"""Deterministic hypothesis generation over explicit evidence states."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from src.investigation.contracts import InvestigationEvidence
from src.investigation.correlation import EvidenceCorrelation
from src.investigation.evidence_state import EvidenceState


HYPOTHESIS_STATUSES = frozenset(
    {"SUPPORTED", "PARTIALLY_SUPPORTED", "CONTRADICTED", "UNVERIFIED"}
)


@dataclass(frozen=True)
class Hypothesis:
    hypothesis_id: str
    statement: str
    status: str
    evidence_ids: tuple[str, ...] = ()
    reason: str = ""

    def __post_init__(self) -> None:
        if self.status not in HYPOTHESIS_STATUSES:
            raise ValueError(f"unsupported hypothesis status: {self.status}")


def _status_for(
    evidence_ids: tuple[str, ...],
    states: dict[str, EvidenceState],
    evidence: dict[str, InvestigationEvidence],
    correlation: EvidenceCorrelation,
) -> tuple[str, str]:
    if any(
        pair[0] in evidence_ids and pair[1] in evidence_ids
        for pair in correlation.contradictions
    ):
        return "CONTRADICTED", "La evidencia correlacionada contiene una contradicción explícita."

    available = [
        states[evidence_id]
        for evidence_id in evidence_ids
        if evidence_id in states
    ]
    records = [
        evidence[evidence_id]
        for evidence_id in evidence_ids
        if evidence_id in evidence
    ]
    if not available:
        return "UNVERIFIED", "No existe evidencia vinculada suficiente para evaluar la hipótesis."
    if all(item.state == "AVAILABLE" for item in available) and all(
        item.certainty in {"confirmed", "partial"} for item in records
    ):
        return "SUPPORTED", "Toda la evidencia vinculada está disponible, sin conflicto y con certeza suficiente."
    if all(item.state == "AVAILABLE" for item in available):
        return "PARTIALLY_SUPPORTED", "La evidencia está disponible, pero su certeza no permite tratar la hipótesis como confirmada."
    if any(item.state in {"MISSING", "INSUFFICIENT", "INVALID"} for item in available):
        return "PARTIALLY_SUPPORTED", "Existe evidencia disponible, pero también faltan o son insuficientes elementos necesarios."
    return "UNVERIFIED", "La evidencia vinculada no permite verificar la hipótesis."


def build_hypotheses(
    evidence: Iterable[InvestigationEvidence],
    states: Iterable[EvidenceState],
    correlation: EvidenceCorrelation,
) -> tuple[Hypothesis, ...]:
    """Generate bounded hypotheses only from explicit observations.

    Correlation can support a hypothesis, but never by itself proves root cause.
    """
    items = tuple(evidence)
    state_map = {item.evidence_id or "": item for item in states}
    evidence_map = {item.evidence_id: item for item in items}
    result: list[Hypothesis] = []

    movement_ids = tuple(
        item.evidence_id
        for item in items
        if "movement" in item.observation_type.lower()
    )
    stock_ids = tuple(
        item.evidence_id
        for item in items
        if any(token in item.observation_type.lower() for token in ("stock", "quantity"))
    )

    if movement_ids and stock_ids:
        linked = tuple(
            dict.fromkeys(
                [
                    relation.source_evidence_id
                    for relation in correlation.relations
                    if relation.relation == "explains"
                ]
                + [
                    relation.target_evidence_id
                    for relation in correlation.relations
                    if relation.relation == "explains"
                ]
            )
        )
        ids = linked or tuple(dict.fromkeys(movement_ids + stock_ids))
        status, reason = _status_for(ids, state_map, evidence_map, correlation)
        result.append(
            Hypothesis(
                hypothesis_id="HYP-MOVEMENT-STOCK",
                statement=(
                    "La diferencia observada puede estar relacionada con movimientos "
                    "que afectan el stock de la misma entidad."
                ),
                status=status,
                evidence_ids=ids,
                reason=reason
                + " La correlación movimiento-stock no constituye por sí sola una causa raíz.",
            )
        )

    if correlation.contradictions:
        ids = tuple(
            dict.fromkeys(
                evidence_id
                for pair in correlation.contradictions
                for evidence_id in pair
            )
        )
        result.append(
            Hypothesis(
                hypothesis_id="HYP-CONFLICTING-OBSERVATIONS",
                statement="Existen observaciones incompatibles que requieren validación funcional antes de concluir.",
                status="CONTRADICTED",
                evidence_ids=ids,
                reason="La correlación identificó contradicciones explícitas entre observaciones de la misma entidad.",
            )
        )

    if not result:
        result.append(
            Hypothesis(
                hypothesis_id="HYP-INSUFFICIENT-EVIDENCE",
                statement="La evidencia disponible no permite establecer todavía una explicación funcional verificable.",
                status="UNVERIFIED",
                evidence_ids=tuple(item.evidence_id for item in items),
                reason="No se identificó una relación de evidencia suficiente para evaluar una hipótesis específica.",
            )
        )

    return tuple(result)
