from src.document.source import DocumentSource, DocumentStatus, build_document_identity


def test_identity_is_deterministic_and_filename_independent():
    first = DocumentSource("source-a", "a.txt", "hola")
    second = DocumentSource("source-b", "b.md", "hola")
    assert first.document_id == second.document_id
    assert first.content_hash == second.content_hash


def test_different_content_has_different_identity():
    a = build_document_identity("A")
    b = build_document_identity("B")
    assert a != b


def test_unicode_is_hashed_as_utf8():
    source = DocumentSource("unicode", "x.txt", "SAP — ñá")
    assert len(source.content_hash) == 64
    assert source.size > len(source.content)


def test_empty_document_is_valid_source():
    source = DocumentSource("empty", "empty.txt", "")
    assert source.document_id.startswith("DOC-")
    assert source.file_type == "txt"


def test_file_type_and_status_contract():
    source = DocumentSource("md", "manual.MD", "# title")
    assert source.file_type == "md"
    assert DocumentStatus.AVAILABLE.value == "AVAILABLE"


def test_invalid_source_metadata_is_rejected():
    try:
        DocumentSource("", "x.txt", "x")
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError")
