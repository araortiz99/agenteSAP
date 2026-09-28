"""First end-to-end bounded consultative investigation slice."""

from __future__ import annotations

from dataclasses import asdict
from datetime import date
from typing import Any

from src.github.client import GitHubClient
from src.sap.mcp_gateway import McpEvidenceGateway
from src.tools.evidence import assess_evidence
from src.tools.reason import reason_from_evidence
from src.tools.search_unified import UnifiedResult, UnifiedSearchResult, search_unified

from src.investigation.capabilities import discover_capabilities, match_capabilities
from src.investigation.case_id import build_case_id
from src.investigation.correlation import correlate_evidence
from src.investigation.contracts import (
    Investigation,
    InvestigationEntity,
    InvestigationEvidence,
    InvestigationStep,
)
from src.investigation.entities import extract_entities, missing_required_entities
from src.investigation.planner import create_plan


MAX_STEPS_DEFAULT = 5


def _content(value: object) -> str:
    if isinstance(value, str):
        return value
    return str(value)


def _normalize_knowledge_evidence(result: UnifiedResult) -> InvestigationEvidence:
    evidence_id = "EVD-" + __import__("hashlib").sha256(
        "|".join(
            (
                result.source_layer,
                result.path,
                result.source_id or "",
                result.knowledge_type,
                result.certainty,
            )
        ).encode("utf-8")
    ).hexdigest()[:12].upper()
    provenance = tuple(result.provenance)
    return InvestigationEvidence(
        evidence_id=evidence_id,
        provider=result.source_layer,
        operation=result.match_type,
        landscape="KNOWLEDGE",
        system=None,
        object_type=result.knowledge_type,
        object_id=result.source_id,
        observation_type=result.knowledge_type,
        content=result.content,
        certainty=result.certainty,
        provenance=provenance,
    )


def _normalize_runtime_evidence(evidence: Any) -> InvestigationEvidence:
    raw = "|".join(
        (
            str(evidence.provider),
            str(evidence.operation),
            str(evidence.system or ""),
            str(evidence.landscape or ""),
            str(evidence.object_id or ""),
            str(evidence.observation_type),
        )
    )
    evidence_id = "EVD-" + __import__("hashlib").sha256(raw.encode("utf-8")).hexdigest()[:12].upper()
    provenance = tuple(sorted(evidence.as_metadata().items()))
    return InvestigationEvidence(
        evidence_id=evidence_id,
        provider=evidence.provider,
        operation=evidence.operation,
        landscape=evidence.landscape or "QAS",
        system=evidence.system,
        object_type="SAP_RUNTIME",
        object_id=evidence.object_id,
        observation_type=evidence.observation_type,
        content=_content(evidence.content),
        certainty=evidence.certainty,
        provenance=provenance,
    )


def _query_arguments(capability, entities: tuple[InvestigationEntity, ...]) -> dict[str, object] | None:
    schema = capability.input_schema
    properties = schema.get("properties", {}) if isinstance(schema, dict) else {}
    required = schema.get("required", []) if isinstance(schema, dict) else []
    values = {item.entity_type: item.value for item in entities}
    aliases = {
        "material": ("material", "matnr", "material_number"),
        "plant": ("plant", "center", "centro", "werks"),
        "storage_location": ("storage_location", "storage", "almacen", "lgort"),
        "movement_type": ("movement_type", "movement", "bwart"),
        "material_document": ("material_document", "material_doc", "mblnr"),
    }
    arguments: dict[str, object] = {}
    for entity_type, keys in aliases.items():
        if entity_type not in values:
            continue
        for key in keys:
            if key in properties:
                arguments[key] = values[entity_type]
                break
    if required and any(key not in arguments for key in required):
        return None
    if not properties and required:
        return None
    return arguments


def _provenance(item: InvestigationEvidence) -> dict[str, Any]:
    return {
        "evidence_id": item.evidence_id,
        "provider": item.provider,
        "operation": item.operation,
        "landscape": item.landscape,
        "system": item.system,
        "observation_type": item.observation_type,
        "certainty": item.certainty,
        "provenance": dict(item.provenance),
    }


def _confidence(items: list[InvestigationEvidence], missing: list[str], conflicts: bool) -> tuple[str, str]:
    if conflicts:
        return "LOW", "Evidencia contradictoria: no se permite una conclusión definitiva."
    runtime = [item for item in items if item.landscape == "QAS"]
    independent = {(item.provider, item.operation) for item in items}
    if runtime and len(independent) >= 2 and not missing:
        return "HIGH", "Existe observación runtime QAS y evidencia independiente suficiente."
    if runtime or len(independent) >= 2:
        return "MEDIUM", "Existe evidencia parcial con al menos una fuente independiente."
    return "LOW", "No existe evidencia suficiente para sostener una causa raíz."


def investigate(
    client: GitHubClient,
    question: str,
    *,
    ref: str = "main",
    mcp_gateway: McpEvidenceGateway | None = None,
    max_steps: int = MAX_STEPS_DEFAULT,
    day: date | None = None,
) -> Investigation:
    if not question or not question.strip():
        raise ValueError("question must not be empty")
    if max_steps < 1:
        raise ValueError("max_steps must be greater than zero")

    entities = extract_entities(question)
    plan = create_plan(question, entities)
    investigation = Investigation(
        case_id=build_case_id(question, day=day),
        user_question=question.strip(),
        intent=plan.intent,
        entities=entities,
        required_evidence=plan.required_evidence,
        steps=list(plan.steps),
    )

    missing_entities = missing_required_entities(entities)
    if missing_entities:
        investigation.evidence_missing.extend(
            f"critical_entity:{item}" for item in missing_entities
        )
        investigation.stop_reason = "missing_entity"
        investigation.conclusion = (
            "No se puede iniciar una investigación funcional completa porque faltan "
            "las entidades críticas: " + ", ".join(missing_entities) + "."
        )
        investigation.confidence, investigation.confidence_reason = "LOW", "Faltan entidades críticas."
        return investigation

    gateway = mcp_gateway
    if gateway is None:
        gateway = McpEvidenceGateway.from_qas_runtime_env()

    knowledge = search_unified(
        client,
        question,
        max_results=max_steps,
        ref=ref,
        mcp_gateway=None,
    )
    for result in knowledge.results:
        investigation.evidence_collected.append(_normalize_knowledge_evidence(result))

    capabilities = ()
    selected: dict[str, Any] = {}
    if gateway is not None:
        try:
            validation = gateway.validate_runtime_allowlist()
            invalid = [item for item in validation if not item.get("valid")]
            if invalid:
                investigation.stop_reason = "missing_capability"
                investigation.evidence_missing.append("QAS allowlist validation failed")
            else:
                capabilities = discover_capabilities(gateway)
                selected = match_capabilities(plan.required_evidence, capabilities)
        except (PermissionError, ValueError, OSError) as exc:
            investigation.stop_reason = "missing_capability"
            investigation.evidence_missing.append(f"QAS capability discovery unavailable: {exc}")

    missing_capabilities = [
        evidence_type for evidence_type in plan.required_evidence
        if evidence_type not in selected
    ]
    investigation.evidence_missing.extend(
        f"capability:{item}" for item in missing_capabilities
    )

    if gateway is not None and not investigation.stop_reason and selected:
        for evidence_type in plan.required_evidence:
            if len(investigation.steps) > max_steps:
                investigation.stop_reason = "max_steps_reached"
                break
            capability = selected.get(evidence_type)
            if capability is None:
                continue
            arguments = _query_arguments(capability, entities)
            if arguments is None:
                investigation.evidence_missing.append(
                    f"query_arguments:{evidence_type}:{capability.name}"
                )
                continue
            try:
                runtime = gateway.read_runtime(capability.name, arguments)
            except (PermissionError, ValueError, OSError) as exc:
                investigation.evidence_missing.append(
                    f"runtime_call:{evidence_type}:{capability.name}:{exc}"
                )
                continue
            investigation.evidence_collected.append(_normalize_runtime_evidence(runtime))
            investigation.provenance.append(_provenance(investigation.evidence_collected[-1]))

    investigation.correlation = correlate_evidence(investigation.evidence_collected)

    runtime_items = [item for item in investigation.evidence_collected if item.landscape == "QAS"]
    if runtime_items:
        investigation.findings.append(
            f"Se obtuvieron {len(runtime_items)} observaciones de runtime QAS en modo read-only."
        )
    if knowledge.results:
        investigation.findings.append(
            f"Se recuperaron {len(knowledge.results)} evidencias de Knowledge para contextualizar la investigación."
        )

    assessment = assess_evidence(
        UnifiedSearchResult(
            query=question.strip(),
            results=knowledge.results,
            sap_standard=knowledge.sap_standard,
            internal=knowledge.internal,
            mcp=knowledge.mcp,
        )
    )
    reasoning = reason_from_evidence(assessment)

    if investigation.stop_reason is None:
        if assessment.conflicts:
            investigation.stop_reason = "conflicting_evidence"
        elif not runtime_items:
            investigation.stop_reason = "missing_capability"
        elif missing_capabilities:
            investigation.stop_reason = "missing_capability"
        else:
            investigation.stop_reason = "evidence_sufficient"

    if investigation.stop_reason == "evidence_sufficient":
        investigation.conclusion = (
            "La evidencia disponible permite continuar la correlación funcional, "
            "pero la causa raíz solo debe afirmarse cuando los valores de stock y "
            "movimientos relevantes estén directamente observados y sean consistentes."
        )
    elif investigation.stop_reason == "conflicting_evidence":
        investigation.conclusion = reasoning.conclusion
    elif investigation.stop_reason == "missing_entity":
        pass
    else:
        investigation.conclusion = (
            "No se pudo determinar una causa raíz con la evidencia disponible. "
            "La investigación queda acotada a los datos observados y a las capacidades "
            "que el entorno QAS anunció y autorizó."
        )

    investigation.confidence, investigation.confidence_reason = _confidence(
        investigation.evidence_collected,
        investigation.evidence_missing,
        bool(assessment.conflicts),
    )
    if not investigation.hypotheses and investigation.stop_reason != "evidence_sufficient":
        investigation.hypotheses.append(
            "La diferencia puede estar relacionada con movimientos o stock no observados; "
            "esta hipótesis requiere evidencia QAS adicional y no constituye un hecho."
        )
    return investigation


def render_investigation(investigation: Investigation) -> str:
    lines = [
        f"Investigation Case: {investigation.case_id}",
        "",
        f"Intent: {investigation.intent}",
        "",
        "Entities:",
    ]
    lines.extend(
        f"- {item.entity_type} = {item.value}"
        for item in investigation.entities
    )
    lines.extend(["", "Evidence:"])
    lines.extend(
        f"- [{item.evidence_id}] {item.provider}/{item.operation} · {item.landscape} · certainty={item.certainty}"
        for item in investigation.evidence_collected
    )
    lines.extend(["", "Findings:"])
    lines.extend(f"- {item}" for item in investigation.findings) or lines.append("- None")
    lines.extend(["", "Hypotheses:"])
    lines.extend(f"- {item}" for item in investigation.hypotheses) or lines.append("- None")
    lines.extend(["", "Conclusion:", investigation.conclusion or "No conclusion."])
    lines.extend(["", "Confidence:", investigation.confidence])
    lines.append(investigation.confidence_reason)
    lines.extend(["", "Missing information:"])
    lines.extend(f"- {item}" for item in investigation.evidence_missing) or lines.append("- None")
    lines.extend(["", "Stop reason:", investigation.stop_reason or "unknown"])
    lines.extend(["", "Provenance:"])
    lines.extend(f"- {item['evidence_id']} · {item['provider']} · {item['operation']} · {item['landscape']}" for item in investigation.provenance) or lines.append("- None")
    return "\n".join(lines) + "\n"
