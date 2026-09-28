import json
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


def test_qas_readiness_is_disabled_by_default(monkeypatch, capsys):
    monkeypatch.delenv("AGENTESAP_SAP_RUNTIME_ENABLED", raising=False)
    assert runtime_cli.main(["readiness-qas"]) == 2
    report = json.loads(capsys.readouterr().out)
    assert report["runtime_ready"] is False
    assert report["reason"] == "runtime disabled"


def test_qas_readiness_requires_readonly_scope(monkeypatch, capsys):
    monkeypatch.setenv("AGENTESAP_SAP_RUNTIME_ENABLED", "true")
    monkeypatch.setenv("AGENTESAP_SAP_RUNTIME_LANDSCAPE", "QAS")
    monkeypatch.setenv("AGENTESAP_SAP_RUNTIME_SCOPE", "write")
    assert runtime_cli.main(["readiness-qas"]) == 2
    report = json.loads(capsys.readouterr().out)
    assert report["reason"] == "scope must be mcp_readonly"


def test_qas_readiness_rejects_non_qas_landscape(monkeypatch, capsys):
    monkeypatch.setenv("AGENTESAP_SAP_RUNTIME_ENABLED", "true")
    monkeypatch.setenv("AGENTESAP_SAP_RUNTIME_LANDSCAPE", "PRD")
    monkeypatch.setenv("AGENTESAP_SAP_RUNTIME_SCOPE", "mcp_readonly")
    assert runtime_cli.main(["readiness-qas"]) == 2
    report = json.loads(capsys.readouterr().out)
    assert report["reason"] == "landscape must be QAS"


def test_qas_readiness_can_verify_a_readonly_catalog(monkeypatch, capsys):
    monkeypatch.setenv("AGENTESAP_SAP_RUNTIME_ENABLED", "true")
    monkeypatch.setenv("AGENTESAP_SAP_RUNTIME_LANDSCAPE", "QAS")
    monkeypatch.setenv("AGENTESAP_SAP_RUNTIME_SCOPE", "mcp_readonly")
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

    assert runtime_cli.main(["readiness-qas", "--verify-catalog"]) == 0
    report = json.loads(capsys.readouterr().out)
    assert report["catalog_verified"] is True
    assert report["allowlist_validated"] is True
    assert report["runtime_ready"] is True


def test_qas_readiness_reports_catalog_validation_failure(monkeypatch, capsys):
    monkeypatch.setenv("AGENTESAP_SAP_RUNTIME_ENABLED", "true")
    monkeypatch.setenv("AGENTESAP_SAP_RUNTIME_LANDSCAPE", "QAS")
    monkeypatch.setenv("AGENTESAP_SAP_RUNTIME_SCOPE", "mcp_readonly")
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
                    "reason": "destructive_hint=true",
                },
            )

    monkeypatch.setattr(runtime_cli, "McpEvidenceGateway", FakeGateway)

    assert runtime_cli.main(["readiness-qas", "--verify-catalog"]) == 2
    report = json.loads(capsys.readouterr().out)
    assert report["catalog_verified"] is True
    assert report["allowlist_validated"] is False
    assert report["runtime_ready"] is False
    assert "destructive_hint=true" in report["reason"]


def test_qas_readiness_does_not_verify_catalog_without_explicit_probe(monkeypatch, capsys):
    monkeypatch.setenv("AGENTESAP_SAP_RUNTIME_ENABLED", "true")
    monkeypatch.setenv("AGENTESAP_SAP_RUNTIME_LANDSCAPE", "QAS")
    monkeypatch.setenv("AGENTESAP_SAP_RUNTIME_SCOPE", "mcp_readonly")
    monkeypatch.setenv("AGENTESAP_SAP_RUNTIME_READ_TOOLS", "verified_read_tool")

    class FakeGateway:
        @classmethod
        def from_qas_runtime_env(cls):
            raise AssertionError("catalog must not be contacted without --verify-catalog")

    monkeypatch.setattr(runtime_cli, "McpEvidenceGateway", FakeGateway)

    assert runtime_cli.main(["readiness-qas"]) == 2
    report = json.loads(capsys.readouterr().out)
    assert report["catalog_verified"] is False
    assert report["runtime_ready"] is False


def test_qas_read_cli_requires_allowlisted_read_only_tool(monkeypatch):
    monkeypatch.setenv("AGENTESAP_SAP_RUNTIME_ENABLED", "true")
    monkeypatch.setenv("AGENTESAP_SAP_RUNTIME_LANDSCAPE", "QAS")
    monkeypatch.setenv("AGENTESAP_SAP_RUNTIME_SCOPE", "mcp_readonly")
    monkeypatch.setenv("AGENTESAP_SAP_RUNTIME_READ_TOOLS", "verified_read_tool")

    class FakeEvidence:
        provider = "sap_mcp_server"
        operation = "verified_read_tool"
        landscape = "QAS"
        system = "S4QAS"
        object_id = "MARA"
        observation_type = "runtime_observation"
        certainty = "observed"
        content = '{"rows":[{"MATNR":"100123"}]}'
        provenance = (("provider", "sap_mcp_server"), ("landscape", "QAS"))

    class FakeGateway:
        @classmethod
        def from_qas_runtime_env(cls):
            return cls()

        def validate_runtime_allowlist(self):
            return ({"name": "verified_read_tool", "valid": True, "reason": "read-only"},)

        def read_runtime(self, tool_name, arguments):
            assert tool_name == "verified_read_tool"
            assert arguments == {"query": "MARA"}
            return FakeEvidence()

    monkeypatch.setattr(runtime_cli, "McpEvidenceGateway", FakeGateway)
    assert runtime_cli.main([
        "read-qas",
        "--tool", "verified_read_tool",
        "--arguments", '{"query":"MARA"}',
    ]) == 0


def test_qas_read_cli_rejects_non_allowlisted_tool(monkeypatch):
    monkeypatch.setenv("AGENTESAP_SAP_RUNTIME_ENABLED", "true")
    monkeypatch.setenv("AGENTESAP_SAP_RUNTIME_LANDSCAPE", "QAS")
    monkeypatch.setenv("AGENTESAP_SAP_RUNTIME_SCOPE", "mcp_readonly")
    monkeypatch.setenv("AGENTESAP_SAP_RUNTIME_READ_TOOLS", "verified_read_tool")

    class FakeGateway:
        @classmethod
        def from_qas_runtime_env(cls):
            return cls()

        def validate_runtime_allowlist(self):
            return ({"name": "verified_read_tool", "valid": True, "reason": "read-only"},)

    monkeypatch.setattr(runtime_cli, "McpEvidenceGateway", FakeGateway)

    try:
        runtime_cli.main([
            "read-qas",
            "--tool", "unknown_tool",
            "--arguments", "{}",
        ])
    except PermissionError as exc:
        assert "not allowlisted" in str(exc)
    else:
        raise AssertionError("unallowlisted runtime tool must be rejected")
