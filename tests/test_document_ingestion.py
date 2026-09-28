from src.document.ingestion import DocumentIngestionConfig, ingest_document
from src.document.source import DocumentSource


def test_ingestion_preserves_heading_context_and_provenance():
    source = DocumentSource(
        "source",
        "ticket.md",
        "# Inventario\n\nMIGO mueve stock.\n\n## Ajuste\n\n551 registra merma.",
    )

    result = ingest_document(source)

    assert len(result.chunks) == 2
    assert [chunk.heading for chunk in result.chunks] == ["Inventario", "Ajuste"]
    assert result.records[0].provenance.document_id == source.document_id
    assert result.evidence[0].landscape == "KNOWLEDGE"
    assert result.evidence[0].object_type == "DOCUMENT"


def test_ingestion_is_deterministic():
    source = DocumentSource("source", "ticket.md", "# MM\n\nMIGO 101.")
    first = ingest_document(source)
    second = ingest_document(source)

    assert first == second
    assert [item.evidence_id for item in first.evidence] == [
        item.evidence_id for item in second.evidence
    ]


def test_ingestion_is_bounded_by_content_and_chunks():
    source = DocumentSource("source", "large.txt", "A" * 100)

    result = ingest_document(
        source,
        config=DocumentIngestionConfig(
            max_content_chars=100,
            max_chunk_chars=10,
            max_chunks=3,
        ),
    )

    assert len(result.chunks) == 3
    assert all(len(chunk.content) <= 10 for chunk in result.chunks)


def test_ingestion_rejects_content_over_limit():
    source = DocumentSource("source", "large.txt", "A" * 101)

    try:
        ingest_document(
            source,
            config=DocumentIngestionConfig(max_content_chars=100),
        )
    except ValueError as exc:
        assert "max_content_chars" in str(exc)
    else:
        raise AssertionError("expected ValueError")


def test_ingestion_defaults_business_documents_to_candidate_authority():
    source = DocumentSource("source", "zmm.md", "# ZMM\n\nBusiness rule.")
    result = ingest_document(source)
    assert result.records[0].authority.authority.value == "candidate"
    assert result.evidence[0].provenance[-4][1] == "candidate"


def test_ingestion_rejects_unapproved_authoritative_document():
    source = DocumentSource(
        "source",
        "zmm.md",
        "# ZMM\n\nBusiness rule.",
        metadata=(
            ("authority", "authoritative"),
            ("origin", "business_document"),
            ("version", "1.0"),
            ("scope", "organization"),
        ),
    )
    try:
        ingest_document(source)
    except ValueError as exc:
        assert "approved_by" in str(exc)
    else:
        raise AssertionError("expected ValueError")
