from pathlib import Path

import pytest

from src.sap.registry import SAPSource, SourceRegistry


def test_registry_round_trip(tmp_path: Path):
    registry = SourceRegistry(tmp_path / "registry.json")
    source = SAPSource(
        source_id="SAP-TEST",
        url="https://help.sap.com/docs/test",
        product="SAP S/4HANA",
        module="MM",
        release="2025",
    )
    registry.save({source.source_id: source})
    assert registry.get("SAP-TEST") == source


def test_unknown_source_is_rejected(tmp_path: Path):
    registry = SourceRegistry(tmp_path / "registry.json")
    with pytest.raises(KeyError):
        registry.get("DOES-NOT-EXIST")
