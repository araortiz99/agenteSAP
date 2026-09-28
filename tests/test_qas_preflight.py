from src.sap import qas_preflight


def test_qas_preflight_reports_disabled_runtime(monkeypatch, capsys):
    monkeypatch.delenv("AGENTESAP_SAP_RUNTIME_ENABLED", raising=False)

    assert qas_preflight.main([]) == 2
    assert "QAS runtime is disabled" in capsys.readouterr().out
