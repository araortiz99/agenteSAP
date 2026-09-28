"""Validation and proposal building for persistent Knowledge changes."""

from __future__ import annotations

from dataclasses import dataclass
import re


ALLOWED_ROOTS = ("knowledge/",)
FORBIDDEN_ROOTS = ("standards/", "templates/", "agent/", "tickets/", ".github/")
REQUIRED_METADATA = (
    "ticket_id", "document_type", "knowledge_type", "knowledge_scope",
    "version", "status", "date", "author",
)
ALLOWED_STATUSES = {"draft", "in_review", "approved", "validated", "implemented", "obsolete"}
SECRET_PATTERNS = (
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"(?i)\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9_]{20,}\b"),
    re.compile(r"(?i)\bgithub_pat_[A-Za-z0-9_]{20,}\b"),
    re.compile(r"(?i)\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"(?i)\bBearer\s+[A-Za-z0-9._-]{20,}\b"),
)


@dataclass(frozen=True)
class KnowledgeChangeProposal:
    path: str
    operation: str
    base_ref: str
    branch: str
    ticket_id: str | None
    old_version: str | None
    new_version: str
    status: str
    source_paths: tuple[str, ...]
    content: str
    change_type: str


class KnowledgeChangeError(ValueError):
    """Raised when a Knowledge change is unsafe or structurally invalid."""


def _strip_bom(content: str) -> str:
    return content.lstrip("\ufeff")


def _metadata(content: str) -> dict[str, str]:
    content = _strip_bom(content)
    if not content.startswith("---"):
        return {}
    values: dict[str, str] = {}
    for line in content.splitlines()[1:]:
        if line.strip() == "---":
            break
        if ":" in line:
            key, value = line.split(":", 1)
            values[key.strip()] = value.strip().strip('"').strip("'")
    return values


def _version_tuple(version: str) -> tuple[int, ...]:
    match = re.fullmatch(r"(\d+)\.(\d+)(?:\.(\d+))?", version.strip())
    if not match:
        raise KnowledgeChangeError(
            f"Invalid knowledge version '{version}'. Expected MAJOR.MINOR[.PATCH]."
        )
    return tuple(int(part) for part in match.groups() if part is not None)


def validate_path(path: str) -> None:
    normalized = path.strip().replace("\\", "/").lstrip("/")
    if any(normalized.startswith(root) for root in FORBIDDEN_ROOTS):
        raise KnowledgeChangeError(f"Path is not publishable by Knowledge Governance: {path}")
    if not any(normalized.startswith(root) for root in ALLOWED_ROOTS):
        raise KnowledgeChangeError(f"Knowledge publication requires a path under knowledge/: {path}")
    if not normalized.endswith(".md"):
        raise KnowledgeChangeError("Only Markdown Knowledge files are publishable")


def validate_security(content: str) -> None:
    for pattern in SECRET_PATTERNS:
        if pattern.search(content):
            raise KnowledgeChangeError(
                "Potential secret detected. Correct or sanitize the content before publication."
            )


def validate_document(content: str) -> dict[str, str]:
    metadata = _metadata(content)
    missing = [key for key in REQUIRED_METADATA if not metadata.get(key, "").strip()]
    if missing:
        raise KnowledgeChangeError(f"Missing required Knowledge metadata: {', '.join(missing)}")
    if metadata["knowledge_type"] not in {"standard", "custom", "mixed", "unknown"}:
        raise KnowledgeChangeError("Invalid knowledge_type")
    if metadata["status"] not in ALLOWED_STATUSES:
        raise KnowledgeChangeError("Invalid status")
    _version_tuple(metadata["version"])
    validate_security(content)
    return metadata


def build_change_proposal(
    *, path: str, content: str, base_ref: str, branch: str,
    ticket_id: str | None = None, existing_content: str | None = None,
    source_paths: tuple[str, ...] = (), change_type: str = "minor",
) -> KnowledgeChangeProposal:
    validate_path(path)
    if not base_ref.strip():
        raise KnowledgeChangeError("base_ref must not be empty")
    if branch.strip() == base_ref.strip():
        raise KnowledgeChangeError("branch must differ from base_ref")
    if branch.strip() in {"main", "master"}:
        raise KnowledgeChangeError("Protected branch cannot be the change branch")

    metadata = validate_document(content)
    proposed_ticket = ticket_id or metadata.get("ticket_id") or None
    old_version = None
    operation = "create"

    if existing_content is not None:
        old_metadata = validate_document(existing_content)
        old_version = old_metadata["version"]
        operation = "update"
        if _version_tuple(metadata["version"]) <= _version_tuple(old_version):
            raise KnowledgeChangeError(
                f"New version {metadata['version']} must be greater than existing version {old_version}"
            )

    if change_type not in {"patch", "minor", "major"}:
        raise KnowledgeChangeError("change_type must be patch, minor or major")

    return KnowledgeChangeProposal(
        path=path.strip().replace("\\", "/").lstrip("/"),
        operation=operation,
        base_ref=base_ref.strip(),
        branch=branch.strip(),
        ticket_id=proposed_ticket,
        old_version=old_version,
        new_version=metadata["version"],
        status=metadata["status"],
        source_paths=tuple(dict.fromkeys(source_paths)),
        content=content,
        change_type=change_type,
    )
