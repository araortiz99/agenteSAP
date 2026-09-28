from src.sap.runtime_preflight import run_preflight


def test_runtime_preflight_is_disabled_by_default(monkeypatch):
    monkeypatch.delenv("AGENTESAP_SAP_RUNTIME_ENABLED", raising=False)

    result = run_preflight()

    assert result["enabled"] is False
    assert result["ready"] is False
