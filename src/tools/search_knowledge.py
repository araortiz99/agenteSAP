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


@dataclass(frozen=True)
class SearchResult:
    path: str
    score: float
    matched_terms: tuple[str, ...]
    content: str


def _normalize(value: str) -> str:
    return re.sub(r"[^a-z0-9_áéíóúüñ-]+", " ", value.lower())


def _terms(query: str) -> list[str]:
    return [term for term in _normalize(query).split() if len(term) >= 2]


def _is_searchable(path: str) -> bool:
    if path == "promptMaestro":
        return True

    return (
        path.endswith(".md")
        and path.startswith(SEARCH_ROOTS)
    )


def _score(content: str, terms: list[str]) -> tuple[float, tuple[str, ...]]:
    normalized = _normalize(content)
    matched = tuple(term for term in terms if term in normalized)

    if not terms:
        return 0.0, ()

    return len(matched) / len(terms), matched


def search_knowledge(
    client: GitHubClient,
    query: str,
    paths: list[str] | None = None,
    max_results: int = 10,
    ref: str = "main",
) -> list[SearchResult]:
    """Search repository text and return the most relevant matches.

    This is a deterministic lexical MVP. Semantic retrieval can be added later
    without changing the capability contract.
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
        score, matched = _score(content, terms)

        if score > 0:
            results.append(
                SearchResult(
                    path=path,
                    score=score,
                    matched_terms=matched,
                    content=content,
                )
            )

    results.sort(
        key=lambda result: (
            result.score,
            -len(PurePosixPath(result.path).parts),
        ),
        reverse=True,
    )

    return results[:max_results]
