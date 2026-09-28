"""Deterministic source-selection policy for evidence retrieval."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


EvidenceSource = Literal["sap_standard", "internal", "runtime", "external"]


@dataclass(frozen=True)
class SourceSelection:
    """What evidence layer is relevant to the user's question."""

    requested: tuple[EvidenceSource, ...]
    rationale: tuple[str, ...]


_RUNTIME_MARKERS = (
    "actualmente",
    "ahora",
    "en qas",
    "en prd",
    "en producción",
    "en produccion",
    "en sap",
    "estado actual",
    "valor actual",
    "qué tiene configurado",
    "que tiene configurado",
    "qué está configurado",
    "que esta configurado",
    "ejecutar",
    "ejecución",
    "ejecucion",
)

_STANDARD_MARKERS = (
    "sap standard",
    "sap estándar",
    "estándar",
    "estandar",
    "help.sap",
    "cómo funciona estándar",
    "como funciona estandar",
)

_INTERNAL_MARKERS = (
    "nuestra implementación",
    "nuestra implementacion",
    "custom",
    "desarrollo z",
    "objeto z",
    "ticket",
    "incidente",
    "nuestro proceso",
    "nuestra solución",
    "nuestra solucion",
)

_COMPARE_MARKERS = (
    "compará",
    "compara",
    "comparar",
    "diferencia",
    "versus",
    "vs.",
)


def select_evidence_sources(query: str) -> SourceSelection:
    """Infer evidence needs without treating the inference as evidence."""
    if not query or not query.strip():
        raise ValueError("query must not be empty")

    lowered = query.strip().lower()
    requested: list[EvidenceSource] = []
    rationale: list[str] = []

    def add(source: EvidenceSource, reason: str) -> None:
        if source not in requested:
            requested.append(source)
            rationale.append(reason)

    if any(marker in lowered for marker in _COMPARE_MARKERS):
        add("sap_standard", "comparison language requests the standard layer")
        add("internal", "comparison language requests the implementation layer")

    if any(marker in lowered for marker in _RUNTIME_MARKERS):
        add("runtime", "current-system/configuration language requires runtime evidence")

    if any(marker in lowered for marker in _STANDARD_MARKERS):
        add("sap_standard", "standard-oriented language requests SAP Standard evidence")

    if any(marker in lowered for marker in _INTERNAL_MARKERS):
        add("internal", "implementation-oriented language requests internal evidence")

    if not requested:
        # A generic SAP functional question should consult both reusable
        # standard knowledge and customer implementation knowledge, while
        # explicitly recording that this is a retrieval policy, not a finding.
        add("sap_standard", "generic SAP question: check standard semantics")
        add("internal", "generic SAP question: check implementation semantics")

    return SourceSelection(
        requested=tuple(requested),
        rationale=tuple(rationale),
    )
