"""Typed metadata model for official SAP Help evidence.

This module is intentionally source-agnostic: it does not fetch SAP Help and
never invents metadata. Missing fields remain None; inferred fields must be
explicitly marked by metadata_origin.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal


MetadataOrigin = Literal["source", "inferred"]
SAPHelpStatus = Literal["candidate", "validated", "active", "retired"]


@dataclass(frozen=True)
class SAPHelpMetadata:
    source_type: str = "SAP_STANDARD"
    source_system: str = "SAP_HELP"
    repository: str | None = None
    branch: str | None = None
    commit_sha: str | None = None
    path: str | None = None
    document_id: str | None = None
    title: str | None = None
    product: str | None = None
    component: str | None = None
    version: str | None = None
    language: str | None = None
    help_url: str | None = None
    source_url: str | None = None
    last_modified: str | None = None
    retrieved_at: str | None = None
    content_hash: str | None = None
    license: str | None = None
    authority_level: str | None = None
    confidence: str | None = None
    status: SAPHelpStatus = "candidate"
    metadata_origin: MetadataOrigin = "source"


@dataclass(frozen=True)
class SAPHelpDocument:
    metadata: SAPHelpMetadata
    section_path: tuple[str, ...] = ()
    heading: str | None = None
    parent_heading: str | None = None
    content: str = ""
    keywords: tuple[str, ...] = ()
    entities: tuple[str, ...] = ()
    content_hash: str | None = None


@dataclass(frozen=True)
class SAPHelpChunk:
    document_id: str
    chunk_id: str
    section_path: tuple[str, ...]
    heading: str | None
    parent_heading: str | None
    source_location: str | None
    content: str
    content_hash: str
    metadata: SAPHelpMetadata
    entities: tuple[str, ...] = ()
    relationships: tuple[dict[str, str], ...] = field(default_factory=tuple)


def validate_metadata(metadata: SAPHelpMetadata) -> None:
    """Reject invalid identity/provenance combinations without guessing values."""
    if metadata.source_type != "SAP_STANDARD":
        raise ValueError("SAP Help metadata must use source_type=SAP_STANDARD")
    if metadata.source_system != "SAP_HELP":
        raise ValueError("SAP Help metadata must use source_system=SAP_HELP")
    if metadata.metadata_origin not in {"source", "inferred"}:
        raise ValueError("metadata_origin must be source or inferred")
    if metadata.branch and not metadata.repository:
        raise ValueError("branch requires repository provenance")
    if metadata.commit_sha and not metadata.repository:
        raise ValueError("commit_sha requires repository provenance")
    if metadata.path and not metadata.repository:
        raise ValueError("path requires repository provenance")
    if metadata.metadata_origin == "inferred" and not metadata.confidence:
        raise ValueError("inferred metadata requires explicit confidence")
