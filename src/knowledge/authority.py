"""Knowledge Authority Layer.

Defines whether persisted business knowledge may be treated as an
authoritative source. This layer is deliberately separate from retrieval:
retrieval finds evidence; authority determines how strongly that evidence
may be used.
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from enum import Enum


class KnowledgeAuthority(str, Enum):
    CANDIDATE = "candidate"
    REFERENCE = "reference"
    AUTHORITATIVE = "authoritative"
    SUPERSEDED = "superseded"


class KnowledgeOrigin(str, Enum):
    SAP_PUBLIC = "sap_public"
    BUSINESS_DOCUMENT = "business_document"
    TICKET = "ticket"
    GENERATED = "generated"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class AuthorityRecord:
    source_id: str
    content_hash: str
    version: str
    authority: KnowledgeAuthority
    origin: KnowledgeOrigin
    scope: str
    title: str
    source_path: str
    supersedes: str | None = None
    approved_by: str | None = None

    @property
    def reusable_as_truth(self) -> bool:
        return self.authority == KnowledgeAuthority.AUTHORITATIVE

    def validate(self) -> None:
        if not self.source_id.strip():
            raise ValueError("source_id must not be empty")
        if not re.fullmatch(r"[0-9a-f]{64}", self.content_hash):
            raise ValueError("content_hash must be a SHA-256 hex digest")
        if not re.fullmatch(r"d+.d+(?:.d+)?", self.version):
            raise ValueError("version must use MAJOR.MINOR[.PATCH]")
        if not self.title.strip():
            raise ValueError("title must not be empty")
        if not self.source_path.strip():
            raise ValueError("source_path must not be empty")
        if self.authority == KnowledgeAuthority.AUTHORITATIVE:
            if not self.approved_by or not self.approved_by.strip():
                raise ValueError(
                    "authoritative knowledge requires explicit approved_by"
                )
        if self.authority == KnowledgeAuthority.SUPERSEDED and not self.supersedes:
            raise ValueError("superseded knowledge requires supersedes")

    def metadata(self) -> dict[str, str]:
        self.validate()
        result = {
            "source_id": self.source_id,
            "content_hash": self.content_hash,
            "version": self.version,
            "authority": self.authority.value,
            "origin": self.origin.value,
            "scope": self.scope,
            "title": self.title,
            "source_path": self.source_path,
            "reusable_as_truth": str(self.reusable_as_truth).lower(),
        }
        if self.supersedes:
            result["supersedes"] = self.supersedes
        if self.approved_by:
            result["approved_by"] = self.approved_by
        return result


def content_hash(content: str) -> str:
    if not isinstance(content, str):
        raise TypeError("content must be text")
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def build_authority_record(
    *,
    source_id: str,
    content: str,
    version: str,
    authority: KnowledgeAuthority,
    origin: KnowledgeOrigin,
    scope: str,
    title: str,
    source_path: str,
    supersedes: str | None = None,
    approved_by: str | None = None,
) -> AuthorityRecord:
    record = AuthorityRecord(
        source_id=source_id,
        content_hash=content_hash(content),
        version=version,
        authority=authority,
        origin=origin,
        scope=scope,
        title=title,
        source_path=source_path,
        supersedes=supersedes,
        approved_by=approved_by,
    )
    record.validate()
    return record


def can_promote_to_authoritative(
    *,
    origin: KnowledgeOrigin,
    version: str,
    approved_by: str | None,
    has_provenance: bool,
    has_security_review: bool,
) -> bool:
    """Return whether a document satisfies the minimum truth-source gate.

    Generated knowledge can never become authoritative through this helper.
    Human approval, provenance and security review are mandatory.
    """
    if origin == KnowledgeOrigin.GENERATED:
        return False
    if not approved_by or not approved_by.strip():
        return False
    if not has_provenance or not has_security_review:
        return False
    return bool(re.fullmatch(r"d+.d+(?:.d+)?", version))
