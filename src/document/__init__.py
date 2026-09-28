"""Document knowledge ingestion primitives."""

from src.document.file_input import SUPPORTED_TEXT_TYPES, load_document_file
from src.document.ingestion import DocumentIngestionConfig, IngestedDocument, ingest_document
from src.document.source import DocumentSource, DocumentStatus, build_document_identity

__all__ = [
    "DocumentIngestionConfig",
    "DocumentSource",
    "DocumentStatus",
    "IngestedDocument",
    "SUPPORTED_TEXT_TYPES",
    "build_document_identity",
    "ingest_document",
    "load_document_file",
]
