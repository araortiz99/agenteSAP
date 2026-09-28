"""Deterministic bounded query decomposition for complex SAP retrieval.

The planner creates retrieval hypotheses only. It never treats a generated
subquery as evidence or as a functional conclusion.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class QueryPlan:
    original_query: str
    intent: str
    subqueries: tuple[str, ...]
    max_steps: int = 4


def _add(items: list[str], value: str) -> None:
    value = value.strip()
    if value and value not in items:
        items.append(value)


def decompose_query(query: str, *, max_steps: int = 4) -> QueryPlan:
    if not query or not query.strip():
        raise ValueError("query must not be empty")
    if max_steps < 1:
        raise ValueError("max_steps must be greater than zero")

    original = " ".join(query.split())
    lowered = original.lower()
    parts: list[str] = [original]

    comparison = any(x in lowered for x in ("diferencia", "compará", "compara", "versus", " vs "))
    troubleshooting = any(x in lowered for x in ("por qué", "porque", "causa", "error", "fall", "no genera", "no crea", "no transmite"))
    relationship = any(x in lowered for x in ("relación", "relaciona", "cómo se relacionan", "documentos participan", "end-to-end"))
    configuration = any(x in lowered for x in ("configuración", "configurado", "account determination", "determinación de cuentas", "customizing"))
    standard_custom = any(x in lowered for x in ("standard", "estándar", "custom", " z", "implementación", "desarrollo"))

    if standard_custom:
        intent = "standard_vs_custom"
        _add(parts, f"SAP Standard relacionado con: {original}")
        _add(parts, f"implementación interna relacionada con: {original}")
    elif comparison:
        intent = "comparison"
        _add(parts, f"SAP Standard: {original}")
        _add(parts, f"implementación interna/custom: {original}")
    elif troubleshooting:
        intent = "troubleshooting"
        _add(parts, f"comportamiento SAP Standard relacionado con: {original}")
        _add(parts, f"configuración y determinación funcional relacionada con: {original}")
        _add(parts, f"posibles puntos de implementación custom relacionados con: {original}")
    elif relationship:
        intent = "multi_hop"
        _add(parts, f"objetos y documentos SAP relacionados con: {original}")
        _add(parts, f"relaciones funcionales end-to-end relacionadas con: {original}")
    elif configuration:
        intent = "configuration"
        _add(parts, f"comportamiento SAP Standard y configuración relacionada con: {original}")
    elif standard_custom:
        intent = "standard_vs_custom"
        _add(parts, f"SAP Standard relacionado con: {original}")
        _add(parts, f"implementación interna relacionada con: {original}")
    else:
        intent = "factual"

    return QueryPlan(
        original_query=original,
        intent=intent,
        subqueries=tuple(parts[:max_steps]),
        max_steps=max_steps,
    )
