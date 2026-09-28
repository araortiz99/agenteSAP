"""Document knowledge ingestion primitives."""

from src.document.ingestion import DocumentIngestionConfig, IngestedDocument, ingest_document
from src.document.source import DocumentSource, DocumentStatus, build_document_identity

__all__ = [
    "DocumentIngestionConfig",
    "DocumentSource",
    "DocumentStatus",
    "IngestedDocument",
    "build_document_identity",
    "ingest_document",
]
