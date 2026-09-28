"""Compact deterministic investigation case identifiers."""

from __future__ import annotations

from datetime import date
import hashlib


def build_case_id(question: str, *, day: date | None = None) -> str:
    if not question or not question.strip():
        raise ValueError("question must not be empty")
    current_day = day or date.today()
    digest = hashlib.sha256(question.strip().lower().encode("utf-8")).hexdigest()[:4].upper()
    return f"INV-{current_day:%Y%m%d}-{digest}"
