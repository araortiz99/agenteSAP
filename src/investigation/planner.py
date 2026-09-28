"""Deterministic investigation planner for the first SAP MM vertical slice."""

from __future__ import annotations

from dataclasses import dataclass

from src.investigation.contracts import InvestigationStep
from src.investigation.entities import missing_required_entities


@dataclass(frozen=True)
class InvestigationPlan:
    intent: str
    required_evidence: tuple[str, ...]
    required_entities: tuple[str, ...]
    steps: tuple[InvestigationStep, ...]
    stop_conditions: tuple[str, ...]


def create_plan(question: str, entities) -> InvestigationPlan:
    if not question.strip():
        raise ValueError("question must not be empty")
    intent = "stock_discrepancy"
    required_entities = ("material", "plant")
    required_evidence = (
        "material_master",
        "plant_data",
        "current_stock",
        "relevant_movements",
        "material_documents",
    )
    steps = (
        InvestigationStep("S1", "Resolve material and plant", "master_data", required_entities),
        InvestigationStep("S2", "Retrieve current stock", "current_stock", ("material", "plant")),
        InvestigationStep("S3", "Retrieve relevant movements", "movements", ("material", "plant")),
        InvestigationStep("S4", "Correlate material documents and quantities", "material_documents", ("material", "plant")),
        InvestigationStep("S5", "Evaluate evidence and conclude", "functional_analysis", required_entities),
    )
    stops = (
        "missing_entity",
        "missing_capability",
        "conflicting_evidence",
        "evidence_sufficient",
        "max_steps_reached",
    )
    return InvestigationPlan(
        intent=intent,
        required_evidence=required_evidence,
        required_entities=required_entities,
        steps=steps,
        stop_conditions=stops,
    )
