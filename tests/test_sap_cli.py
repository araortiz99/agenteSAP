from pathlib import Path

from src.sap.cli import main
from src.sap.registry import SAPSource, SourceRegistry


def test_cli_rejects_unregistered_url_override(tmp_path: Path, capsys):
    registry_path = tmp_path / "registry.json"
    SourceRegistry(registry_path).save({
        "SAP-TEST": SAPSource(
            source_id="SAP-TEST",
            url="https://help.sap.com/docs/test",
            product="SAP S/4HANA",
            module="MM",
            release="2025",
        )
    })

    assert main([
        "--source-id", "SAP-TEST",
        "--registry", str(registry_path),
        "--url", "https://help.sap.com/docs/other",
    ]) == 2
    assert "registered source" in capsys.readouterr().err
