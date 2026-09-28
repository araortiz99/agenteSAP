"""Local semantic gate for MVP 4.2 using the configured real LLM provider."""

from __future__ import annotations

from src.agent.consultant import ConsultationResult
from src.agent.router import run_agent
from src.github.client import GitHubClient
from src.llm.client import OpenAIResponsesClient


CANONICAL_REQUEST = (
    "Consultá el ticket 31426 y explicame qué está confirmado, "
    "qué corresponde a nuestra implementación y qué información falta."
)

REQUIRED_SECTIONS = (
    "## Resumen",
    "## Qué está confirmado",
    "## Qué corresponde a nuestra implementación",
    "## Qué no está confirmado",
    "## Evidencias",
    "## Ticket",
    "## Próximos pasos",
)


def check_structure(answer: str) -> tuple[bool, str]:
    positions = [answer.find(section) for section in REQUIRED_SECTIONS]
    if any(position < 0 for position in positions):
        return False, "Faltan secciones obligatorias."
    if positions != sorted(positions):
        return False, "Las secciones están fuera de orden."
    return True, "Estructura 4.2 válida."


def check_citations(result: ConsultationResult) -> tuple[bool, str]:
    evidence_ids = {item.evidence_id for item in result.traceability.evidence}
    cited_ids = {citation.evidence_id for citation in result.citations}
    if not cited_ids:
        return False, "No se encontraron citas EVD-*."
    if not cited_ids.issubset(evidence_ids):
        return False, "Existe una cita EVD-* fuera de la trazabilidad."
    return True, f"{len(cited_ids)} cita(s) EVD-* verificadas."


def check_ticket(result: ConsultationResult) -> tuple[bool, str]:
    if not result.ticket_context:
        return False, "No se recuperó contexto del ticket."
    references = {item.reference_id for item in result.ticket_context}
    if not any(reference in result.answer for reference in references):
        return False, "La respuesta no referencia TKT-*."
    return True, "Contexto TKT-* recuperado y referenciado."


def check_uncertainty(result: ConsultationResult) -> tuple[bool, str]:
    answer = result.answer.lower()
    if result.reasoning.conclusion_status == "conflict":
        required = (
            "k1" in answer
            and "k4" in answer
            and any(
                phrase in answer
                for phrase in (
                    "no confirmado",
                    "pendiente",
                    "requiere análisis",
                    "requiere validación",
                    "discrepancia",
                    "contradic",
                )
            )
        )
        if not required:
            return False, "El conflicto K1/K4 no quedó tratado como pendiente."
    return True, "La respuesta conserva el estado de incertidumbre."


def check_standard_custom(result: ConsultationResult) -> tuple[bool, str]:
    answer = result.answer.lower()
    has_standard = any(
        item.source_layer == "sap_standard"
        for item in result.traceability.evidence
    )
    has_internal = any(
        item.source_layer == "internal"
        for item in result.traceability.evidence
    )
    if has_standard and has_internal:
        if not any(x in answer for x in ("standard", "estándar", "sap")):
            return False, "No se distingue SAP Standard."
        if not any(x in answer for x in ("implementación", "intern", "custom", "propia")):
            return False, "No se distingue la implementación interna/custom."
    return True, "Separación Standard/Custom presente o no aplicable."


def check_missing_information(result: ConsultationResult) -> tuple[bool, str]:
    answer = result.answer.lower()
    if not result.traceability.gaps:
        return True, "No existen gaps determinísticos."
    markers = (
        "no confirmado",
        "información faltante",
        "pendiente",
        "falta",
        "no se dispone",
        "requiere validación",
        "requiere análisis",
    )
    if not any(marker in answer for marker in markers):
        return False, "La respuesta no explicita la información faltante."
    return True, "La información faltante/gaps fue explicitada."


def main() -> int:
    github = GitHubClient(
        "araortiz99",
        "agenteSAP",
        token=None,
    )
    llm = OpenAIResponsesClient.from_env()

    response = run_agent(
        github,
        CANONICAL_REQUEST,
        ref="feature/agent-mvp-search",
        llm=llm,
    )
    result = response.result
    if not isinstance(result, ConsultationResult):
        print("FAIL | El router no produjo ConsultationResult.")
        return 1

    checks = (
        ("01 estructura", check_structure(result.answer)),
        ("02 citas EVD", check_citations(result)),
        ("03 incertidumbre/conflicto", check_uncertainty(result)),
        ("04 Standard/Custom", check_standard_custom(result)),
        ("05 información faltante", check_missing_information(result)),
        ("06 contexto ticket", check_ticket(result)),
    )

    print("MVP 4.2 — Semantic Gate")
    print(f"Model: {result.model}")
    print(f"Reasoning status: {result.reasoning.conclusion_status}")
    print(f"Trace: {result.traceability.trace_id}")
    print()

    failed = False
    for name, (passed, detail) in checks:
        print(f"{'PASS' if passed else 'FAIL'} | {name} | {detail}")
        failed = failed or not passed

    print()
    print("Response:")
    print(result.answer)
    print()
    print("Conflicts:")
    for conflict in result.traceability.conflicts:
        print(
            f"- {conflict.conflict_type} | {conflict.status} | "
            f"{conflict.description}"
        )

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
