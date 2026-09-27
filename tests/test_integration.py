"""Integration tests for the deterministic SAP agent MVP flow."""

from pathlib import Path

from src.tools.analyze import analyze
from src.tools.generate_document import generate_document
from src.tools.get_related_knowledge import get_related_knowledge
from src.tools.get_ticket import get_ticket
from src.tools.search_knowledge import search_knowledge


FIXTURES = Path(__file__).parent / "fixtures"


class IntegrationGitHubClient:
    """In-memory repository shaped like the production knowledge layout."""

    def __init__(self, fixture_dir: Path):
        self.files = {
            f"tickets/31426/{name}": (fixture_dir / name).read_text(encoding="utf-8")
            for name in ("ticket-31426.md",)
        }
        self.files.update(
            {
                f"knowledge/sap-objects/{name}": (fixture_dir / name).read_text(
                    encoding="utf-8"
                )
                for name in ("sap-object-zmm-imx-0004.md",)
            }
        )
        self.files.update(
            {
                f"knowledge/processes/{name}": (fixture_dir / name).read_text(
                    encoding="utf-8"
                )
                for name in ("process-snc-logistico.md",)
            }
        )
        self.files.update(
            {
                f"knowledge/business-rules/{name}": (fixture_dir / name).read_text(
                    encoding="utf-8"
                )
                for name in ("business-rule-snc.md",)
            }
        )
        self.files.update(
            {
                f"knowledge/relationships/{name}": (fixture_dir / name).read_text(
                    encoding="utf-8"
                )
                for name in (
                    "rel-31426-zmm-imx-0004.md",
                    "rel-zmm-imx-0004-process.md",
                )
            }
        )

        # The production generator retrieves the official template from GitHub.
        for template in (
            "analysis.md",
            "requirement.md",
            "functional-specification.md",
            "functional-tests.md",
            "investigation.md",
        ):
            self.files[f"templates/{template}"] = "# Test template\n"

    def get_tree(self, ref="main"):
        return [
            {"path": path, "type": "blob"}
            for path in sorted(self.files)
        ]

    def get_file(self, path, ref="main"):
        return self.files[path]


def test_end_to_end_retrieval_analysis_and_generation():
    client = IntegrationGitHubClient(FIXTURES)

    search_results = search_knowledge(client, "ZMM_IMX_0004")
    assert search_results
    assert search_results[0].path == "knowledge/sap-objects/sap-object-zmm-imx-0004.md"
    assert search_results[0].match_type == "identifier"

    ticket = get_ticket(client, "31426")
    assert ticket.ticket_id == "31426"
    assert len(ticket.documents) == 1

    relationships = get_related_knowledge(client, "TICKET", "31426")
    assert len(relationships.relationships) == 1
    assert relationships.relationships[0].target_id == "ZMM_IMX_0004"

    analysis = analyze(
        client,
        "Analizar el incidente y la evidencia disponible.",
        "31426",
    )
    assert analysis.ticket_id == "31426"
    assert analysis.facts
    assert len(analysis.relationships.relationships) == 1
    assert not analysis.hypotheses
    assert "must not be inferred" in analysis.conclusion

    document = generate_document(
        client,
        "analysis",
        "Analizar el incidente y generar el documento.",
        "31426",
        date="2026-09-27",
        author="integration-test",
    )
    assert document.document_type == "analysis"
    assert document.ticket_id == "31426"
    assert document.status == "draft"
    assert document.version == "1.0"
    assert "## 4. Hechos identificados" in document.content
    assert "## 5. Evidencias" in document.content
    assert "31426" in document.content
    assert "ZMM_IMX_0004" in document.content
    assert "templates/analysis.md" in document.source_paths


def test_end_to_end_does_not_infer_relationships_from_cooccurrence():
    client = IntegrationGitHubClient(FIXTURES)

    relationships = get_related_knowledge(client, "SAP_OBJECT", "ZMM_IMX_0004")

    target_ids = {r.target_id for r in relationships.relationships}
    source_ids = {r.source_id for r in relationships.relationships}

    assert "ZMM_IMX_0004" not in target_ids
    assert "ZMM_IMX_0004" in source_ids or "ZMM_IMX_0004" in target_ids
    assert all(r.relation_type for r in relationships.relationships)
