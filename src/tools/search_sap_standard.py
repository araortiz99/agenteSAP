"""Search capability for SAP Standard Knowledge.

MVP: deterministic lexical retrieval restricted to knowledge/sap-standard/.
"""

from __future__ import annotations

from dataclasses import dataclass
import re

from src.github.client import GitHubClient


ROOT = "knowledge/sap-standard/"


@dataclass(frozen=True)
class SAPStandardResult:
    path: str
    score: float
    matched_terms: tuple[str, ...]
    content: str


def _terms(query: str) -> list[str]:
    return [x for x in re.sub(r"[^a-z0-9áéíóúüñ-]+", " ", query.lower()).split() if len(x) >= 2]


def search_sap_standard(
    client: GitHubClient,
    query: str,
    max_results: int = 10,
    ref: str = "main",
) -> list[SAPStandardResult]:
    if not query.strip():
        raise ValueError("query must not be empty")
    if max_results < 1:
        raise ValueError("max_results must be greater than zero")

    terms = _terms(query)
    if not terms:
        return []

    results: list[SAPStandardResult] = []
    for item in client.get_tree(ref=ref):
        path = item.get("path", "")
        if not path.startswith(ROOT) or not path.endswith(".md"):
            continue

        content = client.get_file(path, ref=ref)
        normalized = content.lower()
        matched = tuple(term for term in terms if term in normalized)
        if not matched:
            continue

        results.append(
            SAPStandardResult(
                path=path,
                score=len(matched) / len(terms),
                matched_terms=matched,
                content=content,
            )
        )

    results.sort(key=lambda x: (-x.score, x.path))
    return results[:max_results]
