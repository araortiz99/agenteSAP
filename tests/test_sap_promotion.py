from pathlib import Path

import pytest

from src.sap.metadata import build_metadata, render_candidate
from src.sap.promotion import PromotionError, promote_candidate
from src.sap.registry import SAPSource, SourceRegistry


def _registry(tmp_path: Path) -> SourceRegistry:
    registry = SourceRegistry(tmp_path / "registry.json")
    source = SAPSource(
        source_id="SAP-TEST",
        url="https://help.sap.com/docs/test",
        product="SAP S/4HANA",
        module="MM",
        release="2025",
        language="en",
    )
    registry.save({"SAP-TEST": source})
    return registry


def _candidate(tmp_path: Path) -> Path:
    metadata = build_metadata(
        "SAP-TEST",
        "https://help.sap.com/docs/test",
        "SAP S/4HANA",
        "MM",
        "2025",
        "en",
        "SAP content",
    )
    path = tmp_path / "candidate.md"
    path.write_text(
        render_candidate(metadata, "Test", "SAP content"),
        encoding="utf-8",
    )
    return path


def test_promotes_valid_candidate(tmp_path: Path):
    candidate = _candidate(tmp_path)
    result = promote_candidate(
        candidate_path=candidate,
        destination_dir=tmp_path / "knowledge",
        registry=_registry(tmp_path),
    )
    assert result.status == "validated"
    assert result.certainty == "confirmed"
    promoted = (tmp_path / "knowledge" / "sap-test.md").read_text(encoding="utf-8")
    assert "status: validated" in promoted
    assert "certainty: confirmed" in promoted
    assert "CANDIDATE" not in promoted


def test_rejects_unknown_source(tmp_path: Path):
    candidate = _candidate(tmp_path)
    registry = SourceRegistry(tmp_path / "registry.json")
    with pytest.raises(KeyError):
        promote_candidate(
            candidate_path=candidate,
            destination_dir=tmp_path / "knowledge",
            registry=registry,
        )


def test_rejects_checksum_change(tmp_path: Path):
    candidate = _candidate(tmp_path)
    content = candidate.read_text(encoding="utf-8").replace("SAP content", "Changed content")
    candidate.write_text(content, encoding="utf-8")
    with pytest.raises(PromotionError, match="checksum"):
        promote_candidate(
            candidate_path=candidate,
            destination_dir=tmp_path / "knowledge",
            registry=_registry(tmp_path),
        )


def test_rejects_duplicate(tmp_path: Path):
    candidate = _candidate(tmp_path)
    destination = tmp_path / "knowledge"
    promote_candidate(
        candidate_path=candidate,
        destination_dir=destination,
        registry=_registry(tmp_path),
    )
    with pytest.raises(PromotionError, match="equivalent"):
        promote_candidate(
            candidate_path=candidate,
            destination_dir=destination,
            registry=_registry(tmp_path),
        )
