"""Local semantic gate for MVP 4.2 using the configured real LLM provider."""

from __future__ import annotations

import argparse
from dataclasses import replace

from src.agent.consultant import Citation, ConsultationResult
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

NEGATIVE_CASES = (
    "partial_as_confirmed",
    "conflict_omitted",
    "unknown_evidence",
    "standard_custom_mixed",
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


def check_certainty_preservation(result: ConsultationResult) -> tuple[bool, str]:
    """Reject explicit confirmation of evidence whose certainty is below confirmed."""
    by_id = {item.evidence_id: item for item in result.traceability.evidence}
    confirmation_markers = (
        "confirmado",
        "confirmada",
        "se confirma",
        "está confirmado",
        "esta confirmado",
        "queda confirmado",
    )
    for evidence_id, item in by_id.items():
        if item.certainty == "confirmed" or evidence_id not in result.answer:
            continue
        for line in result.answer.lower().splitlines():
            if evidence_id.lower() in line and any(
                marker in line for marker in confirmation_markers
            ):
                return (
                    False,
                    f"{evidence_id} tiene certainty={item.certainty} "
                    "pero fue presentado como confirmado.",
                )
    return True, "No se detectó promoción explícita de certainty."


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

        internal_ids = {
            item.evidence_id
            for item in result.traceability.evidence
            if item.source_layer == "internal"
        }
        for line in result.answer.lower().splitlines():
            if "standard" not in line and "estándar" not in line:
                continue
            if any(evidence_id.lower() in line for evidence_id in internal_ids):
                return (
                    False,
                    "Una evidencia interna/custom fue presentada en la misma "
                    "afirmación como SAP Standard.",
                )
            if "zmm_" in line or "snc k1" in line:
                return (
                    False,
                    "Un objeto/proceso custom fue presentado como SAP Standard.",
                )
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


def semantic_checks(result: ConsultationResult) -> tuple[tuple[str, tuple[bool, str]], ...]:
    return (
        ("01 estructura", check_structure(result.answer)),
        ("02 citas EVD", check_citations(result)),
        ("03 incertidumbre/conflicto", check_uncertainty(result)),
        ("04 preservación certainty", check_certainty_preservation(result)),
        ("05 Standard/Custom", check_standard_custom(result)),
        ("06 información faltante", check_missing_information(result)),
        ("07 contexto ticket", check_ticket(result)),
    )


def _first_evidence(result: ConsultationResult, certainty: str | None = None):
    for item in result.traceability.evidence:
        if certainty is None or item.certainty == certainty:
            return item
    return result.traceability.evidence[0]


def _negative_answer(result: ConsultationResult, body: str) -> str:
    evidence_id = _first_evidence(result).evidence_id
    ticket_ref = result.ticket_context[0].reference_id if result.ticket_context else "TKT-NONE"
    return (
        "## Resumen\n\n"
        f"{body} [{evidence_id}]\n\n"
        "## Qué está confirmado\n\n"
        f"Información documentada [{evidence_id}]\n\n"
        "## Qué corresponde a nuestra implementación\n\n"
        "La implementación interna corresponde al contexto del ticket.\n\n"
        "## Qué no está confirmado\n\n"
        "La evidencia adicional requiere validación.\n\n"
        "## Evidencias\n\n"
        f"- [{evidence_id}]\n\n"
        "## Ticket\n\n"
        f"Referencia: {ticket_ref}\n\n"
        "## Próximos pasos\n\n"
        "Validar contra la fuente original."
    )


def build_negative_case(result: ConsultationResult, case: str) -> ConsultationResult:
    evidence = _first_evidence(result)
    partial = _first_evidence(result, "partial")

    if case == "partial_as_confirmed":
        answer = _negative_answer(
            result,
            f"[{partial.evidence_id}] está confirmado como hecho funcional.",
        )
        return replace(result, answer=answer)

    if case == "conflict_omitted":
        answer = _negative_answer(
            result,
            "El escenario del ticket está correctamente identificado y no presenta discrepancias.",
        )
        return replace(result, answer=answer)

    if case == "unknown_evidence":
        fake_id = "EVD-FAKE000000"
        citation = Citation(
            citation_id=fake_id,
            evidence_id=fake_id,
            path="synthetic/unknown",
            source_id=None,
            certainty="confirmed",
        )
        answer = _negative_answer(
            result,
            f"Se incorpora una evidencia adicional [{fake_id}] no presente en la trazabilidad.",
        )
        return replace(
            result,
            answer=answer,
            citations=tuple(result.citations) + (citation,),
        )

    if case == "standard_custom_mixed":
        answer = _negative_answer(
            result,
            f"SAP Standard confirma que ZMM_IMX_0004 genera SNC K1 [{evidence.evidence_id}].",
        )
        return replace(result, answer=answer)

    raise ValueError(f"Unknown negative case: {case}")


def run_negative_cases(result: ConsultationResult) -> bool:
    print("Negative semantic cases:")
    all_passed = True
    expected_rejections = {
        "partial_as_confirmed": "04 preservación certainty",
        "conflict_omitted": "03 incertidumbre/conflicto",
        "unknown_evidence": "02 citas EVD",
        "standard_custom_mixed": "05 Standard/Custom",
    }
    for case in NEGATIVE_CASES:
        mutated = build_negative_case(result, case)
        checks = dict(semantic_checks(mutated))
        expected = expected_rejections[case]
        passed, detail = checks[expected]
        rejected = not passed
        print(
            f"{'PASS' if rejected else 'FAIL'} | {case} | "
            f"rechazo esperado por {expected} | {detail}"
        )
        all_passed = all_passed and rejected
    return all_passed


def run_once(github: GitHubClient, llm: OpenAIResponsesClient) -> tuple[ConsultationResult, bool]:
    response = run_agent(
        github,
        CANONICAL_REQUEST,
        ref="feature/agent-mvp-search",
        llm=llm,
    )
    result = response.result
    if not isinstance(result, ConsultationResult):
        raise TypeError("El router no produjo ConsultationResult.")
    checks = semantic_checks(result)
    passed = all(item[0] for item in checks)
    print(f"Reasoning status: {result.reasoning.conclusion_status}")
    print(f"Trace: {result.traceability.trace_id}")
    for name, (ok, detail) in checks:
        print(f"{'PASS' if ok else 'FAIL'} | {name} | {detail}")
    return result, passed


def main() -> int:
    parser = argparse.ArgumentParser(description="MVP 4.2 semantic gate")
    parser.add_argument(
        "--runs",
        type=int,
        default=1,
        help="Cantidad de ejecuciones reales del caso canónico.",
    )
    args = parser.parse_args()
    if args.runs < 1:
        parser.error("--runs debe ser >= 1")

    github = GitHubClient("araortiz99", "agenteSAP", token=None)
    llm = OpenAIResponsesClient.from_env()

    print("MVP 4.2 — Semantic Gate")
    print(f"Model: {llm.model}")
    print(f"Canonical runs: {args.runs}")
    print()

    passed_runs = 0
    last_result = None
    for index in range(1, args.runs + 1):
        print(f"=== Canonical run {index}/{args.runs} ===")
        result, passed = run_once(github, llm)
        last_result = result
        passed_runs += int(passed)
        print()

    print(f"Canonical stability: {passed_runs}/{args.runs} runs PASS")
    if last_result is None:
        return 1

    negative_passed = run_negative_cases(last_result)
    print()
    print(
        "Negative cases: "
        f"{'PASS' if negative_passed else 'FAIL'} "
        "(cada caso debe ser rechazado por el Gate)"
    )

    return 0 if passed_runs == args.runs and negative_passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
