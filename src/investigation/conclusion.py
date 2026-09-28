"""Deterministic conclusion gate for bounded SAP investigations.

The gate converts evidence state + hypothesis status into a qualified conclusion.
It never promotes correlation to root cause and never treats missing evidence as
proof of absence.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from src.investigation.evidence_state import EvidenceState
from src.investigation.hypothesis import Hypothesis


CONCLUSION_STATUSES = frozenset(
    {"CONFIRMED", "QUALIFIED", "BLOCKED", "UNVERIFIED"}
)


@dataclass(frozen=True)
class ConclusionDecision:
    status: str
    statement: str
    reason: str
    evidence_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if self.status not in CONCLUSION_STATUSES:
            raise ValueError(f"unsupported conclusion status: {self.status}")


def build_conclusion(
    hypotheses: Iterable[Hypothesis],
    evidence_states: Iterable[EvidenceState],
    *,
    missing: Iterable[str] = (),
) -> ConclusionDecision:
    """Apply a fail-closed conclusion policy to explicit semantic contracts."""
    hypotheses = tuple(hypotheses)
    states = tuple(evidence_states)
    missing = tuple(dict.fromkeys(missing))
    state_map = {item.evidence_id: item.state for item in states if item.evidence_id}

    if any(item.state in {"CONFLICTING", "INVALID"} for item in states):
        ids = tuple(
            item.evidence_id for item in states
            if item.evidence_id and item.state in {"CONFLICTING", "INVALID"}
        )
        return ConclusionDecision(
            "BLOCKED",
            "No se puede establecer una conclusión funcional porque existe evidencia en conflicto o inválida.",
            "La política de cierre bloquea conclusiones cuando la evidencia no es consistente.",
            ids,
        )

    supported = tuple(item for item in hypotheses if item.status == "SUPPORTED")
    supported_complete = tuple(
        item for item in supported
        if item.evidence_ids and all(state_map.get(evidence_id) == "AVAILABLE" for evidence_id in item.evidence_ids)
    )
    supported_unresolved = tuple(item for item in supported if item not in supported_complete)
    partial = tuple(item for item in hypotheses if item.status == "PARTIALLY_SUPPORTED")
    contradicted = tuple(item for item in hypotheses if item.status == "CONTRADICTED")

    if contradicted:
        ids = tuple(dict.fromkeys(
            evidence_id
            for item in contradicted
            for evidence_id in item.evidence_ids
        ))
        return ConclusionDecision(
            "BLOCKED",
            "Las hipótesis disponibles contienen contradicciones explícitas y requieren validación funcional antes de cerrar.",
            "Una hipótesis contradicha no puede convertirse en conclusión.",
            ids,
        )

    if supported_unresolved and not missing:
        ids = tuple(dict.fromkeys(
            evidence_id
            for item in supported_unresolved
            for evidence_id in item.evidence_ids
        ))
        return ConclusionDecision(
            "QUALIFIED",
            "La hipótesis está marcada como soportada, pero no todas sus evidencias tienen un estado AVAILABLE explícito; se requiere validación adicional.",
            "El gate de evidencia impide elevar una hipótesis a CONFIRMED sin estados AVAILABLE para todas sus evidencias.",
            ids,
        )

    if missing:
        ids = tuple(dict.fromkeys(
            evidence_id
            for item in (*supported_complete, *partial)
            for evidence_id in item.evidence_ids
            if state_map.get(evidence_id) == "AVAILABLE"
        ))
        return ConclusionDecision(
            "QUALIFIED" if supported_complete or partial else "UNVERIFIED",
            (
                "La evidencia disponible permite una conclusión acotada, pero faltan "
                "datos requeridos para afirmar una causa raíz."
                if supported or partial
                else "No existe evidencia suficiente para establecer una conclusión funcional."
            ),
            "Persisten requisitos de evidencia no obtenidos: " + ", ".join(missing),
            ids,
        )

    if supported_complete:
        item = supported_complete[0]
        return ConclusionDecision(
            "CONFIRMED",
            (
                "La evidencia disponible respalda la relación funcional indicada por la "
                "hipótesis, sin convertir esa relación en una afirmación de causa raíz."
            ),
            item.reason,
            item.evidence_ids,
        )

    if partial:
        item = partial[0]
        return ConclusionDecision(
            "QUALIFIED",
            "La evidencia permite una interpretación funcional parcial, pero no una conclusión confirmada.",
            item.reason,
            item.evidence_ids,
        )

    return ConclusionDecision(
        "UNVERIFIED",
        "No se puede establecer una explicación funcional verificable con la evidencia disponible.",
        "No existe una hipótesis soportada ni evidencia suficiente para cerrar la investigación.",
    )
