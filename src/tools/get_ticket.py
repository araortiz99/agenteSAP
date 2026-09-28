"""Ticket retrieval capability."""

from __future__ import annotations

from dataclasses import dataclass

from src.github.client import GitHubClient


@dataclass(frozen=True)
class TicketDocument:
    path: str
    content: str


@dataclass(frozen=True)
class TicketContext:
    ticket_id: str
    documents: tuple[TicketDocument, ...]


class TicketNotFoundError(LookupError):
    """Raised when the requested ticket does not exist in the repository."""


def _ticket_prefix(ticket_id: str) -> str:
    return f"tickets/{ticket_id}/"


def get_ticket(
    client: GitHubClient,
    ticket_id: str,
    ref: str = "main",
) -> TicketContext:
    """Retrieve all Markdown documents belonging to an existing ticket.

    The repository tree is the source of truth for ticket existence. No ticket
    directory or document is inferred when it is absent.
    """

    normalized_id = str(ticket_id).strip()

    if not normalized_id:
        raise ValueError("ticket_id must not be empty")

    prefix = _ticket_prefix(normalized_id)
    tree = client.get_tree(ref=ref)

    paths = sorted(
        item["path"]
        for item in tree
        if item.get("type") == "blob"
        and item.get("path", "").startswith(prefix)
        and item.get("path", "").endswith(".md")
    )

    if not paths:
        raise TicketNotFoundError(
            f"Ticket {normalized_id} was not found at {prefix}"
        )

    documents = tuple(
        TicketDocument(path=path, content=client.get_file(path, ref=ref))
        for path in paths
    )

    return TicketContext(
        ticket_id=normalized_id,
        documents=documents,
    )
