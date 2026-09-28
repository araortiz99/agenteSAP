from src.sap.qas_runtime import SapQasRuntimeConfig
from src.sap.mcp_gateway import McpEvidenceGateway


def test_qas_runtime_config_is_disabled_by_default(monkeypatch):
    monkeypatch.delenv("AGENTESAP_SAP_RUNTIME_ENABLED", raising=False)
    config = SapQasRuntimeConfig.from_env()

    assert config.enabled is False
    assert config.landscape == "QAS"


def test_qas_runtime_config_requires_explicit_read_tool_allowlist(monkeypatch):
    monkeypatch.setenv("AGENTESAP_SAP_RUNTIME_ENABLED", "true")
    monkeypatch.setenv("AGENTESAP_SAP_RUNTIME_LANDSCAPE", "QAS")
    monkeypatch.delenv("AGENTESAP_SAP_RUNTIME_READ_TOOLS", raising=False)

    try:
        SapQasRuntimeConfig.from_env()
    except ValueError as exc:
        assert "explicit read-tool allowlist" in str(exc)
    else:
        raise AssertionError("runtime must fail closed without an explicit tool allowlist")


def test_qas_runtime_config_rejects_non_qas(monkeypatch):
    monkeypatch.setenv("AGENTESAP_SAP_RUNTIME_ENABLED", "true")
    monkeypatch.setenv("AGENTESAP_SAP_RUNTIME_LANDSCAPE", "PRD")
    monkeypatch.setenv("AGENTESAP_SAP_RUNTIME_READ_TOOLS", "verified_read_tool")

    try:
        SapQasRuntimeConfig.from_env()
    except ValueError as exc:
        assert "restricted to landscape QAS" in str(exc)
    else:
        raise AssertionError("runtime integration must reject PRD at this stage")


def test_qas_runtime_config_parses_explicit_read_tools(monkeypatch):
    monkeypatch.setenv("AGENTESAP_SAP_RUNTIME_ENABLED", "true")
    monkeypatch.setenv("AGENTESAP_SAP_RUNTIME_LANDSCAPE", "qas")
    monkeypatch.setenv(
        "AGENTESAP_SAP_RUNTIME_READ_TOOLS",
        "verified_table_read, verified_ddic_read",
    )
    monkeypatch.setenv(
        "AGENTESAP_SAP_MCP_ARGS",
        '--profile "qas readonly"',
    )

    config = SapQasRuntimeConfig.from_env()

    assert config.enabled is True
    assert config.landscape == "QAS"
    assert config.allowed_tools == ("verified_table_read", "verified_ddic_read")
    assert config.args == ("--profile", "qas readonly")


def test_qas_runtime_gateway_requires_allowlisted_tool(monkeypatch):
    monkeypatch.setenv("AGENTESAP_SAP_RUNTIME_ENABLED", "true")
    monkeypatch.setenv("AGENTESAP_SAP_RUNTIME_LANDSCAPE", "QAS")
    monkeypatch.setenv("AGENTESAP_SAP_RUNTIME_READ_TOOLS", "verified_table_read")

    gateway = McpEvidenceGateway.from_qas_runtime_env()

    assert gateway is not None
    assert gateway.target.provider == "sap_mcp_server"
    assert gateway.target.read_only is True
    assert gateway.target.observation_type == "runtime_observation"
    assert gateway.target.metadata["landscape"] == "QAS"

    try:
        gateway.read_runtime("unapproved_tool", {})
    except PermissionError as exc:
        assert "not allowlisted" in str(exc)
    else:
        raise AssertionError("unapproved runtime tools must be denied")


def test_qas_runtime_gateway_is_opt_in(monkeypatch):
    monkeypatch.delenv("AGENTESAP_SAP_RUNTIME_ENABLED", raising=False)

    assert McpEvidenceGateway.from_qas_runtime_env() is None
