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
        return [{"path": f"tests/fixtures/{name}"} for name in self.files]

    def get_file(self, path, ref="main"):
        name = path.removeprefix("tests/fixtures/")
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
            "tests/fixtures/sap-object-zmm-imx-0004.md",
            "tests/fixtures/ticket-31426.md",
            "tests/fixtures/ticket-33007.md",
            "tests/fixtures/process-snc-logistico.md",
            "tests/fixtures/business-rule-snc.md",
        ],
    )

    assert results
    assert results[0].path == "tests/fixtures/sap-object-zmm-imx-0004.md"
    assert "zmm_imx_0004" in results[0].matched_terms


def test_search_finds_ticket_31426():
    client = FakeGitHubClient(FIXTURES)

    results = search_knowledge(client, "31426")

    assert len(results) == 1
    assert results[0].path == "tests/fixtures/ticket-31426.md"


def test_search_finds_snc_logistico_related_fixtures():
    client = FakeGitHubClient(FIXTURES)

    results = search_knowledge(client, "SNC LOGISTICO")

    paths = {result.path for result in results}

    assert "tests/fixtures/process-snc-logistico.md" in paths
    assert "tests/fixtures/ticket-31426.md" in paths
    assert "tests/fixtures/ticket-33007.md" in paths


def test_search_returns_no_results_for_unknown_term():
    client = FakeGitHubClient(FIXTURES)

    results = search_knowledge(client, "ABC_XYZ_999999")

    assert results == []
