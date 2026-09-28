"""Deterministic orchestration layer for the SAP agent MVP."""

from __future__ import annotations

import re
from dataclasses import dataclass

from src.github.client import GitHubClient
from src.agent.consultant import ConsultationResult, consult
from src.llm.client import LLMClient, OpenAIResponsesClient
from src.tools.analyze import AnalysisResult, analyze
from src.tools.generate_document import GeneratedDocument, generate_document
from src.tools.get_ticket import TicketContext, get_ticket
from src.tools.get_related_knowledge import RelatedKnowledge, get_related_knowledge
from src.tools.search_knowledge import SearchResult, search_knowledge
from src.tools.search_sap_standard import SAPStandardResult, search_sap_standard
from src.tools.search_unified import UnifiedSearchResult, search_unified
from src.tools.evidence import EvidenceAssessment, assess_evidence
from src.tools.reason import ReasoningResult, reason_from_evidence
from src.tools.evidence_trace import TraceabilityReport, build_traceability


class IntentRoutingError(ValueError):
    """Raised when a user request cannot be mapped safely to an MVP intent."""


@dataclass(frozen=True)
class AgentPlan:
    intent: str
    ticket_id: str | None
    capabilities: tuple[str, ...]


@dataclass(frozen=True)
class AgentResponse:
    request: str
    plan: AgentPlan
    result: object


_TICKET_PATTERNS = (
    re.compile(r"\bticket\s*#?\s*(\d+)\b", re.IGNORECASE),
    re.compile(r"\bincidente\s*#?\s*(\d+)\b", re.IGNORECASE),
    re.compile(r"\b(?:analiz[aá]|analizar|analisis|análisis)\s+(?:el\s+)?(?:ticket|incidente)\s*#?\s*(\d+)\b", re.IGNORECASE),
)


def _extract_ticket_id(request: str) -> str | None:
    for pattern in _TICKET_PATTERNS:
        match = pattern.search(request)
        if match:
            return match.group(1)
    return None


def route_intent(request: str) -> AgentPlan:
    """Classify a user request and produce a deterministic capability plan."""
    text = request.strip()
    if not text:
        raise IntentRoutingError("request must not be empty")

    lowered = text.lower()
    ticket_id = _extract_ticket_id(text)

    if any(phrase in lowered for phrase in ("consultá", "consulta", "consultar", "explicame", "explicá", "explica")):
        return AgentPlan(
            intent="consult",
            ticket_id=ticket_id,
            capabilities=(
                "search_unified",
                "assess_evidence",
                "reason_from_evidence",
                "build_traceability",
                "consult_llm",
            ),
        )

    if any(term in lowered for term in ("analizá", "analiza", "analizar", "análisis", "analisis")):
        if not ticket_id:
            raise IntentRoutingError(
                "No se pudo identificar ticket_id para la solicitud de análisis."
            )
        return AgentPlan(
            intent="analyze_ticket",
            ticket_id=ticket_id,
            capabilities=(
                "get_ticket",
                "get_related_knowledge",
                "analyze",
            ),
        )

    if any(term in lowered for term in ("generá", "genera", "generar", "creá", "crear", "documentá", "documentar")):
        document_type = None
        if "requerimiento" in lowered:
            document_type = "requirement"
        elif "especificación funcional" in lowered or "especificacion funcional" in lowered:
            document_type = "functional-specification"
        elif "prueba funcional" in lowered or "pruebas funcionales" in lowered:
            document_type = "functional-test"
        elif "investigación" in lowered or "investigacion" in lowered:
            document_type = "investigation"
        elif "análisis" in lowered or "analisis" in lowered:
            document_type = "analysis"

        if not document_type:
            raise IntentRoutingError(
                "No se pudo identificar el tipo documental solicitado."
            )

        return AgentPlan(
            intent="generate_document",
            ticket_id=ticket_id,
            capabilities=("generate_document",),
        )

    if any(
        phrase in lowered
        for phrase in (
            "trazabilidad de evidencia",
            "trazabilidad de la evidencia",
            "evidence trace",
            "evidence traceability",
        )
    ):
        return AgentPlan(
            intent="evidence_traceability",
            ticket_id=ticket_id,
            capabilities=(
                "search_unified",
                "assess_evidence",
                "reason_from_evidence",
                "build_traceability",
            ),
        )

    if any(
        phrase in lowered
        for phrase in (
            "evaluá la evidencia",
            "evalua la evidencia",
            "evaluar evidencia",
            "analizá la evidencia",
            "analiza la evidencia",
            "qué está confirmado",
            "que esta confirmado",
            "qué está confirmado y qué falta",
            "que esta confirmado y que falta",
        )
    ):
        return AgentPlan(
            intent="evidence_reasoning",
            ticket_id=ticket_id,
            capabilities=(
                "search_unified",
                "assess_evidence",
                "reason_from_evidence",
            ),
        )

    if any(
        phrase in lowered
        for phrase in (
            "sap standard y",
            "sap estándar y",
            "standard y custom",
            "standard y nuestra",
            "estándar y nuestra",
            "compará sap",
            "compara sap",
        )
    ):
        return AgentPlan(
            intent="search_unified",
            ticket_id=ticket_id,
            capabilities=("search_unified",),
        )

    if any(term in lowered for term in ("sap standard", "sap estándar", "sap standard knowledge", "help portal")):
        return AgentPlan(
            intent="search_sap_standard",
            ticket_id=ticket_id,
            capabilities=("search_sap_standard",),
        )

    if "relacion" in lowered or "relacionado" in lowered:
        if not ticket_id:
            raise IntentRoutingError(
                "No se pudo identificar la entidad para consultar relaciones."
            )
        return AgentPlan(
            intent="get_related_knowledge",
            ticket_id=ticket_id,
            capabilities=("get_related_knowledge",),
        )

    if "ticket" in lowered and ticket_id:
        return AgentPlan(
            intent="get_ticket",
            ticket_id=ticket_id,
            capabilities=("get_ticket",),
        )

    return AgentPlan(
        intent="search_knowledge",
        ticket_id=ticket_id,
        capabilities=("search_knowledge",),
    )


def run_agent(
    client: GitHubClient,
    request: str,
    *,
    ref: str = "main",
    date: str = "",
    author: str = "",
    llm: LLMClient | None = None,
    ticket_id: str | None = None,
    max_results: int = 8,
) -> AgentResponse:
    """Route and execute the minimum safe capability chain for a request."""
    if max_results < 1:
        raise ValueError("max_results must be greater than zero")
    plan = route_intent(request)
    if ticket_id:
        plan = AgentPlan(
            intent=plan.intent,
            ticket_id=ticket_id.strip(),
            capabilities=plan.capabilities,
        )

    if plan.intent == "consult":
        llm_client = llm or OpenAIResponsesClient.from_env()
        result = consult(client, request, llm_client, ref=ref, ticket_id=plan.ticket_id, max_results=max_results)
    elif plan.intent == "analyze_ticket":
        result = analyze(client, request, plan.ticket_id or "", ref=ref)
    elif plan.intent == "get_ticket":
        result = get_ticket(client, plan.ticket_id or "", ref=ref)
    elif plan.intent == "get_related_knowledge":
        result = get_related_knowledge(client, "TICKET", plan.ticket_id or "", ref=ref)
    elif plan.intent == "search_sap_standard":
        result = search_sap_standard(client, request, ref=ref)
    elif plan.intent == "search_unified":
        result = search_unified(client, request, ref=ref)
    elif plan.intent == "evidence_reasoning":
        retrieval = search_unified(client, request, ref=ref)
        evidence = assess_evidence(retrieval)
        result = reason_from_evidence(evidence)
    elif plan.intent == "evidence_traceability":
        retrieval = search_unified(client, request, ref=ref)
        evidence = assess_evidence(retrieval)
        reasoning = reason_from_evidence(evidence)
        result = build_traceability(reasoning)
    elif plan.intent == "search_knowledge":
        result = search_knowledge(client, request, ref=ref)
    elif plan.intent == "generate_document":
        document_type = _document_type_from_request(request)
        result = generate_document(
            client,
            document_type,
            request,
            plan.ticket_id,
            ref=ref,
            date=date,
            author=author,
        )
    else:
        raise IntentRoutingError(f"Unsupported intent: {plan.intent}")

    return AgentResponse(request=request.strip(), plan=plan, result=result)


def _document_type_from_request(request: str) -> str:
    lowered = request.lower()
    if "requerimiento" in lowered:
        return "requirement"
    if "especificación funcional" in lowered or "especificacion funcional" in lowered:
        return "functional-specification"
    if "prueba funcional" in lowered or "pruebas funcionales" in lowered:
        return "functional-test"
    if "investigación" in lowered or "investigacion" in lowered:
        return "investigation"
    if "análisis" in lowered or "analisis" in lowered:
        return "analysis"
    raise IntentRoutingError("No se pudo identificar el tipo documental solicitado.")
