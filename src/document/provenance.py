from dataclasses import dataclass
from src.document.chunking import DocumentChunk

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

def chunk_to_record(chunk: DocumentChunk, filename: str) -> DocumentRecord:
    p = Provenance(chunk.document_id, chunk.chunk_id, filename, chunk.sequence, chunk.heading)
    return DocumentRecord("REC-DOC-" + chunk.chunk_id[4:], chunk.content, p)
