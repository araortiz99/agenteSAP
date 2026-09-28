"""Executable semantic acceptance checks for the SAP MM v1 benchmark.

These checks complement the broad regression matrix by asserting the boundaries
that the benchmark is intended to protect: evidence layers, provenance,
bounded planning, and missing-runtime handling.
"""

from src.agent.investigation import investigate

from tests.test_mm_investigation_v1 import InvestigationFixtureClient


def test_mm_standard_and_custom_evidence_layers_remain_distinct():
    result = investigate(
        InvestigationFixtureClient(),
        "Compará SAP Standard con la implementación ZMM_IM_0002.",
        max_steps=4,
        max_results=8,
        max_hops=2,
    )

    standard = [
        item for item in result.evidence_collected
        if item.provider == "sap_standard"
    ]
    internal = [
        item for item in result.evidence_collected
        if item.provider == "internal"
    ]

    assert standard
    assert internal
    assert all(item.landscape == "KNOWLEDGE" for item in standard + internal)
    assert all(item.provenance for item in standard + internal)
    assert not any(
        item.provider == "sap_standard"
        and "ZMM_IM_0002" in item.content
        for item in result.evidence_collected
    )


def test_mm_query_plan_is_not_promoted_to_evidence():
    result = investigate(
        InvestigationFixtureClient(),
        "¿Qué significa el movimiento 551?",
        max_steps=4,
        max_results=8,
        max_hops=2,
    )

    evidence_text = "\n".join(item.content for item in result.evidence_collected)

    assert result.plan.subqueries
    assert all(
        subquery not in evidence_text
        for subquery in result.plan.subqueries
    )
    assert all(item.landscape == "KNOWLEDGE" for item in result.evidence_collected)


def test_mm_missing_runtime_evidence_remains_explicit():
    result = investigate(
        InvestigationFixtureClient(),
        "¿Por qué falla actualmente en QAS el proceso de inventario?",
        max_steps=4,
        max_results=8,
        max_hops=2,
    )

    assert any("runtime" in gap.lower() for gap in result.evidence_missing)
    assert result.stop_reason == "missing_capability"
    assert result.confidence == "LOW"
    assert "evidence" in result.confidence_reason.lower()


def test_mm_multihop_relationships_remain_bounded():
    result = investigate(
        InvestigationFixtureClient(),
        "¿Cómo se relacionan purchase order, goods receipt, material document y accounting document?",
        max_steps=4,
        max_results=8,
        max_hops=2,
    )

    assert result.knowledge_context.relationships
    assert all(0 <= item.hop <= 2 for item in result.knowledge_context.relationships)
