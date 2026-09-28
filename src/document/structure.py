"""Deterministic document structure parsing with heading context."""

from __future__ import annotations

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
    """Parse line-oriented text while preserving the active heading context."""
    blocks: list[DocumentBlock] = []
    active_heading: str | None = None

    for sequence, line in enumerate(source.content.splitlines()):
        text = line.strip()
        if not text:
            continue

        if text.startswith("#"):
            active_heading = text.lstrip("#").strip()
            if not active_heading:
                continue
            blocks.append(
                DocumentBlock(
                    kind="heading",
                    text=active_heading,
                    sequence=sequence,
                    heading=active_heading,
                )
            )
            continue

        blocks.append(
            DocumentBlock(
                kind="paragraph",
                text=text,
                sequence=sequence,
                heading=active_heading,
            )
        )

    return DocumentStructure(source.document_id, tuple(blocks))
