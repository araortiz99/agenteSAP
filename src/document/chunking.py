from dataclasses import dataclass
import hashlib
from src.document.structure import DocumentStructure

@dataclass(frozen=True)
class DocumentChunk:
    chunk_id: str
    document_id: str
    content: str
    sequence: int
    heading: str | None = None

def chunk_document(structure: DocumentStructure, max_chunk_chars: int = 1600, max_chunks: int = 128) -> tuple[DocumentChunk, ...]:
    if max_chunk_chars < 1 or max_chunks < 1:
        raise ValueError("chunk limits must be greater than zero")
    chunks = []
    current = ""
    heading = None
    for block in structure.blocks:
        if block.kind == "heading":
            heading = block.heading
            continue
        parts = [block.text[i:i + max_chunk_chars] for i in range(0, len(block.text), max_chunk_chars)]
        for part in parts:
            if len(chunks) >= max_chunks:
                return tuple(chunks)
            raw = f"{structure.document_id}|{len(chunks)}|{heading or ''}|{part}"
            chunk_id = "CHK-" + hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16].upper()
            chunks.append(DocumentChunk(chunk_id, structure.document_id, part, len(chunks), heading))
    return tuple(chunks)
