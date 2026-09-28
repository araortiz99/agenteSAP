from src.tools.search_sap_standard import search_sap_standard


class FakeClient:
    def __init__(self):
        self.files = {
            "knowledge/sap-standard/mm/material-master.md": (
                "# Material Master\n"
                "SAP S/4HANA Materials Management material master data."
            ),
            "knowledge/custom/process.md": "# Custom process\nLocal process.",
        }

    def get_tree(self, ref="main"):
        return [{"path": p} for p in self.files]

    def get_file(self, path, ref="main"):
        return self.files[path]


def test_search_is_restricted_to_sap_standard():
    results = search_sap_standard(FakeClient(), "material master")
    assert len(results) == 1
    assert results[0].path == "knowledge/sap-standard/mm/material-master.md"


def test_empty_query_rejected():
    try:
        search_sap_standard(FakeClient(), "")
    except ValueError:
        return
    raise AssertionError("empty query should raise ValueError")


def test_standard_retrieval_filters_generic_prose_and_preserves_short_sap_terms():
    client = FakeClient()
    client.files["knowledge/sap-standard/mm/other.md"] = (
        "---\n"
        "source_id: SAP-OTHER\n"
        "transaction: MIGO\n"
        "---\n"
        "# Other\n"
        "MIGO goods movement."
    )
    results = search_sap_standard(client, "Explicá qué hace MIGO")
    assert results[0].path == "knowledge/sap-standard/mm/other.md"
    assert results[0].match_type == "identifier"
    assert "migo" in results[0].matched_terms
    assert "qué" not in results[0].matched_terms


def test_standard_retrieval_uses_token_boundaries():
    client = FakeClient()
    client.files["knowledge/sap-standard/mm/unrelated.md"] = "# Unrelated\nThis document mentions materialize but not material."

    results = search_sap_standard(client, "material")

    assert all(result.path != "knowledge/sap-standard/mm/unrelated.md" for result in results)
