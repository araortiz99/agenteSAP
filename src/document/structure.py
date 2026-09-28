from dataclasses import dataclass
from src.document.source import DocumentSource

@dataclass(frozen=True)
class DocumentBlock:
    kind: str
    text: str
    sequence: int
    heading: str | None = None

@dataclass(frozen=True)
class DocumentStructure:
    document_id: str
    blocks: tuple[DocumentBlock, ...]

def parse_text_structure(source: DocumentSource) -> DocumentStructure:
    blocks = []
    for sequence, line in enumerate(source.content.splitlines()):
        text = line.strip()
        if not text:
            continue
        kind = "heading" if text.startswith("#") else "paragraph"
        heading = text.lstrip("#").strip() if kind == "heading" else None
        blocks.append(DocumentBlock(kind, heading or text, sequence, heading))
    return DocumentStructure(source.document_id, tuple(blocks))
