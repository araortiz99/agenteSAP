from pathlib import Path

import pytest

from src.document.file_input import SUPPORTED_TEXT_TYPES, load_document_file


def test_load_document_file_creates_transport_neutral_source(tmp_path: Path):
    path = tmp_path / "incidente.md"
    path.write_text("# MM\n\nZMM_IM_0002 registra merma.", encoding="utf-8")

    source = load_document_file(path)

    assert source.filename == "incidente.md"
    assert source.file_type == "md"
    assert source.media_type == "text/markdown"
    assert source.metadata == (("source", "LOCAL_FILE"),)
    assert source.content_hash
    assert source.document_id.startswith("DOC-")


def test_supported_text_types_are_explicit():
    assert SUPPORTED_TEXT_TYPES == frozenset({"txt", "md", "csv"})


def test_load_document_file_rejects_unsupported_format(tmp_path: Path):
    path = tmp_path / "spec.pdf"
    path.write_bytes(b"%PDF")

    with pytest.raises(ValueError, match="unsupported document type"):
        load_document_file(path)


def test_load_document_file_rejects_oversized_file(tmp_path: Path):
    path = tmp_path / "large.txt"
    path.write_text("123456", encoding="utf-8")

    with pytest.raises(ValueError, match="max_bytes"):
        load_document_file(path, max_bytes=5)


def test_load_document_file_rejects_missing_file(tmp_path: Path):
    with pytest.raises(FileNotFoundError):
        load_document_file(tmp_path / "missing.txt")


def test_load_document_file_is_read_only(tmp_path: Path):
    path = tmp_path / "ticket.txt"
    path.write_text("contenido", encoding="utf-8")
    before = path.stat().st_mtime_ns

    load_document_file(path)

    assert path.read_text(encoding="utf-8") == "contenido"
    assert path.stat().st_mtime_ns == before
