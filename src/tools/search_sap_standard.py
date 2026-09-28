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
    match_type: str = "content"


STANDARD_STOPWORDS = frozenset({
    "a", "al", "ante", "con", "como", "de", "del", "el", "en", "es",
    "esta", "está", "este", "la", "las", "lo", "los", "para", "por",
    "que", "qué", "se", "su", "sus", "un", "una", "y",
    "busca", "buscá", "buscar", "explica", "explicá", "explicar",
})

IDENTIFIER_FIELDS = (
    "source_id", "knowledge_id", "document_id", "transaction",
    "table", "cds_view", "movement_type", "app", "object_id",
)

def _terms(query: str) -> list[str]:
    return [
        x
        for x in re.sub(r"[^a-z0-9áéíóúüñ_-]+", " ", query.lower()).split()
        if len(x) >= 2 and x not in STANDARD_STOPWORDS
    ]

def _metadata(content: str) -> dict[str, str]:
    if not content.startswith("---"):
        return {}
    metadata: dict[str, str] = {}
    for line in content.splitlines()[1:]:
        if line.strip() == "---":
            break
        if ":" in line:
            key, value = line.split(":", 1)
            metadata[key.strip()] = value.strip().strip('"').strip("'")
    return metadata

def _rank(content: str, terms: list[str], lexical_score: float):
    metadata = _metadata(content)
    identifiers = {
        value.lower().strip()
        for field in IDENTIFIER_FIELDS
        if (value := metadata.get(field))
    }
    identifier_matches = tuple(term for term in terms if term in identifiers)
    if identifier_matches:
        return 1.0, identifier_matches, "identifier"

    title = next(
        (line[2:].strip().lower() for line in content.splitlines() if line.startswith("# ")),
        "",
    )
    title_matches = tuple(term for term in terms if term in title)
    if title_matches:
        return lexical_score, title_matches, "title"

    return lexical_score, tuple(term for term in terms if term in content.lower()), "content"


def _load_contents(client: GitHubClient, paths: list[str], ref: str) -> dict[str, str]:
    """Use concurrent transport when available; keep test-double compatibility."""
    get_files = getattr(client, "get_files", None)
    if callable(get_files):
        return get_files(paths, ref=ref)

    return {path: client.get_file(path, ref=ref) for path in paths}


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

    paths = [
        item.get("path", "")
        for item in client.get_tree(ref=ref)
        if item.get("path", "").startswith(ROOT)
        and item.get("path", "").endswith(".md")
    ]
    contents = _load_contents(client, paths, ref)

    results: list[SAPStandardResult] = []
    for path in paths:
        content = contents[path]
        normalized = content.lower()
        matched = tuple(term for term in terms if term in normalized)
        if not matched:
            continue

        lexical_score = len(matched) / len(terms)
        score, ranked_terms, match_type = _rank(content, terms, lexical_score)
        results.append(
            SAPStandardResult(
                path=path,
                score=score,
                matched_terms=ranked_terms,
                content=content,
                match_type=match_type,
            )
        )

    results.sort(
        key=lambda x: (
            {"identifier": 3, "title": 2, "content": 1}[x.match_type],
            x.score,
            x.path,
        ),
        reverse=True,
    )
    return results[:max_results]
