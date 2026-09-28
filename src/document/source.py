"""Deterministic, transport-neutral document source contracts."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from enum import Enum


class DocumentStatus(str, Enum):
    AVAILABLE = "AVAILABLE"
    PROCESSING = "PROCESSING"
    FAILED = "FAILED"
    DUPLICATE = "DUPLICATE"
    SUPERSEDED = "SUPERSEDED"


@dataclass(frozen=True)
class DocumentSource:
    source_id: str
    filename: str
    content: str
    media_type: str | None = None
    metadata: tuple[tuple[str, str], ...] = ()

    def __post_init__(self) -> None:
        if not self.source_id.strip():
            raise ValueError("source_id must not be empty")
        if not self.filename.strip():
            raise ValueError("filename must not be empty")
        if not isinstance(self.content, str):
            raise TypeError("content must be text")

    @property
    def content_hash(self) -> str:
        return hashlib.sha256(self.content.encode("utf-8")).hexdigest()

    @property
    def document_id(self) -> str:
        return "DOC-" + self.content_hash[:16].upper()

    @property
    def size(self) -> int:
        return len(self.content.encode("utf-8"))

    @property
    def file_type(self) -> str:
        name = self.filename.rsplit("/", 1)[-1]
        return name.rsplit(".", 1)[-1].lower() if "." in name else "txt"


def build_document_identity(content: str) -> tuple[str, str]:
    if not isinstance(content, str):
        raise TypeError("content must be text")
    digest = hashlib.sha256(content.encode("utf-8")).hexdigest()
    return "DOC-" + digest[:16].upper(), digest
