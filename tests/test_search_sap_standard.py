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
