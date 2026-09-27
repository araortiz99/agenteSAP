"""Orchestrate controlled SAP Help ingestion into a staging area."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re

from src.sap.collector import collect_source
from src.sap.metadata import SAPSourceMetadata, build_metadata, render_candidate
from src.sap.parser import parse_html


@dataclass(frozen=True)
class IngestionResult:
    source_id: str
    output_path: Path
    metadata: SAPSourceMetadata


def ingest_source(
    *,
    source_id: str,
    url: str,
    product: str,
    module: str,
    release: str,
    language: str,
    output_dir: Path,
) -> IngestionResult:
    retrieved = collect_source(url)
    title, text = parse_html(retrieved.content)
    metadata = build_metadata(source_id, url, product, module, release, language, text)
    safe_name = re.sub(r"[^a-z0-9-]+", "-", (title or source_id).lower()).strip("-")
    output_path = output_dir / f"{safe_name or source_id.lower()}.md"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render_candidate(metadata, title, text), encoding="utf-8")
    return IngestionResult(source_id, output_path, metadata)
