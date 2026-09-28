from pathlib import Path

from src.tools.search_knowledge import _score, search_knowledge


FIXTURES = Path(__file__).parent / "fixtures"


class FakeGitHubClient:
    """Minimal in-memory client used to test retrieval without network access."""

    def __init__(self, fixture_dir: Path):
        self.files = {
            path.relative_to(fixture_dir).as_posix(): path.read_text(encoding="utf-8")
            for path in fixture_dir.glob("*.md")
        }

    def get_tree(self, ref="main"):
        return [{"path": f"knowledge/test-fixtures/{name}"} for name in self.files]

    def get_file(self, path, ref="main"):
        name = path.removeprefix("knowledge/test-fixtures/")
        return self.files[name]


def test_score_matches_terms():
    score, matched = _score(
        "ZMM_IMX_0004 genera documentos SNC y utiliza K4",
        ["zmm_imx_0004", "snc"],
    )

    assert score == 1.0
    assert matched == ("zmm_imx_0004", "snc")


def test_score_ignores_missing_terms():
    score, matched = _score(
        "Documento funcional de SNC",
        ["snc", "zmm_imx_0004"],
    )

    assert score == 0.5
    assert matched == ("snc",)


def test_search_finds_object_fixture():
    client = FakeGitHubClient(FIXTURES)

    results = search_knowledge(
        client,
        "ZMM_IMX_0004",
        paths=[
            "knowledge/test-fixtures/sap-object-zmm-imx-0004.md",
            "knowledge/test-fixtures/ticket-31426.md",
            "knowledge/test-fixtures/ticket-33007.md",
            "knowledge/test-fixtures/process-snc-logistico.md",
            "knowledge/test-fixtures/business-rule-snc.md",
        ],
    )

    assert results
    assert results[0].path == "knowledge/test-fixtures/sap-object-zmm-imx-0004.md"
    assert results[0].match_type == "identifier"
    assert "zmm_imx_0004" in results[0].matched_terms


def test_search_finds_ticket_31426_as_direct_entity_match():
    client = FakeGitHubClient(FIXTURES)

    results = search_knowledge(client, "31426")

    assert results
    assert results[0].path == "knowledge/test-fixtures/ticket-31426.md"
    assert results[0].match_type == "identifier"
    assert "31426" in results[0].matched_terms
    assert len(results) > 1


def test_search_finds_snc_logistico_related_fixtures():
    client = FakeGitHubClient(FIXTURES)

    results = search_knowledge(client, "SNC LOGISTICO")

    paths = {result.path for result in results}

    assert "knowledge/test-fixtures/process-snc-logistico.md" in paths
    assert "knowledge/test-fixtures/ticket-31426.md" in paths
    assert "knowledge/test-fixtures/ticket-33007.md" in paths


def test_search_returns_no_results_for_unknown_term():
    client = FakeGitHubClient(FIXTURES)

    results = search_knowledge(client, "ABC_XYZ_999999")

    assert results == []


def test_search_filters_prose_stopwords_from_query_terms():
    client = FakeGitHubClient(FIXTURES)

    results = search_knowledge(
        client,
        "Analizá el ticket 31426 y separá claramente qué está confirmado",
    )

    assert results
    assert results[0].path == "knowledge/test-fixtures/ticket-31426.md"
    assert results[0].match_type == "identifier"
    assert "31426" in results[0].matched_terms
    assert all(term not in {"el", "y", "qué", "está", "separá"} for term in results[0].matched_terms)
\n\ndef test_search_uses_token_boundaries_for_internal_terms():
    client = FakeGitHubClient(FIXTURES)
    client.files["knowledge/test-fixtures/unrelated.md"] = "# Unrelated\nThe word ticketing is not a ticket."

    results = search_knowledge(client, "ticket")

    assert all(result.path != "knowledge/test-fixtures/unrelated.md" for result in results)
