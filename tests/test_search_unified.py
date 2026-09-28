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


def test_unified_search_reserves_requested_layers(monkeypatch):
    from src.tools.search_unified import UnifiedResult
    import src.tools.search_unified as module

    standard = UnifiedResult(
        "sap.md", 0.95, ("x",), "standard", "sap_standard", "content",
        "SAP-1", "standard", "global", "confirmed"
    )
    internal = UnifiedResult(
        "int.md", 0.90, ("x",), "internal", "internal", "content",
        "INT-1", "custom", "org", "confirmed"
    )

    monkeypatch.setattr(module, "search_sap_standard", lambda *args, **kwargs: [
        type("R", (), {"path": "sap.md", "score": 0.95, "matched_terms": ("x",), "match_type": "content", "content": """---
knowledge_type: standard
source_id: SAP-1
certainty: confirmed
---
standard"""})()
    ])
    monkeypatch.setattr(module, "search_knowledge", lambda *args, **kwargs: [
        type("R", (), {"path": "int.md", "score": 0.90, "matched_terms": ("x",), "match_type": "content", "content": """---
knowledge_type: custom
source_id: INT-1
certainty: confirmed
---
internal"""})()
    ])

    result = module.search_unified(object(), "¿Cómo funciona el inventario?", max_results=2)
    assert {item.source_layer for item in result.results} == {"sap_standard", "internal"}


def test_evidence_does_not_count_truncated_source_as_retrieved():
    from src.tools.evidence import assess_evidence
    from src.tools.search_unified import UnifiedResult, UnifiedSearchResult

    internal = UnifiedResult(
        "int.md", 1.0, ("x",), "internal", "internal", "content",
        "INT-1", "custom", "org", "partial"
    )
    hidden_standard = UnifiedResult(
        "sap.md", 0.9, ("x",), "standard", "sap_standard", "content",
        "SAP-1", "standard", "global", "confirmed"
    )
    retrieval = UnifiedSearchResult(
        "¿Cómo funciona el inventario?",
        (internal,),
        (hidden_standard,),
        (internal,),
    )
    assessment = assess_evidence(retrieval)
    assert "sap_standard" not in {item.source_layer for item in assessment.items}
    assert "No SAP Standard evidence was retrieved." in assessment.gaps


def test_unified_search_excludes_external_mcp_for_runtime_queries():
    from src.tools.search_unified import UnifiedResult, _merge_evidence_results

    runtime = UnifiedResult(
        "runtime://qas", 0.9, ("actual",), "runtime", "mcp", "mcp",
        "QAS-1", "runtime_observation", "runtime", "partial"
    )
    external = UnifiedResult(
        "mcp://sap-devs/search", 0.99, ("actual",), "developer context", "mcp", "mcp",
        "DEV-1", "developer_context", "external", "external_source"
    )

    selected = _merge_evidence_results(
        [], [], [runtime, external],
        requested=("runtime",), max_results=2,
    )

    assert selected == [runtime]
