import pytest

from src.tools.get_ticket import TicketNotFoundError, get_ticket


class FakeGitHubClient:
    def __init__(self, files):
        self.files = files

    def get_tree(self, ref="main"):
        return [{"path": path, "type": "blob"} for path in self.files]

    def get_file(self, path, ref="main"):
        return self.files[path]


def test_get_ticket_returns_all_ticket_documents():
    client = FakeGitHubClient(
        {
            "tickets/31426/ticket.md": "# Ticket 31426",
            "tickets/31426/analysis.md": "# Analysis 31426",
            "tickets/31426/debug.md": "# Debug 31426",
            "tickets/33007/ticket.md": "# Ticket 33007",
        }
    )

    result = get_ticket(client, "31426")

    assert result.ticket_id == "31426"
    assert [doc.path for doc in result.documents] == [
        "tickets/31426/analysis.md",
        "tickets/31426/debug.md",
        "tickets/31426/ticket.md",
    ]


def test_get_ticket_ignores_non_markdown_files():
    client = FakeGitHubClient(
        {
            "tickets/31426/ticket.md": "# Ticket 31426",
            "tickets/31426/evidence.png": "binary-placeholder",
        }
    )

    result = get_ticket(client, "31426")

    assert len(result.documents) == 1
    assert result.documents[0].path == "tickets/31426/ticket.md"


def test_get_ticket_raises_when_ticket_does_not_exist():
    client = FakeGitHubClient(
        {
            "tickets/31426/ticket.md": "# Ticket 31426",
        }
    )

    with pytest.raises(TicketNotFoundError):
        get_ticket(client, "99999")


def test_get_ticket_rejects_empty_ticket_id():
    client = FakeGitHubClient({})

    with pytest.raises(ValueError):
        get_ticket(client, "   ")
