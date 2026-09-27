from pathlib import Path

import pytest

from src.sap.collector import SAPSourceError, _validate_url
from src.sap.metadata import build_metadata, render_candidate
from src.sap.parser import parse_html


def test_only_official_sap_help_is_allowed():
    _validate_url("https://help.sap.com/docs/example")
    with pytest.raises(SAPSourceError):
        _validate_url("https://example.com/sap")
    with pytest.raises(SAPSourceError):
        _validate_url("http://help.sap.com/docs/example")


def test_parser_removes_script_and_extracts_title():
    title, text = parse_html("<html><title>SAP Test</title><script>secret()</script><h1>Goods Movement</h1><p>Standard process.</p></html>")
    assert title == "SAP Test"
    assert "Goods Movement" in text
    assert "secret" not in text


def test_metadata_is_candidate_and_traceable():
    metadata = build_metadata(
        "SAP-TEST",
        "https://help.sap.com/docs/example",
        "SAP S/4HANA",
        "MM",
        "2025",
        "en",
        "content",
    )
    rendered = render_candidate(metadata, "Test", "SAP content")
    assert metadata.status == "candidate"
    assert metadata.certainty == "under_validation"
    assert "source_id: SAP-TEST" in rendered
    assert "CANDIDATE" in rendered
    assert "checksum_sha256:" in rendered
