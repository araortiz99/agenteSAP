"""Evidence-based functional analysis capability."""

from __future__ import annotations

from dataclasses import dataclass

from src.github.client import GitHubClient
from src.tools.get_related_knowledge import RelatedKnowledge, get_related_knowledge
from src.tools.get_ticket import TicketContext, get_ticket


@dataclass(frozen=True)
class AnalysisResult:
    ticket_id: str
    request: str
    context: TicketContext
    relationships: RelatedKnowledge
    facts: tuple[str, ...]
    hypotheses: tuple[str, ...]
    missing_information: tuple[str, ...]
    conclusion: str


def _extract_facts(context: TicketContext) -> tuple[str, ...]:
    """Extract explicit bullet facts from retrieved ticket documents.

    This MVP only treats Markdown bullets as facts. It deliberately avoids
    generating semantic conclusions from arbitrary prose.
    """
    facts: list[str] = []

    for document in context.documents:
        for line in document.content.splitlines():
            stripped = line.strip()
            if stripped.startswith("- "):
                facts.append(stripped[2:].strip())

    return tuple(dict.fromkeys(facts))


def analyze(
    client: GitHubClient,
    request: str,
    ticket_id: str,
    *,
    entity_type: str = "TICKET",
    ref: str = "main",
) -> AnalysisResult:
    """Build an evidence-based analysis context for a ticket.

    The MVP retrieves evidence and documented relationships. It does not infer
    a root cause or solution from incomplete evidence.
    """

    if not request.strip():
        raise ValueError("request must not be empty")

    context = get_ticket(client, ticket_id, ref=ref)
    relationships = get_related_knowledge(
        client,
        entity_type,
        ticket_id,
        ref=ref,
    )
    facts = _extract_facts(context)

    missing: list[str] = []
    if not facts:
        missing.append("No explicit bullet facts were found in the ticket documents.")

    if not relationships.relationships:
        missing.append("No explicit relationships were documented for the ticket.")

    hypotheses: tuple[str, ...] = ()

    if missing:
        conclusion = (
            "The available repository evidence is insufficient for a confirmed "
            "functional conclusion. Additional evidence or documentation is required."
        )
    else:
        conclusion = (
            "The ticket context and documented relationships were retrieved. "
            "A functional conclusion requires review of the retrieved evidence "
            "and must not be inferred automatically by this MVP."
        )

    return AnalysisResult(
        ticket_id=str(ticket_id).strip(),
        request=request.strip(),
        context=context,
        relationships=relationships,
        facts=facts,
        hypotheses=hypotheses,
        missing_information=tuple(missing),
        conclusion=conclusion,
    )
