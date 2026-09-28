from src.tools.analyze import analyze


class FakeGitHubClient:
    def __init__(self, files):
        self.files = files

    def get_tree(self, ref="main"):
        return [
            {
                "path": path,
                "type": "blob",
            }
            for path in self.files
        ]

    def get_file(self, path, ref="main"):
        return self.files[path]


def test_analyze_retrieves_ticket_facts_and_relationships():
    client = FakeGitHubClient(
        {
            "tickets/31426/ticket.md": """---
ticket_id: "31426"
---

# Ticket 31426

## Hechos

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

    result = analyze(
        client,
        "Analizá el ticket 31426",
        "31426",
    )

    assert result.ticket_id == "31426"
    assert "El objeto funcional mencionado es ZMM_IMX_0004." in result.facts
    assert len(result.relationships.relationships) == 1
    assert result.hypotheses == ()
    assert result.missing_information == ()


def test_analyze_does_not_invent_missing_relationships():
    client = FakeGitHubClient(
        {
            "tickets/31426/ticket.md": """---
ticket_id: "31426"
---

# Ticket 31426

- El objeto funcional mencionado es ZMM_IMX_0004.
""",
        }
    )

    result = analyze(
        client,
        "Analizá el ticket 31426",
        "31426",
    )

    assert result.relationships.relationships == ()
    assert "No explicit relationships" in result.missing_information[0]
    assert result.hypotheses == ()
