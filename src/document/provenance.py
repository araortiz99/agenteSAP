from dataclasses import dataclass

from src.document.chunking import DocumentChunk
from src.knowledge.authority import (
    AuthorityRecord,
    KnowledgeAuthority,
    KnowledgeOrigin,
    build_authority_record,
)


@dataclass(frozen=True)
class Provenance:
    document_id: str
    chunk_id: str
    filename: str
    sequence: int
    heading: str | None


@dataclass(frozen=True)
class DocumentRecord:
    record_id: str
    content: str
    provenance: Provenance
    authority: AuthorityRecord


def chunk_to_record(
    chunk: DocumentChunk,
    filename: str,
    *,
    authority: AuthorityRecord | None = None,
) -> DocumentRecord:
    p = Provenance(
        chunk.document_id,
        chunk.chunk_id,
        filename,
        chunk.sequence,
        chunk.heading,
    )
    record_id = "REC-DOC-" + chunk.chunk_id[4:]
    record_authority = authority or build_authority_record(
        source_id=chunk.document_id,
        content=chunk.content,
        version="1.0",
        authority=KnowledgeAuthority.CANDIDATE,
        origin=KnowledgeOrigin.BUSINESS_DOCUMENT,
        scope="unknown",
        title=filename,
        source_path=filename,
    )
    return DocumentRecord(record_id, chunk.content, p, record_authority)
