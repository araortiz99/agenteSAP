"""Deterministic, read-only SAP Help normalization primitives.

Network crawling is deliberately outside this module. The foundation accepts
already fetched source text plus provenance and produces reproducible chunks.
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import replace

from src.sap_help.model import SAPHelpChunk, SAPHelpDocument, SAPHelpMetadata, validate_metadata


_HEADING_RE = re.compile(r"^(#{1,6})\\s+(.*)$")


def normalize_content(content: str) -> str:
    """Normalize line endings and trailing whitespace without changing meaning."""
    if not isinstance(content, str):
        raise TypeError("content must be a string")
    lines = [line.rstrip() for line in content.replace("\\r\\n", "\\n").replace("\\r", "\\n").split("\\n")]
    return "\\n".join(lines).strip()


def content_hash(content: str) -> str:
    return hashlib.sha256(normalize_content(content).encode("utf-8")).hexdigest()


def _section_path(headings: list[tuple[int, str]], level: int, title: str) -> tuple[str, ...]:
    while headings and headings[-1][0] >= level:
        headings.pop()
    headings.append((level, title))
    return tuple(title for _, title in headings)


def chunk_markdown(document: SAPHelpDocument) -> tuple[SAPHelpChunk, ...]:
    """Chunk Markdown by headings while retaining heading hierarchy."""
    validate_metadata(document.metadata)
    text = normalize_content(document.content)
    if not text:
        return ()

    lines = text.splitlines()
    sections: list[tuple[tuple[str, ...], str | None, str | None, list[str]]] = []
    heading_stack: list[tuple[int, str]] = []
    current_path = document.section_path
    current_heading = document.heading
    current_parent = document.parent_heading
    buffer: list[str] = []

    def flush() -> None:
        nonlocal buffer
        if buffer:
            sections.append((current_path, current_heading, current_parent, buffer))
            buffer = []

    for line in lines:
        match = _HEADING_RE.match(line)
        if not match:
            buffer.append(line)
            continue
        flush()
        level = len(match.group(1))
        title = match.group(2).strip()
        current_path = _section_path(heading_stack, level, title)
        current_heading = title
        current_parent = heading_stack[-2][1] if len(heading_stack) > 1 else None

    flush()
    chunks: list[SAPHelpChunk] = []
    document_id = document.metadata.document_id or content_hash(text)[:16]
    for index, (path, heading, parent, body) in enumerate(sections, start=1):
        chunk_content = "\\n".join(body).strip()
        if not chunk_content:
            continue
        digest = content_hash(chunk_content)
        chunks.append(
            SAPHelpChunk(
                document_id=document_id,
                chunk_id=f"{document_id}:{digest[:16]}",
                section_path=path,
                heading=heading,
                parent_heading=parent,
                source_location=document.metadata.path,
                content=chunk_content,
                content_hash=digest,
                metadata=replace(document.metadata, content_hash=digest),
                entities=document.entities,
            )
        )
    return tuple(chunks)
