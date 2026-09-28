from pathlib import Path

import pytest

from src.document.ingestion import ingest_documents
from src.document.source import DocumentSource


def _source(name: str, content: str) -> DocumentSource:
    return DocumentSource(source_id=name, filename=name, content=content)


def test_ingest_documents_aggregates_distinct_sources_with_provenance():
    result = ingest_documents(
        [
            _source("ticket.md", "# Ticket\n\nIncidente 31426 en centro 5023."),
            _source("analysis.txt", "Material 100123 presenta diferencia de stock."),
        ]
    )

    assert result.document_count == 2
    assert len(result.evidence) == 2
    assert {dict(item.provenance)["filename"] for item in result.evidence} == {
        "ticket.md",
        "analysis.txt",
    }


def test_ingest_documents_deduplicates_same_document_identity():
    first = _source("a.txt", "Material 100123 centro 5023.")
    second = _source("b.txt", "Material 100123 centro 5023.")

    result = ingest_documents([first, second])

    assert result.document_count == 1
    assert result.documents[0].source.filename == "a.txt"


def test_ingest_documents_enforces_document_count():
    with pytest.raises(ValueError, match="max_documents"):
        ingest_documents(
            [_source(f"{index}.txt", "evidence") for index in range(3)],
            max_documents=2,
        )


def test_ingest_documents_enforces_aggregate_content_limit():
    with pytest.raises(ValueError, match="aggregate content"):
        ingest_documents(
            [_source("a.txt", "12345"), _source("b.txt", "67890")],
            max_total_content_chars=9,
        )


def test_ingest_documents_enforces_aggregate_evidence_limit():
    with pytest.raises(ValueError, match="aggregate evidence"):
        ingest_documents(
            [_source("a.txt", "first"), _source("b.txt", "second")],
            max_total_evidence=1,
        )
