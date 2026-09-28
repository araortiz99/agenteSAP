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


@dataclass(frozen=True)
class MultiDocumentIngestion:
    """Bounded aggregate of multiple independent document ingestions."""

    documents: tuple[IngestedDocument, ...]
    evidence: tuple[InvestigationEvidence, ...]
    entities: tuple[SapEntity, ...]

    @property
    def document_count(self) -> int:
        return len(self.documents)


def ingest_documents(
    sources: tuple[DocumentSource, ...] | list[DocumentSource],
    *,
    config: DocumentIngestionConfig | None = None,
    max_documents: int = 16,
    max_total_content_chars: int = 1_000_000,
    max_total_evidence: int = 512,
) -> MultiDocumentIngestion:
    """Ingest multiple explicit sources with aggregate safety bounds.

    Sources are processed in caller order. Duplicate document identities are
    ignored deterministically so the same content cannot be counted twice.
    No filesystem, SAP, MCP, network, or persistence side effects occur here.
    """
    if max_documents < 1:
        raise ValueError("max_documents must be greater than zero")
    if max_total_content_chars < 1:
        raise ValueError("max_total_content_chars must be greater than zero")
    if max_total_evidence < 1:
        raise ValueError("max_total_evidence must be greater than zero")

    materialized = tuple(sources)
    if len(materialized) > max_documents:
        raise ValueError(f"document count exceeds max_documents={max_documents}")

    settings = config or DocumentIngestionConfig()
    ingested: list[IngestedDocument] = []
    evidence: list[InvestigationEvidence] = []
    entities: list[SapEntity] = []
    seen_ids: set[str] = set()
    total_chars = 0

    for source in materialized:
        if source.document_id in seen_ids:
            continue
        if total_chars + len(source.content) > max_total_content_chars:
            raise ValueError(
                f"aggregate content exceeds max_total_content_chars={max_total_content_chars}"
            )
        item = ingest_document(source, config=settings)
        if len(evidence) + len(item.evidence) > max_total_evidence:
            raise ValueError(
                f"aggregate evidence exceeds max_total_evidence={max_total_evidence}"
            )
        seen_ids.add(source.document_id)
        total_chars += len(source.content)
        ingested.append(item)
        evidence.extend(item.evidence)
        entities.extend(item.entities)

    return MultiDocumentIngestion(
        documents=tuple(ingested),
        evidence=tuple(evidence),
        entities=tuple(entities),
    )
