from pathlib import Path

from src.tools.sap_standard import search_sap_standard


FIXTURES = Path(__file__).parent / "fixtures"


class FakeGitHubClient:
    def __init__(self, fixture_dir: Path):
        self.files = {
            path.relative_to(fixture_dir).as_posix(): path.read_text(encoding="utf-8")
            for path in fixture_dir.glob("*.md")
        }

    def get_tree(self, ref="main"):
        return [
            {"path": f"knowledge/sap-standard/mm/{name}"}
            for name in self.files
            if name.startswith("sap-standard-")
        ]

    def get_file(self, path, ref="main"):
        name = path.removeprefix("knowledge/sap-standard/mm/")
        return self.files[name]


def test_search_sap_standard_filters_standard_sap_knowledge():
    client = FakeGitHubClient(FIXTURES)

    results = search_sap_standard(
        client,
        query="Product Master",
        product="SAP S/4HANA",
        module="MM-IM",
        version="2025 FPS01",
    )

    assert len(results) == 1
    assert results[0].knowledge_id == "fixture-sap-product-master"
    assert results[0].certainty == "confirmed"


def test_search_sap_standard_does_not_return_custom_knowledge():
    client = FakeGitHubClient(FIXTURES)

    results = search_sap_standard(client, query="Product Master")

    assert len(results) == 1
    assert results[0].knowledge_id == "fixture-sap-product-master"
