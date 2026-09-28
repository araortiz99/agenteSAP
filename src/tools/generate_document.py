"""Deterministic document generation capability for the MVP."""

from __future__ import annotations

import re
from dataclasses import dataclass

from src.github.client import GitHubClient
from src.tools.analyze import AnalysisResult, analyze


TEMPLATE_PATHS = {
    "requirement": "templates/requirement.md",
    "analysis": "templates/analysis.md",
    "functional-specification": "templates/functional-specification.md",
    "functional-test": "templates/functional-tests.md",
    "investigation": "templates/investigation.md",
}


class DocumentGenerationError(RuntimeError):
    """Raised when a document cannot be generated safely."""


@dataclass(frozen=True)
class GeneratedDocument:
    document_type: str
    ticket_id: str | None
    version: str
    status: str
    content: str
    source_paths: tuple[str, ...]


def _template_path(document_type: str) -> str:
    try:
        return TEMPLATE_PATHS[document_type]
    except KeyError as exc:
        raise DocumentGenerationError(
            f"Unsupported document_type: {document_type}"
        ) from exc


def _metadata_block(
    document_type: str,
    ticket_id: str | None,
    *,
    knowledge_type: str = "unknown",
    knowledge_scope: str = "unknown",
    version: str = "1.0",
    status: str = "draft",
    date: str = "",
    author: str = "",
) -> str:
    return "\n".join(
        [
            "---",
            f'ticket_id: "{ticket_id or ""}"',
            f'document_type: "{document_type}"',
            f'knowledge_type: "{knowledge_type}"',
            f'knowledge_scope: "{knowledge_scope}"',
            f'version: "{version}"',
            f'status: "{status}"',
            f'date: "{date}"',
            f'author: "{author}"',
            "---",
        ]
    )


def _pending() -> str:
    return "Información pendiente de validar."


def _bullet_lines(items: tuple[str, ...] | list[str]) -> str:
    return "\n".join(f"- {item}" for item in items) if items else _pending()


def _relationship_lines(analysis_result: AnalysisResult) -> str:
    relationships = analysis_result.relationships.relationships
    if not relationships:
        return "No existen relaciones explícitamente documentadas."
    return "\n".join(
        f"- {r.source_type} {r.source_id} {r.relation_type} "
        f"{r.target_type} {r.target_id}"
        for r in relationships
    )


def _analysis_document(
    analysis_result: AnalysisResult,
    *,
    date: str,
    author: str,
) -> str:
    sections = {
        "1. Objetivo del análisis": analysis_result.request,
        "2. Contexto": f"Ticket {analysis_result.ticket_id}.",
        "3. Información disponible": (
            f"Se recuperaron {len(analysis_result.context.documents)} "
            "documentos del ticket."
        ),
        "4. Hechos identificados": _bullet_lines(analysis_result.facts),
        "5. Evidencias": _relationship_lines(analysis_result),
        "6. Análisis funcional": (
            "El MVP recuperó y estructuró evidencia. La interpretación "
            "funcional detallada requiere revisión de las evidencias recuperadas."
        ),
        "7. Hipótesis": "No se generan hipótesis automáticamente en este MVP.",
        "8. Información faltante": _bullet_lines(
            analysis_result.missing_information
        ),
        "9. Impactos identificados": _pending(),
        "10. Dependencias": _pending(),
        "11. Conclusión": analysis_result.conclusion,
        "12. Próximos pasos": (
            "Revisar las evidencias recuperadas y completar la información pendiente."
        ),
        "13. Documentación relacionada": _bullet_lines(
            [document.path for document in analysis_result.context.documents]
        ),
    }
    return _render_document(
        "Análisis",
        "analysis",
        analysis_result.ticket_id,
        sections,
        date=date,
        author=author,
    )


def _render_document(
    title: str,
    document_type: str,
    ticket_id: str | None,
    sections: dict[str, str],
    *,
    date: str,
    author: str,
) -> str:
    output = [
        f"# {title}",
        "",
        "## Metadata",
        "",
        _metadata_block(document_type, ticket_id, date=date, author=author),
        "",
    ]
    for heading, body in sections.items():
        output.extend([f"## {heading}", "", body or _pending(), ""])
    return "\n".join(output).rstrip() + "\n"


def _build_sections(
    document_type: str,
    ticket_id: str | None,
    analysis_result: AnalysisResult | None,
) -> tuple[str, dict[str, str]]:
    if analysis_result is None:
        facts: tuple[str, ...] = ()
        relationships = "No existen relaciones explícitamente documentadas."
        documents = "Información pendiente de validar."
        request = "Información pendiente de validar."
        conclusion = "No existe evidencia de ticket recuperada para este documento."
    else:
        facts = analysis_result.facts
        relationships = _relationship_lines(analysis_result)
        documents = _bullet_lines(
            [document.path for document in analysis_result.context.documents]
        )
        request = analysis_result.request
        conclusion = analysis_result.conclusion

    common = {
        "requirement": (
            "Requerimiento",
            {
                "1. Antecedente": documents,
                "2. Situación actual": _bullet_lines(facts),
                "3. Necesidad / Problema": request,
                "4. Objetivo": request,
                "5. Alcance": _pending(),
                "6. Fuera de alcance": _pending(),
                "7. Impacto funcional": _pending(),
                "8. Criterios de aceptación": _pending(),
                "9. Información adicional": relationships,
                "10. Documentación relacionada": documents,
            },
        ),
        "functional-specification": (
            "Especificación Funcional",
            {
                "1. Antecedente": documents,
                "2. Motivo": request,
                "3. Objetivo": request,
                "4. Alcance": _pending(),
                "5. Situación actual": _bullet_lines(facts),
                "6. Solución funcional propuesta": _pending(),
                "7. Flujo funcional": _pending(),
                "8. Reglas de negocio": _pending(),
                "9. Validaciones": _pending(),
                "10. Escenarios": _pending(),
                "11. Datos involucrados": _pending(),
                "12. Objetos SAP relacionados": relationships,
                "13. Integraciones": _pending(),
                "14. Impactos": _pending(),
                "15. Dependencias": _pending(),
                "16. Riesgos": _pending(),
                "17. Criterios de aceptación": _pending(),
                "18. Consideraciones para pruebas": _pending(),
                "19. Documentación relacionada": documents,
            },
        ),
        "functional-test": (
            "Pruebas Funcionales",
            {
                "1. Objetivo": request,
                "2. Versión funcional validada": _pending(),
                "3. Ambiente": _pending(),
                "4. Precondiciones": _pending(),
                "5. Datos de prueba": _pending(),
                "6. Casos de prueba": (
                    "No se generan casos ni resultados de prueba automáticamente. "
                    "Deben completarse con datos, pasos, resultado esperado, "
                    "resultado obtenido, estado y evidencia."
                ),
                "7. Pruebas negativas": _pending(),
                "8. Pruebas de regresión": _pending(),
                "9. Resultado general": _pending(),
                "10. Incidencias encontradas": _pending(),
                "11. Evidencias": relationships,
                "12. Documentación relacionada": documents,
            },
        ),
        "investigation": (
            "Investigación",
            {
                "1. Objetivo": request,
                "2. Pregunta de investigación": request,
                "3. Fuentes consultadas": documents,
                "4. Información encontrada": _bullet_lines(facts),
                "5. Análisis": conclusion,
                "6. Relaciones identificadas": relationships,
                "7. Conclusiones": conclusion,
                "8. Información pendiente de validar": _pending(),
                "9. Documentación relacionada": documents,
            },
        ),
    }

    return common[document_type]


def _template_headings(template: str) -> tuple[str, ...]:
    """Return structural Markdown headings declared by the official template."""
    return tuple(
        line.strip()
        for line in template.splitlines()
        if re.match(r"^##\s+", line.strip())
    )


def _validate_generated(
    document_type: str,
    content: str,
    template: str,
) -> None:
    """Validate generated structure against the official template contract."""
    required = {
        "requirement": [
            "## Metadata",
            "## 1. Antecedente",
            "## 10. Documentación relacionada",
        ],
        "analysis": [
            "## Metadata",
            "## 1. Objetivo del análisis",
            "## 13. Documentación relacionada",
        ],
        "functional-specification": [
            "## Metadata",
            "## 1. Antecedente",
            "## 19. Documentación relacionada",
        ],
        "functional-test": [
            "## Metadata",
            "## 1. Objetivo",
            "## 12. Documentación relacionada",
        ],
        "investigation": [
            "## Metadata",
            "## 1. Objetivo",
            "## 9. Documentación relacionada",
        ],
    }[document_type]

    missing = [heading for heading in required if heading not in content]
    if missing:
        raise DocumentGenerationError(
            f"Generated document is structurally incomplete: {missing}"
        )

    if not template.strip():
        raise DocumentGenerationError("Official template is empty")

    # If the official template declares Markdown section headings, require the
    # generated document to preserve every declared section. This keeps the
    # deterministic renderer aligned with template evolution without inventing
    # semantic content for sections whose evidence is missing.
    template_headings = _template_headings(template)
    if template_headings:
        missing_template_sections = [
            heading for heading in template_headings if heading not in content
        ]
        if missing_template_sections:
            raise DocumentGenerationError(
                "Generated document does not preserve official template sections: "
                f"{missing_template_sections}"
            )


def generate_document(
    client: GitHubClient,
    document_type: str,
    request: str,
    ticket_id: str | None = None,
    *,
    ref: str = "main",
    date: str = "",
    author: str = "",
) -> GeneratedDocument:
    """Generate a safe document instance from repository evidence."""
    normalized_type = document_type.strip().lower()
    if not request.strip():
        raise ValueError("request must not be empty")

    template_path = _template_path(normalized_type)
    template = client.get_file(template_path, ref=ref)

    analysis_result: AnalysisResult | None = None
    if ticket_id:
        analysis_result = analyze(
            client,
            request,
            ticket_id,
            ref=ref,
        )

    if normalized_type == "analysis":
        if not ticket_id:
            raise DocumentGenerationError(
                "analysis generation requires ticket_id in the MVP"
            )
        content = _analysis_document(
            analysis_result,
            date=date,
            author=author,
        )
    else:
        title, sections = _build_sections(
            normalized_type,
            ticket_id,
            analysis_result,
        )
        content = _render_document(
            title,
            normalized_type,
            ticket_id,
            sections,
            date=date,
            author=author,
        )

    _validate_generated(normalized_type, content, template)

    source_paths = [template_path]
    if analysis_result is not None:
        source_paths.extend(
            document.path for document in analysis_result.context.documents
        )
        source_paths.extend(
            relationship.path
            for relationship in analysis_result.relationships.relationships
        )

    return GeneratedDocument(
        document_type=normalized_type,
        ticket_id=ticket_id,
        version="1.0",
        status="draft",
        content=content,
        source_paths=tuple(dict.fromkeys(source_paths)),
    )
