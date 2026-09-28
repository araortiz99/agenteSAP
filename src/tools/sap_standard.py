"""SAP Standard Knowledge retrieval helpers.

The MVP keeps SAP documentation separate from organization-specific knowledge.
This module is intentionally read-only: it retrieves already ingested SAP
Standard documents from the repository and applies controlled metadata filters.
"""

from __future__ import annotations

from dataclasses import dataclass

from src.github.client import GitHubClient


SAP_STANDARD_ROOT = "knowledge/sap-standard/"


@dataclass(frozen=True)
class SAPStandardResult:
    path: str
    knowledge_id: str
    product: str
    module: str
    version: str
    certainty: str
    content: str


def _metadata(content: str) -> dict[str, str]:
    if not content.startswith("---"):
        return {}

    result: dict[str, str] = {}
    for line in content.splitlines()[1:]:
        if line.strip() == "---":
            break
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        result[key.strip()] = value.strip().strip('"').strip("'")
    return result


def search_sap_standard(
    client: GitHubClient,
    query: str = "",
    product: str | None = None,
    module: str | None = None,
    version: str | None = None,
    max_results: int = 10,
    ref: str = "main",
) -> list[SAPStandardResult]:
    """Search ingested SAP Standard documents using controlled metadata."""

    if max_results < 1:
        raise ValueError("max_results must be greater than zero")

    terms = [term.lower() for term in query.split() if term.strip()]
    tree = client.get_tree(ref=ref)
    results: list[SAPStandardResult] = []

    for item in tree:
        path = item.get("path", "")
        if not path.startswith(SAP_STANDARD_ROOT) or not path.endswith(".md"):
            continue
        if path.endswith("README.md"):
            continue

        content = client.get_file(path, ref=ref)
        metadata = _metadata(content)

        if metadata.get("knowledge_type") != "standard":
            continue
        if metadata.get("origin") != "sap":
            continue
        if product and metadata.get("product", "").lower() != product.lower():
            continue
        if module and metadata.get("module", "").lower() != module.lower():
            continue
        if version and metadata.get("product_version", "").lower() != version.lower():
            continue

        searchable = content.lower()
        if terms and not all(term in searchable for term in terms):
            continue

        results.append(
            SAPStandardResult(
                path=path,
                knowledge_id=metadata.get("knowledge_id", ""),
                product=metadata.get("product", ""),
                module=metadata.get("module", ""),
                version=metadata.get("product_version", ""),
                certainty=metadata.get("certainty", "unknown"),
                content=content,
            )
        )

    results.sort(key=lambda result: (result.certainty != "confirmed", result.path))
    return results[:max_results]
