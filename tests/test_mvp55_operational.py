from dataclasses import dataclass

import pytest

from src.agent.router import IntentRoutingError, route_intent, run_agent


def test_mvp55_explicit_ticket_overrides_extracted_ticket():
    plan = route_intent("Consultá el ticket 31426")
    assert plan.ticket_id == "31426"


def test_mvp55_run_agent_rejects_invalid_max_results():
    class Client:
        pass

    with pytest.raises(ValueError, match="max_results"):
        run_agent(Client(), "Consultá sobre ZMM_IMX_0004", max_results=0)


def test_mvp55_unknown_analysis_requires_ticket():
    with pytest.raises(IntentRoutingError, match="ticket_id"):
        route_intent("Analizá el problema de SNC")


@dataclass(frozen=True)
class FakeLLM:
    model: str = "mvp55-test"

    def generate(self, *, system_prompt: str, user_prompt: str) -> str:
        return (
            "## Resumen\nRespuesta de prueba.\n\n"
            "## Qué está confirmado\nEvidencia disponible.\n\n"
            "## Qué corresponde a nuestra implementación\nContexto interno.\n\n"
            "## Qué no está confirmado\nPendiente.\n\n"
            "## Evidencias\nSin evidencia en este fixture.\n\n"
            "## Ticket\nSin ticket.\n\n"
            "## Próximos pasos\nValidar."
        )


def test_mvp55_router_keeps_explicit_ticket_in_plan(monkeypatch):
    captured = {}

    def fake_consult(client, request, llm, *, ref, ticket_id, max_results):
        captured["ticket_id"] = ticket_id
        captured["max_results"] = max_results
        return "consulted"

    import src.agent.router as router

    monkeypatch.setattr(router, "consult", fake_consult)
    response = run_agent(
        object(),
        "Consultá el ticket 31426",
        ticket_id="99999",
        llm=FakeLLM(),
        max_results=12,
    )
    assert response.plan.intent == "consult"
    assert response.plan.ticket_id == "99999"
    assert captured == {"ticket_id": "99999", "max_results": 12}
