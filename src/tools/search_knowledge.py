"""Repository knowledge search capability."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import PurePosixPath

from src.github.client import GitHubClient


SEARCH_ROOTS = (
    "knowledge/",
    "tickets/",
    "standards/",
    "templates/",
    "agent/",
    "promptMaestro",
)

IDENTIFIER_FIELDS = (
    "ticket_id",
    "object_id",
    "process_id",
    "rule_id",
    "relationship_id",
    "source_id",
)


@dataclass(frozen=True)
class SearchResult:
    path: str
    score: float
    matched_terms: tuple[str, ...]
    content: str
    match_type: str = "content"


def _normalize(value: str) -> str:
    return re.sub(r"[^a-z0-9_áéíóúüñ-]+", " ", value.lower())


def _terms(query: str) -> list[str]:
    return [term for term in _normalize(query).split() if len(term) >= 2]


def _is_searchable(path: str) -> bool:
    if path == "promptMaestro":
        return True

    return path.endswith(".md") and path.startswith(SEARCH_ROOTS)


def _parse_front_matter(content: str) -> dict[str, str]:
    """Parse the repository's simple YAML-like front matter."""
    if not content.startswith("---"):
        return {}

    metadata: dict[str, str] = {}
    for line in content.splitlines()[1:]:
        if line.strip() == "---":
            break
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        metadata[key.strip()] = value.strip().strip('"').strip("'")
    return metadata


def _identifier_match(
    content: str, terms: list[str]
) -> tuple[bool, tuple[str, ...]]:
    metadata = _parse_front_matter(content)
    identifiers = {
        _normalize(metadata[field]).strip()
        for field in IDENTIFIER_FIELDS
        if metadata.get(field)
    }
    matched = tuple(term for term in terms if term in identifiers)
    return bool(matched), matched


def _title_match(content: str, terms: list[str]) -> tuple[bool, tuple[str, ...]]:
    title = next(
        (line[2:].strip() for line in content.splitlines() if line.startswith("# ")),
        "",
    )
    normalized = _normalize(title)
    matched = tuple(term for term in terms if term in normalized)
    return bool(matched), matched


def _score(content: str, terms: list[str]) -> tuple[float, tuple[str, ...]]:
    normalized = _normalize(content)
    matched = tuple(term for term in terms if term in normalized)

    if not terms:
        return 0.0, ()

    return len(matched) / len(terms), matched


def _rank_result(
    content: str, terms: list[str], lexical_score: float
) -> tuple[int, float, tuple[str, ...], str]:
    """Rank identifiers above titles and titles above body matches."""
    identifier_found, identifier_terms = _identifier_match(content, terms)
    if identifier_found:
        return 3, 1.0, identifier_terms, "identifier"

    title_found, title_terms = _title_match(content, terms)
    if title_found:
        return 2, lexical_score, title_terms, "title"

    _, content_terms = _score(content, terms)
    return 1, lexical_score, content_terms, "content"


def search_knowledge(
    client: GitHubClient,
    query: str,
    paths: list[str] | None = None,
    max_results: int = 10,
    ref: str = "main",
) -> list[SearchResult]:
    """Search repository text using deterministic relevance tiers.

    Entity identifiers receive the highest relevance, followed by document
    titles and then body-only matches. This keeps direct entity lookups ahead
    of documents that merely mention the same identifier.
    """
    if not query or not query.strip():
        raise ValueError("query must not be empty")

    if max_results < 1:
        raise ValueError("max_results must be greater than zero")

    terms = _terms(query)
    if not terms:
        return []

    allowed_paths = set(paths or [])
    tree = client.get_tree(ref=ref)

    candidates = []
    for item in tree:
        path = item.get("path", "")
        if not _is_searchable(path):
            continue
        if allowed_paths and path not in allowed_paths:
            continue
        candidates.append(path)

    results: list[SearchResult] = []

    for path in candidates:
        content = client.get_file(path, ref=ref)
        lexical_score, _ = _score(content, terms)
        if lexical_score <= 0:
            continue

        _, ranked_score, matched, match_type = _rank_result(
            content, terms, lexical_score
        )
        results.append(
            SearchResult(
                path=path,
                score=ranked_score,
                matched_terms=matched,
                content=content,
                match_type=match_type,
            )
        )

    results.sort(
        key=lambda result: (
            {"identifier": 3, "title": 2, "content": 1}[result.match_type],
            result.score,
            -len(PurePosixPath(result.path).parts),
            result.path,
        ),
        reverse=True,
    )

    return results[:max_results]
