from src.tools.query_planner import decompose_query


def test_simple_query_is_not_over_decomposed():
    plan = decompose_query("¿Qué es MIGO?")
    assert plan.intent == "factual"
    assert plan.subqueries == ("¿Qué es MIGO?",)


def test_troubleshooting_query_is_bounded():
    plan = decompose_query("¿Por qué una entrada no genera documento contable?")
    assert plan.intent == "troubleshooting"
    assert len(plan.subqueries) <= 4
    assert any("Standard" in item for item in plan.subqueries)


def test_comparison_query_separates_standard_and_internal():
    plan = decompose_query("Diferencia entre comportamiento estándar y nuestra implementación")
    assert plan.intent == "comparison"
    assert any("SAP Standard" in item for item in plan.subqueries)
    assert any("implementación interna" in item for item in plan.subqueries)


def test_multi_hop_query_is_explicit():
    plan = decompose_query("¿Cómo se relacionan el pedido, el documento material y el documento contable?")
    assert plan.intent == "multi_hop"
    assert len(plan.subqueries) <= 4


def test_empty_query_rejected():
    try:
        decompose_query("")
    except ValueError:
        return
    raise AssertionError("empty query must raise ValueError")
