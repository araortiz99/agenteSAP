from src.sap import qas_read


def test_qas_read_refuses_when_runtime_disabled(monkeypatch, capsys):
    monkeypatch.delenv("AGENTESAP_SAP_RUNTIME_ENABLED", raising=False)

    assert qas_read.main(["--tool", "verified_read_tool"]) == 2
    assert "QAS runtime is disabled" in capsys.readouterr().err


def test_qas_read_rejects_non_object_args(monkeypatch, capsys):
    monkeypatch.setenv("AGENTESAP_SAP_RUNTIME_ENABLED", "true")
    monkeypatch.setenv("AGENTESAP_SAP_RUNTIME_LANDSCAPE", "QAS")
    monkeypatch.setenv("AGENTESAP_SAP_RUNTIME_SCOPE", "mcp_readonly")
    monkeypatch.setenv("AGENTESAP_SAP_RUNTIME_READ_TOOLS", "verified_read_tool")

    assert qas_read.main(["--tool", "verified_read_tool", "--args", "[]"]) == 1
    assert "--args must be a JSON object" in capsys.readouterr().err
