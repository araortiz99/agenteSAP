from src.tools.search_unified import search_unified


class UnifiedFakeClient:
    def __init__(self):
        self.files = {
            "knowledge/sap-standard/mm/material-master.md": """---
knowledge_type: standard
knowledge_scope: global
source_id: SAP-HELP-TEST
certainty: confirmed
---
# Material Master
SAP material master standard information.
""",
            "knowledge/custom/material-process.md": """---
knowledge_type: custom
knowledge_scope: organization
source_id: INT-MATERIAL-001
certainty: confirmed
---
# Material Master Process
Our organization uses a custom material master process.
""",
        }

    def get_tree(self, ref="main"):
        return [{"path": path, "type": "blob"} for path in self.files]

    def get_file(self, path, ref="main"):
        return self.files[path]


def test_unified_search_preserves_source_layers():
    result = search_unified(UnifiedFakeClient(), "material master")

    assert result.sap_standard
    assert result.internal
    assert result.sap_standard[0].source_layer == "sap_standard"
    assert result.internal[0].source_layer == "internal"
    assert result.sap_standard[0].knowledge_type == "standard"
    assert result.internal[0].knowledge_type == "custom"
    assert result.internal[0].knowledge_scope == "organization"


def test_unified_search_requires_query():
    try:
        search_unified(UnifiedFakeClient(), "")
    except ValueError:
        return
    raise AssertionError("empty query should raise ValueError")
