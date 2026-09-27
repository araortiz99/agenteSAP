from pathlib import Path

import pytest

from src.agent.router import IntentRoutingError, run_agent, route_intent
from src.tools.analyze import AnalysisResult
from src.tools.get_ticket import TicketContext
from src.tools.get_related_knowledge import RelatedKnowledge
from src.tools.search_knowledge import SearchResult


FIXTURES = Path(__file__).parent / "fixtures"


class AgentFakeGitHubClient:
    def __init__(self):
        self.files = {
            "tickets/31426/ticket.md": (FIXTURES / "ticket-31426.md").read_text(
                encoding="utf-8"
            ),
            "knowledge/relationships/rel-31426-zmm-imx-0004.md": (
                FIXTURES / "rel-31426-zmm-imx-0004.md"
            ).read_text(encoding="utf-8"),
            "knowledge/sap-objects/sap-object-zmm-imx-0004.md": (
                FIXTURES / "sap-object-zmm-imx-0004.md"
            ).read_text(encoding="utf-8"),
            "templates/analysis.md": (FIXTURES / "ticket-31426.md").read_text(
                encoding="utf-8"
            ),
        }

    def get_tree(self, ref="main"):
        return [{"path": path, "type": "blob"} for path in self.files]

    def get_file(self, path, ref="main"):
        return self.files[path]


def test_route_analyze_ticket_31426_builds_capability_plan():
    plan = route_intent("Analizá el ticket 31426")

    assert plan.intent == "analyze_ticket"
    assert plan.ticket_id == "31426"
    assert plan.capabilities == (
        "get_ticket",
        "get_related_knowledge",
        "analyze",
    )


def test_run_agent_executes_analysis_chain_without_manual_capability_calls():
    client = AgentFakeGitHubClient()

    response = run_agent(
        client,
        "Analizá el ticket 31426",
        date="2026-09-27",
        author="integration-test",
    )

    assert response.plan.intent == "analyze_ticket"
    assert response.plan.ticket_id == "31426"
    assert isinstance(response.result, AnalysisResult)
    assert response.result.ticket_id == "31426"
    assert response.result.facts
    assert response.result.relationships.relationships


def test_route_search_when_no_specialized_intent_is_detected():
    plan = route_intent("ZMM_IMX_0004 SNC")

    assert plan.intent == "search_knowledge"
    assert plan.capabilities == ("search_knowledge",)


def test_route_rejects_ambiguous_analysis_without_ticket():
    with pytest.raises(IntentRoutingError):
        route_intent("Analizá este incidente")


def test_run_agent_retrieves_ticket_without_manual_capability_call():
    client = AgentFakeGitHubClient()

    response = run_agent(client, "Mostrame el ticket 31426")

    assert response.plan.intent == "get_ticket"
    assert isinstance(response.result, TicketContext)
    assert response.result.ticket_id == "31426"


def test_run_agent_retrieves_explicit_ticket_relationships():
    client = AgentFakeGitHubClient()

    response = run_agent(client, "Mostrame las relaciones del ticket 31426")

    assert response.plan.intent == "get_related_knowledge"
    assert isinstance(response.result, RelatedKnowledge)
    assert response.result.relationships


def test_route_rejects_empty_request():
    with pytest.raises(IntentRoutingError):
        route_intent("   ")
