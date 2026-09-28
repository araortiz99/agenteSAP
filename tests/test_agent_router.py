from pathlib import Path

import pytest

from src.agent.router import IntentRoutingError, run_agent, route_intent
from src.tools.analyze import AnalysisResult
from src.tools.get_ticket import TicketContext
from src.tools.get_related_knowledge import RelatedKnowledge
from src.tools.search_knowledge import SearchResult
from src.tools.search_sap_standard import SAPStandardResult
from src.tools.search_unified import UnifiedSearchResult


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


class SAPStandardFakeClient:
    def __init__(self):
        self.files = {
            "knowledge/sap-standard/mm/material-master.md": (
                "# Material Master\\nSAP S/4HANA material master and product master."
            ),
            "knowledge/custom/local.md": "# Local\\nMaterial master custom process.",
        }

    def get_tree(self, ref="main"):
        return [{"path": path, "type": "blob"} for path in self.files]

    def get_file(self, path, ref="main"):
        return self.files[path]


def test_route_explicit_consult_to_llm_layer():
    plan = route_intent("Consultá sobre material master")
    assert plan.intent == "consult"
    assert "consult_llm" in plan.capabilities


class FakeLLM:
    model = "fake"

    def generate(self, *, system_prompt, user_prompt):
        import re

        evidence_match = re.search(r"(EVD-[A-Z0-9]+)", user_prompt)
        ticket_match = re.search(r"(TKT-[A-Z0-9]+)", user_prompt)
        evidence_id = evidence_match.group(1) if evidence_match else "EVD-TEST"
        ticket_id = ticket_match.group(1) if ticket_match else "TKT-TEST"

        return (
            "## Resumen\n"
            "Respuesta de prueba basada en la evidencia recuperada.\n\n"
            "## Qué está confirmado\n"
            f"Existe evidencia recuperada [{evidence_id}].\n\n"
            "## Qué corresponde a nuestra implementación\n"
            f"El contexto interno recuperado está referenciado [{evidence_id}].\n\n"
            "## Qué no está confirmado\n"
            "La prueba no establece hechos adicionales fuera de la evidencia recuperada.\n\n"
            "## Evidencias\n"
            f"[{evidence_id}]\n\n"
            "## Ticket\n"
            f"Contexto del ticket [{ticket_id}].\n\n"
            "## Próximos pasos\n"
            "Validar la información pendiente contra la evidencia disponible."
        )

def test_route_analyze_ticket_31426_builds_capability_plan():
    plan = route_intent("Analizá el ticket 31426")

    assert plan.intent == "analyze_ticket"
    assert plan.ticket_id == "31426"
    assert plan.capabilities == (
        "get_ticket",
        "get_related_knowledge",
        "analyze",
    )




def test_route_rich_ticket_analysis_to_consultant():
    plan = route_intent(
        "Analizá el ticket 31426 y separá hechos confirmados, evidencias, "
        "qué corresponde a nuestra implementación y próximos pasos."
    )
    assert plan.intent == "consult"
    assert plan.ticket_id == "31426"
    assert "consult_llm" in plan.capabilities

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


def test_realistic_multi_step_request_routes_to_consultant():
    client = AgentFakeGitHubClient()
    request = (
        "Revisá el ticket 31426, buscá qué objetos SAP están relacionados "
        "y preparame un análisis indicando qué está confirmado y qué información falta."
    )

    response = run_agent(client, request, llm=FakeLLM())

    assert response.plan.intent == "consult"
    assert response.plan.ticket_id == "31426"
    assert response.plan.capabilities == (
        "search_unified",
        "assess_evidence",
        "reason_from_evidence",
        "build_traceability",
        "consult_llm",
    )

    from src.agent.consultant import ConsultationResult

    result = response.result
    assert isinstance(result, ConsultationResult)
    assert result.ticket_context
    assert result.ticket_context[0].ticket_id == "31426"
    assert result.answer.startswith("## Resumen")
    assert result.traceability.evidence
    assert result.citations


def test_route_sap_standard_search():
    plan = route_intent("Buscá SAP Standard sobre material master")
    assert plan.intent == "search_sap_standard"
    assert plan.capabilities == ("search_sap_standard",)


def test_run_agent_sap_standard_search():
    client = SAPStandardFakeClient()
    response = run_agent(client, "Buscá SAP Standard sobre material master")
    assert response.plan.intent == "search_sap_standard"
    assert isinstance(response.result, list)
    assert isinstance(response.result[0], SAPStandardResult)
    assert response.result[0].path.endswith("material-master.md")


def test_route_unified_sap_and_internal_search():
    plan = route_intent("Compará SAP Standard y nuestra implementación sobre material master")
    assert plan.intent == "search_unified"
    assert plan.capabilities == ("search_unified",)


def test_run_agent_unified_search():
    client = AgentFakeGitHubClient()
    response = run_agent(
        client,
        "Compará SAP Standard y nuestra implementación sobre ZMM_IMX_0004",
    )
    assert response.plan.intent == "search_unified"
    assert isinstance(response.result, UnifiedSearchResult)


def test_route_evidence_reasoning():
    plan = route_intent("Evaluá la evidencia y decime qué está confirmado y qué falta sobre material master")
    assert plan.intent == "evidence_reasoning"
    assert plan.capabilities == (
        "search_unified",
        "assess_evidence",
        "reason_from_evidence",
    )


def test_run_agent_evidence_reasoning():
    client = AgentFakeGitHubClient()
    response = run_agent(
        client,
        "Evaluá la evidencia y decime qué está confirmado y qué falta sobre material master",
    )
    assert response.plan.intent == "evidence_reasoning"
    assert response.result.conclusion_status in {
        "requires_analysis",
        "supported",
        "partial",
        "insufficient",
        "conflict",
    }


def test_route_evidence_traceability():
    plan = route_intent("Dame la trazabilidad de evidencia sobre material master")
    assert plan.intent == "evidence_traceability"
    assert plan.capabilities == (
        "search_unified",
        "assess_evidence",
        "reason_from_evidence",
        "build_traceability",
    )


def test_run_agent_evidence_traceability():
    client = AgentFakeGitHubClient()
    response = run_agent(
        client,
        "Dame la trazabilidad de evidencia sobre material master",
    )
    assert response.plan.intent == "evidence_traceability"
    assert response.result.trace_id.startswith("TRACE-")


def test_route_ticket_consult_extracts_ticket_id():
    plan = route_intent("Consultá el ticket 31426 y explicame qué está confirmado")
    assert plan.intent == "consult"
    assert plan.ticket_id == "31426"

def test_route_specialized_evidence_request_before_generic_consult():
    plan = route_intent(
        "Evaluá la evidencia y explicame qué está confirmado y qué falta sobre material master"
    )
    assert plan.intent == "evidence_reasoning"


def test_route_specialized_comparison_request_before_generic_consult():
    plan = route_intent(
        "Explicame la diferencia entre SAP Standard y nuestra implementación"
    )
    assert plan.intent == "search_unified"


def test_route_specialized_standard_request_before_generic_consult():
    plan = route_intent(
        "Explicame SAP Standard sobre material master"
    )
    assert plan.intent == "search_sap_standard"


def test_route_generic_explanation_still_uses_consultant():
    plan = route_intent("Explicame el proceso de inventario")
    assert plan.intent == "consult"
    assert "consult_llm" in plan.capabilities

def test_route_document_generation_before_analysis_keyword():
    plan = route_intent("Generá un análisis del ticket 31426")
    assert plan.intent == "generate_document"
    assert plan.ticket_id == "31426"
    assert "generate_document" in plan.capabilities


def test_route_runtime_configuration_question_to_consultant():
    plan = route_intent("¿Qué tiene configurado actualmente ZMM_IMX_0004 en QAS?")
    assert plan.intent == "consult"
    assert "search_unified" in plan.capabilities
    assert "consult_llm" in plan.capabilities


def test_route_runtime_configuration_without_explicit_question_to_consultant():
    plan = route_intent("Estado actual de ZMM_IMX_0004 en PRD")
    assert plan.intent == "consult"

def test_route_ticket_factual_question_to_consultant():
    plan = route_intent("¿El ticket 31426 corresponde a K1 o K4?")
    assert plan.intent == "consult"
    assert plan.ticket_id == "31426"
    assert "consult_llm" in plan.capabilities


def test_route_ticket_root_cause_question_to_consultant():
    plan = route_intent("¿Cuál es la causa raíz técnica exacta del ticket 31426?")
    assert plan.intent == "consult"
    assert plan.ticket_id == "31426"


def test_route_explicit_ticket_retrieval_stays_deterministic():
    plan = route_intent("Mostrame el ticket 31426")
    assert plan.intent == "get_ticket"


def test_run_agent_unified_search_uses_mcp_when_enabled(monkeypatch):
    class FakeGateway:
        def search_resources(self, query):
            from src.tools.search_unified import UnifiedResult
            return (
                UnifiedResult(
                    path="mcp://sap_devs/search_resources",
                    score=0.9,
                    matched_terms=("ABAP",),
                    content="MCP result",
                    source_layer="mcp",
                    match_type="mcp",
                    source_id="sap_devs:search_resources",
                    knowledge_type="developer_context",
                    knowledge_scope="external",
                    certainty="external_source",
                ),
            )

    monkeypatch.setattr(
        "src.agent.router.McpEvidenceGateway.from_env",
        lambda: FakeGateway(),
    )
    client = AgentFakeGitHubClient()
    response = run_agent(
        client,
        "Compará SAP Standard y nuestra implementación sobre ABAP",
    )

    assert response.result.mcp
    assert response.result.mcp[0].source_layer == "mcp"


def test_run_agent_evidence_reasoning_preserves_mcp_layer(monkeypatch):
    class FakeGateway:
        def search_resources(self, query):
            from src.tools.search_unified import UnifiedResult
            return (
                UnifiedResult(
                    path="mcp://sap_devs/search_resources",
                    score=0.9,
                    matched_terms=("ABAP",),
                    content="MCP result",
                    source_layer="mcp",
                    match_type="mcp",
                    source_id="sap_devs:search_resources",
                    knowledge_type="developer_context",
                    knowledge_scope="external",
                    certainty="external_source",
                ),
            )

    monkeypatch.setattr(
        "src.agent.router.McpEvidenceGateway.from_env",
        lambda: FakeGateway(),
    )
    client = AgentFakeGitHubClient()
    response = run_agent(
        client,
        "Evaluá la evidencia sobre ABAP",
    )

    assert any(item.source_layer == "mcp" for item in response.result.evidence.items)


def test_run_agent_consult_passes_mcp_gateway(monkeypatch):
    class FakeGateway:
        def search_resources(self, query):
            from src.tools.search_unified import UnifiedResult
            return (
                UnifiedResult(
                    path="mcp://sap_devs/search_resources",
                    score=0.9,
                    matched_terms=("ABAP",),
                    content="MCP consultant context",
                    source_layer="mcp",
                    match_type="mcp",
                    source_id="sap_devs:search_resources",
                    knowledge_type="developer_context",
                    knowledge_scope="external",
                    certainty="external_source",
                ),
            )

    class ConsultLLM(FakeLLM):
        def generate(self, *, system_prompt, user_prompt):
            import re
            evidence_id = re.search(r"(EVD-[A-Z0-9]+)", user_prompt).group(1)
            return (
                "## Resumen\\nRespuesta.\\n\\n"
                "## Qué está confirmado\\nContexto. [" + evidence_id + "]\\n\\n"
                "## Qué corresponde a nuestra implementación\\nNo consta.\\n\\n"
                "## Qué no está confirmado\\nPendiente.\\n\\n"
                "## Evidencias\\n[" + evidence_id + "]\\n\\n"
                "## Ticket\\nSin ticket.\\n\\n"
                "## Próximos pasos\\nValidar."
            )

    monkeypatch.setattr("src.agent.router.McpEvidenceGateway.from_env", lambda: FakeGateway())
    response = run_agent(
        AgentFakeGitHubClient(),
        "Explicame el proceso de inventario",
        llm=ConsultLLM(),
    )
    assert response.plan.intent == "consult"
    assert response.result.retrieval.mcp


def test_route_runtime_configuration_question_to_consultant():
    plan = route_intent("¿Qué tiene configurado actualmente ZMM_IMX_0004 en QAS?")
    assert plan.intent == "consult"
    assert "search_unified" in plan.capabilities
    assert "consult_llm" in plan.capabilities


def test_route_runtime_configuration_without_explicit_question_to_consultant():
    plan = route_intent("Estado actual de ZMM_IMX_0004 en PRD")
    assert plan.intent == "consult"


def test_route_runtime_question_is_not_captured_by_standard_search():
    plan = route_intent("¿Qué tiene configurado actualmente ZMM_IMX_0004 según SAP Standard?")
    assert plan.intent == "consult"
