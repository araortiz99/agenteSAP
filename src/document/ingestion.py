"""Bounded, deterministic document ingestion pipeline."""

from __future__ import annotations

from dataclasses import dataclass

from src.document.chunking import DocumentChunk, chunk_document
from src.document.integration import record_to_investigation_evidence
from src.document.provenance import DocumentRecord, chunk_to_record
from src.document.sap_entities import SapEntity, extract_sap_entities
from src.document.source import DocumentSource
from src.document.structure import DocumentStructure, parse_text_structure
from src.investigation.contracts import InvestigationEvidence


@dataclass(frozen=True)
class DocumentIngestionConfig:
    max_content_chars: int = 200_000
    max_chunk_chars: int = 1_600
    max_chunks: int = 128
    max_entities_per_record: int = 64

    def validate(self) -> None:
        if self.max_content_chars < 1:
            raise ValueError("max_content_chars must be greater than zero")
        if self.max_chunk_chars < 1:
            raise ValueError("max_chunk_chars must be greater than zero")
        if self.max_chunks < 1:
            raise ValueError("max_chunks must be greater than zero")
        if self.max_entities_per_record < 1:
            raise ValueError("max_entities_per_record must be greater than zero")


@dataclass(frozen=True)
class IngestedDocument:
    source: DocumentSource
    structure: DocumentStructure
    chunks: tuple[DocumentChunk, ...]
    records: tuple[DocumentRecord, ...]
    evidence: tuple[InvestigationEvidence, ...]
    entities: tuple[SapEntity, ...]


def ingest_document(
    source: DocumentSource,
    *,
    config: DocumentIngestionConfig | None = None,
) -> IngestedDocument:
    """Run the bounded document pipeline without external side effects."""
    settings = config or DocumentIngestionConfig()
    settings.validate()

    if len(source.content) > settings.max_content_chars:
        raise ValueError(
            f"document content exceeds max_content_chars={settings.max_content_chars}"
        )

    structure = parse_text_structure(source)
    chunks = chunk_document(
        structure,
        max_chunk_chars=settings.max_chunk_chars,
        max_chunks=settings.max_chunks,
    )
    records = tuple(chunk_to_record(chunk, source.filename) for chunk in chunks)
    evidence = tuple(record_to_investigation_evidence(record) for record in records)

    extracted: list[SapEntity] = []
    for record in records:
        remaining = settings.max_entities_per_record
        extracted.extend(extract_sap_entities(record, max_entities=remaining))

    return IngestedDocument(
        source=source,
        structure=structure,
        chunks=chunks,
        records=records,
        evidence=evidence,
        entities=tuple(extracted),
    )
