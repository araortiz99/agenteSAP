"""Controlled promotion of SAP Standard candidates into Knowledge."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import hashlib
import re

from src.sap.registry import SourceRegistry


REQUIRED_FIELDS = (
    "knowledge_type",
    "knowledge_scope",
    "source_id",
    "source_type",
    "origin",
    "product",
    "module",
    "release",
    "language",
    "certainty",
    "status",
    "source_url",
    "retrieved_at",
    "checksum_sha256",
)


@dataclass(frozen=True)
class PromotionResult:
    source_id: str
    output_path: Path
    previous_status: str
    status: str
    certainty: str
    checksum_sha256: str


class PromotionError(ValueError):
    """Raised when a candidate cannot be promoted safely."""


def _front_matter(content: str) -> dict[str, str]:
    if not content.startswith("---\n"):
        raise PromotionError("candidate must start with YAML front matter")
    parts = content.split("\n---\n", 1)
    if len(parts) != 2:
        raise PromotionError("invalid front matter")
    fields: dict[str, str] = {}
    for line in parts[0][4:].splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip().strip('"')
    return fields


def _validate_candidate(content: str, registry: SourceRegistry) -> dict[str, str]:
    fields = _front_matter(content)
    missing = [field for field in REQUIRED_FIELDS if not fields.get(field)]
    if missing:
        raise PromotionError("missing metadata: " + ", ".join(missing))

    if fields["status"] != "candidate":
        raise PromotionError("only status=candidate can be promoted")

    if fields["certainty"] != "under_validation":
        raise PromotionError("candidate must have certainty=under_validation")

    source = registry.get(fields["source_id"])
    if source.status != "active":
        raise PromotionError(f"source is not active: {source.source_id}")

    if fields["source_url"] != source.url:
        raise PromotionError("candidate URL does not match the registered source")

    if fields["product"] != source.product:
        raise PromotionError("candidate product does not match the registry")

    if fields["module"] != source.module:
        raise PromotionError("candidate module does not match the registry")

    if fields["release"] != source.release:
        raise PromotionError("candidate release does not match the registry")

    if fields["language"] != source.language:
        raise PromotionError("candidate language does not match the registry")

    if fields["knowledge_type"] != "standard":
        raise PromotionError("SAP Standard promotion requires knowledge_type=standard")

    if fields["source_type"] != "sap_documentation" or fields["origin"] != "sap":
        raise PromotionError("candidate must originate from SAP documentation")

    if not re.search(r"^# .+", content, re.MULTILINE):
        raise PromotionError("candidate must contain a title")

    if "CANDIDATE — REQUIRES VALIDATION" not in content:
        raise PromotionError("candidate marker is missing")

    return fields


def promote_candidate(
    *,
    candidate_path: Path,
    destination_dir: Path,
    registry: SourceRegistry,
) -> PromotionResult:
    content = candidate_path.read_text(encoding="utf-8")
    fields = _validate_candidate(content, registry)

    body = content.split("\n---\n", 1)[1]
    body = body.replace("> **CANDIDATE — REQUIRES VALIDATION**\n\n", "", 1)

    checksum = hashlib.sha256(body.encode("utf-8")).hexdigest()
    if checksum != fields["checksum_sha256"]:
        # The ingestion checksum covers parsed source text, not the rendered Markdown body.
        # Recompute from the source text marker instead of silently accepting a mismatch.
        source_text = body.split("\n\n", 1)[1] if "\n\n" in body else body
        source_checksum = hashlib.sha256(source_text.encode("utf-8")).hexdigest()
        if source_checksum != fields["checksum_sha256"]:
            raise PromotionError("candidate checksum does not match its content")

    promoted = re.sub(
        r"^certainty: .*$",
        "certainty: confirmed",
        content,
        flags=re.MULTILINE,
    )
    promoted = re.sub(
        r"^status: .*$",
        "status: validated",
        promoted,
        flags=re.MULTILINE,
    )
    promoted = promoted.replace("> **CANDIDATE — REQUIRES VALIDATION**\n\n", "", 1)

    source_id = fields["source_id"]
    safe_name = re.sub(r"[^a-z0-9-]+", "-", source_id.lower()).strip("-")
    output_path = destination_dir / f"{safe_name}.md"
    destination_dir.mkdir(parents=True, exist_ok=True)

    if output_path.exists():
        existing = output_path.read_text(encoding="utf-8")
        existing_fields = _front_matter(existing)
        if existing_fields.get("checksum_sha256") == fields["checksum_sha256"]:
            raise PromotionError("equivalent knowledge already exists")
        raise PromotionError("destination already contains a different version")

    output_path.write_text(promoted, encoding="utf-8")
    return PromotionResult(
        source_id=source_id,
        output_path=output_path,
        previous_status="candidate",
        status="validated",
        certainty="confirmed",
        checksum_sha256=fields["checksum_sha256"],
    )
