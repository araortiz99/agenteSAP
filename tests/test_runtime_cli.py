from src.sap import runtime_cli


def test_runtime_catalog_cli_requires_explicit_enablement(monkeypatch):
    monkeypatch.delenv("AGENTESAP_SAP_RUNTIME_ENABLED", raising=False)

    try:
        runtime_cli.main(["discover-qas", "--pretty"])
    except PermissionError as exc:
        assert "disabled" in str(exc)
    else:
        raise AssertionError("catalog discovery must be disabled by default")
