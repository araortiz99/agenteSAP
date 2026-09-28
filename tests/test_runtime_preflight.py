from src.sap.runtime_preflight import run_preflight


def test_runtime_preflight_is_disabled_by_default(monkeypatch):
    monkeypatch.delenv("AGENTESAP_SAP_RUNTIME_ENABLED", raising=False)

    result = run_preflight()

    assert result["enabled"] is False
    assert result["ready"] is False


def test_runtime_preflight_reports_missing_allowlist(monkeypatch):
    monkeypatch.setenv("AGENTESAP_SAP_RUNTIME_ENABLED", "true")
    monkeypatch.setenv("AGENTESAP_SAP_RUNTIME_LANDSCAPE", "QAS")
    monkeypatch.setenv("AGENTESAP_SAP_RUNTIME_SCOPE", "mcp_readonly")
    monkeypatch.setenv("AGENTESAP_SAP_RUNTIME_READ_TOOLS", "read_table,missing_tool")

    from src.sap.mcp_gateway import McpEvidenceGateway

    gateway = McpEvidenceGateway.from_qas_runtime_env()
    assert gateway is not None
    gateway.runtime_tool_catalog = lambda: (
        {"name": "read_table", "read_only_hint": True, "destructive_hint": False},
    )

    # Replace construction for this test so the preflight consumes the controlled
    # catalog without opening a real MCP process.
    original = McpEvidenceGateway.from_qas_runtime_env
    McpEvidenceGateway.from_qas_runtime_env = classmethod(lambda cls: gateway)
    try:
        result = run_preflight()
    finally:
        McpEvidenceGateway.from_qas_runtime_env = original

    assert result["ready"] is False
    assert result["missing_allowlisted_tools"] == ["missing_tool"]
