"""Read-only local file intake for document knowledge ingestion."""

from __future__ import annotations

from pathlib import Path

from src.document.source import DocumentSource

SUPPORTED_TEXT_TYPES = frozenset({"txt", "md", "csv"})


def load_document_file(
    path: str | Path,
    *,
    source_id: str | None = None,
    max_bytes: int = 2_000_000,
) -> DocumentSource:
    """Read one bounded local text file and convert it to DocumentSource.

    No writes are performed. Unsupported/binary formats fail closed.
    """
    file_path = Path(path)
    if not file_path.is_file():
        raise FileNotFoundError(str(file_path))

    suffix = file_path.suffix.lower().lstrip(".") or "txt"
    if suffix not in SUPPORTED_TEXT_TYPES:
        raise ValueError(
            f"unsupported document type: .{suffix}; "
            f"supported types: {', '.join(sorted(SUPPORTED_TEXT_TYPES))}"
        )

    if max_bytes < 1:
        raise ValueError("max_bytes must be greater than zero")

    size = file_path.stat().st_size
    if size > max_bytes:
        raise ValueError(f"file exceeds max_bytes={max_bytes}")

    content = file_path.read_text(encoding="utf-8")
    media_type = {
        "txt": "text/plain",
        "md": "text/markdown",
        "csv": "text/csv",
    }[suffix]

    return DocumentSource(
        source_id=source_id or file_path.name,
        filename=file_path.name,
        content=content,
        media_type=media_type,
        metadata=(("source", "LOCAL_FILE"),),
    )
