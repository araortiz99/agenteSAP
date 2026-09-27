from src.tools.generate_document import (
    DocumentGenerationError,
    generate_document,
)


class FakeGitHubClient:
    def __init__(self, files):
        self.files = files

    def get_tree(self, ref="main"):
        return [{"path": path, "type": "blob"} for path in self.files]

    def get_file(self, path, ref="main"):
        return self.files[path]


def test_generate_analysis_from_ticket_context():
    client = FakeGitHubClient(
        {
            "templates/analysis.md": "# Análisis template",
            "tickets/31426/ticket.md": """---
ticket_id: "31426"
---

# Ticket 31426

- El objeto funcional mencionado es ZMM_IMX_0004.
- El escenario corresponde a SNC K1.
""",
            "knowledge/relationships/rel-001.md": """---
source_id: "31426"
source_type: "TICKET"
relation_type: "relacionado_con"
target_id: "ZMM_IMX_0004"
target_type: "SAP_OBJECT"
---

# Relationship
""",
        }
    )

    result = generate_document(
        client,
        "analysis",
        "Generá el análisis del ticket 31426.",
        "31426",
        date="2026-09-27",
        author="test",
    )

    assert result.document_type == "analysis"
    assert result.ticket_id == "31426"
    assert result.version == "1.0"
    assert result.status == "draft"
    assert "ZMM_IMX_0004" in result.content
    assert "No se generan hipótesis automáticamente" in result.content
    assert "templates/analysis.md" in result.source_paths


def test_generate_document_rejects_unknown_type():
    client = FakeGitHubClient({})

    try:
        generate_document(client, "unknown", "Generá el documento.")
    except DocumentGenerationError as exc:
        assert "Unsupported document_type" in str(exc)
    else:
        raise AssertionError("Expected DocumentGenerationError")


def test_generate_non_analysis_does_not_invent_content():
    client = FakeGitHubClient(
        {
            "templates/functional-specification.md": "# Especificación Funcional template",
        }
    )

    result = generate_document(
        client,
        "functional-specification",
        "Generá una especificación funcional.",
        "31426",
    )

    assert result.document_type == "functional-specification"
    assert "Información pendiente" in result.content
    assert result.source_paths == ("templates/functional-specification.md",)
