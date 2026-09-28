"""Metadata and staging helpers for SAP Standard ingestion."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib


@dataclass(frozen=True)
class SAPSourceMetadata:
    source_id: str
    url: str
    product: str
    module: str
    release: str
    language: str
    retrieved_at: str
    checksum_sha256: str
    source_text: str = ""
    status: str = "candidate"
    knowledge_type: str = "standard"
    knowledge_scope: str = "global"
    source_type: str = "sap_documentation"
    certainty: str = "under_validation"


def build_metadata(
    source_id: str,
    url: str,
    product: str,
    module: str,
    release: str,
    language: str,
    content: str,
) -> SAPSourceMetadata:
    checksum = hashlib.sha256(content.encode("utf-8")).hexdigest()
    return SAPSourceMetadata(
        source_id=source_id,
        url=url,
        product=product,
        module=module,
        release=release,
        language=language,
        retrieved_at=datetime.now(timezone.utc).isoformat(),
        checksum_sha256=checksum,
    )


def render_candidate(metadata: SAPSourceMetadata, title: str, text: str) -> str:
    """Render a reviewable candidate; it is not confirmed knowledge yet."""
    return f'''---
knowledge_type: {metadata.knowledge_type}
knowledge_scope: {metadata.knowledge_scope}
source_id: {metadata.source_id}
source_type: {metadata.source_type}
origin: sap
product: {metadata.product}
module: {metadata.module}
release: "{metadata.release}"
language: {metadata.language}
certainty: {metadata.certainty}
status: {metadata.status}
source_url: {metadata.url}
retrieved_at: {metadata.retrieved_at}
checksum_sha256: {metadata.checksum_sha256}
source_text_sha256: {metadata.checksum_sha256}
---

# {title or metadata.source_id}

> **CANDIDATE — REQUIRES VALIDATION**

{text}
'''
