from src.sap import runtime_preflight


def test_preflight_disabled_by_default(monkeypatch):
    monkeypatch.delenv("AGENTESAP_SAP_RUNTIME_ENABLED", raising=False)

    result = runtime_preflight.run_preflight()

    assert result["enabled"] is False
    assert result["ready"] is False


def test_preflight_reports_invalid_allowlist(monkeypatch):
    monkeypatch.setenv("AGENTESAP_SAP_RUNTIME_ENABLED", "true")
    monkeypatch.setenv("AGENTESAP_SAP_RUNTIME_LANDSCAPE", "QAS")
    monkeypatch.setenv("AGENTESAP_SAP_RUNTIME_SCOPE", "mcp_readonly")
    monkeypatch.setenv("AGENTESAP_SAP_RUNTIME_READ_TOOLS", "read_table,unsafe_tool")

    class FakeGateway:
        target = type(
            "Target",
            (),
            {
                "provider": "sap_mcp_server",
                "metadata": {"landscape": "QAS", "system": "S4QAS"},
                "read_only": True,
                "allowed_tools": ("read_table", "unsafe_tool"),
            },
        )()

        def validate_runtime_allowlist(self):
            return (
                {"name": "read_table", "valid": True, "reason": "advertised and explicitly read-only"},
                {"name": "unsafe_tool", "valid": False, "reason": "destructive_hint=true"},
            )

    monkeypatch.setattr(runtime_preflight.McpEvidenceGateway, "from_qas_runtime_env", lambda: FakeGateway())

    result = runtime_preflight.run_preflight()

    assert result["enabled"] is True
    assert result["ready"] is False
    assert result["invalid_tools"] == ["unsafe_tool"]


def test_preflight_ready_when_all_allowlisted_tools_are_read_only(monkeypatch):
    class FakeGateway:
        target = type(
            "Target",
            (),
            {
                "provider": "sap_mcp_server",
                "metadata": {"landscape": "QAS", "system": "S4QAS"},
                "read_only": True,
                "allowed_tools": ("read_table",),
            },
        )()

        def validate_runtime_allowlist(self):
            return (
                {"name": "read_table", "valid": True, "reason": "advertised and explicitly read-only"},
            )

    monkeypatch.setattr(runtime_preflight.McpEvidenceGateway, "from_qas_runtime_env", lambda: FakeGateway())

    result = runtime_preflight.run_preflight()

    assert result["ready"] is True
    assert result["invalid_tools"] == []
    assert result["landscape"] == "QAS"
