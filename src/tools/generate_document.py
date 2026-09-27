"""Deterministic document generation capability for the MVP."""

from __future__ import annotations

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


def _section(title: str, body: str = "Información pendiente de validar.") -> str:
    return f"## {title}\n\n{body}\n"


def _analysis_document(
    analysis_result: AnalysisResult,
    *,
    date: str,
    author: str,
) -> str:
    facts = (
        "\n".join(f"- {fact}" for fact in analysis_result.facts)
        if analysis_result.facts
        else "Información pendiente de validar."
    )
    missing = (
        "\n".join(f"- {item}" for item in analysis_result.missing_information)
        if analysis_result.missing_information
        else "No se identificaron faltantes en la recuperación inicial."
    )

    relationships = (
        "\n".join(
            f"- {r.source_type} {r.source_id} "
            f"{r.relation_type} {r.target_type} {r.target_id}"
            for r in analysis_result.relationships.relationships
        )
        if analysis_result.relationships.relationships
        else "No existen relaciones explícitamente documentadas."
    )

    return "\n".join(
        [
            "# Análisis",
            "",
            "## Metadata",
            "",
            _metadata_block(
                "analysis",
                analysis_result.ticket_id,
                date=date,
                author=author,
            ),
            "",
            _section("1. Objetivo del análisis", analysis_result.request),
            _section("2. Contexto", f"Ticket {analysis_result.ticket_id}."),
            _section(
                "3. Información disponible",
                f"Se recuperaron {len(analysis_result.context.documents)} documentos del ticket.",
            ),
            _section("4. Hechos identificados", facts),
            _section("5. Evidencias", relationships),
            _section(
                "6. Análisis funcional",
                "El MVP recuperó y estructuró evidencia. La interpretación funcional "
                "detallada requiere revisión de las evidencias recuperadas.",
            ),
            _section(
                "7. Hipótesis",
                "No se generan hipótesis automáticamente en este MVP.",
            ),
            _section("8. Información faltante", missing),
            _section(
                "9. Impactos identificados",
                "Información pendiente de validar.",
            ),
            _section(
                "10. Dependencias",
                "Información pendiente de validar.",
            ),
            _section("11. Conclusión", analysis_result.conclusion),
            _section(
                "12. Próximos pasos",
                "Revisar las evidencias recuperadas y completar la información pendiente.",
            ),
            _section(
                "13. Documentación relacionada",
                "\n".join(
                    f"- {document.path}"
                    for document in analysis_result.context.documents
                ),
            ),
        ]
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
    """Generate a safe document instance from repository evidence.

    The MVP fully materializes the analysis document. Other document types
    return their official template structure with explicit pending fields.
    """

    normalized_type = document_type.strip().lower()
    if not request.strip():
        raise ValueError("request must not be empty")

    template_path = _template_path(normalized_type)
    template = client.get_file(template_path, ref=ref)

    if normalized_type == "analysis":
        if not ticket_id:
            raise DocumentGenerationError(
                "analysis generation requires ticket_id in the MVP"
            )

        analysis_result = analyze(
            client,
            request,
            ticket_id,
            ref=ref,
        )

        content = _analysis_document(
            analysis_result,
            date=date,
            author=author,
        )

        return GeneratedDocument(
            document_type=normalized_type,
            ticket_id=analysis_result.ticket_id,
            version="1.0",
            status="draft",
            content=content,
            source_paths=(
                template_path,
                *(document.path for document in analysis_result.context.documents),
                *(relationship.path for relationship in analysis_result.relationships.relationships),
            ),
        )

    # For the remaining document types, use the template as the structural
    # contract and make missing content explicit instead of inventing it.
    content = "\n".join(
        [
            f"# {normalized_type}",
            "",
            "## Metadata",
            "",
            _metadata_block(
                normalized_type,
                ticket_id,
                date=date,
                author=author,
            ),
            "",
            "## Generation status",
            "",
            "Documento generado en modo MVP. El template oficial fue recuperado:",
            f"- {template_path}",
            "",
            "## Información pendiente",
            "",
            "El MVP todavía no materializa contenido específico para este tipo "
            "documental. No se inventó información.",
        ]
    )

    return GeneratedDocument(
        document_type=normalized_type,
        ticket_id=ticket_id,
        version="1.0",
        status="draft",
        content=content,
        source_paths=(template_path,),
    )
