import pytest
from src.mcp.consultant_server import agentesap_health, investigate_sap

def test_health_never_exposes_credentials(monkeypatch):
    monkeypatch.setenv("GITHUB_TOKEN","secret-value")
    result=agentesap_health()
    assert result["read_only"] is True
    assert result["github_configured"] is True
    assert "secret-value" not in str(result)

def test_health_reports_safe_runtime_flags(monkeypatch):
    monkeypatch.setenv("AGENTESAP_SAP_RUNTIME_ENABLED","true")
    result=agentesap_health()
    assert result["qas_runtime_enabled"] is True
    assert result["read_only"] is True

def test_investigate_sap_validates_request():
    with pytest.raises(ValueError,match="request must not be empty"):
        investigate_sap("")

def test_investigate_sap_validates_bounds():
    with pytest.raises(ValueError,match="max_steps"):
        investigate_sap("material master",max_steps=11)
    with pytest.raises(ValueError,match="max_results"):
        investigate_sap("material master",max_results=21)
