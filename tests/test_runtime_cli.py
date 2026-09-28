from src.sap import runtime_cli


def test_runtime_catalog_cli_requires_explicit_enablement(monkeypatch):
    monkeypatch.delenv("AGENTESAP_SAP_RUNTIME_ENABLED", raising=False)

    try:
        runtime_cli.main(["discover-qas", "--pretty"])
    except PermissionError as exc:
        assert "disabled" in str(exc)
    else:
        raise AssertionError("catalog discovery must be disabled by default")


def test_runtime_preflight_cli_is_fail_closed(monkeypatch):
    monkeypatch.setenv("AGENTESAP_SAP_RUNTIME_ENABLED", "true")
    monkeypatch.setenv("AGENTESAP_SAP_RUNTIME_LANDSCAPE", "QAS")
    monkeypatch.setenv("AGENTESAP_SAP_RUNTIME_READ_TOOLS", "verified_read_tool")

    class FakeGateway:
        @classmethod
        def from_qas_runtime_env(cls):
            return cls()

        def validate_runtime_allowlist(self):
            return (
                {
                    "name": "verified_read_tool",
                    "valid": True,
                    "reason": "advertised and explicitly read-only",
                },
            )

    monkeypatch.setattr(runtime_cli, "McpEvidenceGateway", FakeGateway)

    assert runtime_cli.main(["validate-qas"]) == 0


def test_runtime_preflight_cli_returns_nonzero_for_invalid_tool(monkeypatch):
    monkeypatch.setenv("AGENTESAP_SAP_RUNTIME_ENABLED", "true")
    monkeypatch.setenv("AGENTESAP_SAP_RUNTIME_LANDSCAPE", "QAS")
    monkeypatch.setenv("AGENTESAP_SAP_RUNTIME_READ_TOOLS", "unsafe_tool")

    class FakeGateway:
        @classmethod
        def from_qas_runtime_env(cls):
            return cls()

        def validate_runtime_allowlist(self):
            return (
                {
                    "name": "unsafe_tool",
                    "valid": False,
                    "reason": "requires read_only_hint=true",
                },
            )

    monkeypatch.setattr(runtime_cli, "McpEvidenceGateway", FakeGateway)

    assert runtime_cli.main(["validate-qas"]) == 2
