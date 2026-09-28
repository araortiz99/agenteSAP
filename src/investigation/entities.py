"""Deterministic extraction of SAP investigation entities from user language."""

from __future__ import annotations

import re

from src.investigation.contracts import InvestigationEntity


_PATTERNS: tuple[tuple[str, str], ...] = (
    ("material", r"\bmaterial\s+(?:n(?:ro|úmero|umero)?\s*)?(\d{3,18})\b"),
    ("plant", r"\bcentro\s+(?:n(?:ro|úmero|umero)?\s*)?(\d{3,8})\b"),
    ("storage_location", r"\balmac[eé]n\s+(?:n(?:ro|úmero|umero)?\s*)?([A-Z0-9_-]{2,10})\b"),
    ("movement_type", r"\b(?:tipo\s+de\s+movimiento|movimiento)\s+(\d{3})\b"),
    ("material_document", r"\b(?:documento\s+de\s+material|doc(?:umento)?\s+material)\s+(\d{6,16})\b"),
)

def extract_entities(question: str) -> tuple[InvestigationEntity, ...]:
    if not question or not question.strip():
        raise ValueError("question must not be empty")
    entities: list[InvestigationEntity] = []
    for entity_type, pattern in _PATTERNS:
        match = re.search(pattern, question, re.IGNORECASE)
        if match:
            entities.append(
                InvestigationEntity(
                    entity_type=entity_type,
                    value=match.group(1).upper(),
                )
            )
    return tuple(entities)


def missing_required_entities(entities: tuple[InvestigationEntity, ...]) -> tuple[str, ...]:
    present = {item.entity_type for item in entities}
    return tuple(name for name in ("material", "plant") if name not in present)
