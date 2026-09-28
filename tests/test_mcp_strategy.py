from src.sap.mcp_strategy import plan_mcp_provider


def test_runtime_strategy_is_fail_closed_by_default():
    plan = plan_mcp_provider("runtime")

    assert plan.provider == "sap_mcp_server"
    assert plan.ready is False
    assert "no explicit read-only tool contract" in plan.reason


def test_runtime_strategy_accepts_only_registered_runtime_providers():
    plan = plan_mcp_provider("runtime", configured_provider="abap_ai")

    assert plan.provider == "abap_ai"
    assert plan.ready is False


def test_runtime_strategy_rejects_developer_context_provider():
    plan = plan_mcp_provider("runtime", configured_provider="sap_devs")

    assert plan.provider == "sap_devs"
    assert plan.ready is False
    assert "not approved for runtime" in plan.reason


def test_external_strategy_defaults_to_sap_devs():
    plan = plan_mcp_provider("external")

    assert plan.provider == "sap_devs"
    assert plan.ready is True


def test_external_strategy_rejects_runtime_provider():
    plan = plan_mcp_provider("external", configured_provider="sap_mcp_server")

    assert plan.provider == "sap_mcp_server"
    assert plan.ready is False
    assert "not eligible for external" in plan.reason
