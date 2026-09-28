            f"El caso 31426 queda sujeto a la evidencia disponible [{evidence_id}].\n\n"
            "## Qué está confirmado\n"
            f"ZMM_IMX_0004 está documentado como implementación custom [{evidence_id}].\n\n"
            "## Qué corresponde a nuestra implementación\n"
            f"El contexto corresponde a nuestra implementación y al proceso SNC K1 [{evidence_id}].\n\n"
            "## Qué no está confirmado\n"
            f"No está confirmada la causa raíz, solución definitiva ni evidencia QA [{evidence_id}]. "
            "La discrepancia K1/K4 requiere análisis.\n\n"
            "## Evidencias\n"
            f"[{evidence_id}]\n\n"
            "## Ticket\n"
            f"Contexto del ticket [{ticket_id.group(0)}]\n\n"
            "## Próximos pasos\n"
            "Validar contra el ticket original y evidencia QA."
        )


def _direct_results(client, query, max_results, ref, mcp_gateway=None):
    results = []
    for path, content in client.files.items():
        is_standard = path.startswith("knowledge/sap-standard")
        layer = "sap_standard" if is_standard else "internal"
        source_id = "SAP-MM-MATERIAL" if is_standard else "SRC-31426-KB-20260918"
        ktype = "standard" if is_standard else "custom"
        scope = "global" if is_standard else "ticket"
        certainty = "confirmed" if is_standard else "partial"
        score = 1.0 if any(
            term.lower() in content.lower() or term.lower() in path.lower()
            for term in query.split()
        ) else 0.1
        results.append(
            UnifiedResult(
                path=path, score=score, matched_terms=tuple(query.split()),
                content=content, source_layer=layer, match_type="content",
                source_id=source_id, knowledge_type=ktype,
                knowledge_scope=scope, certainty=certainty,
            )
        )
    results.sort(key=lambda x: (-x.score, x.path))
    return UnifiedSearchResult(
        query=query, results=tuple(results[:max_results]),
        sap_standard=tuple(x for x in results if x.source_layer == "sap_standard"),
        internal=tuple(x for x in results if x.source_layer == "internal"),
        mcp=(),
    )


def _with_retrieval_patch():
    import src.agent.consultant as module
    import src.tools.knowledge_context as context_module
    import src.tools.entity_resolution as entity_module
    from src.tools.search_knowledge import SearchResult

    original = (
        module.search_unified,
        context_module.search_unified,
        entity_module.search_knowledge,
        entity_module.search_sap_standard,
    )
    module.search_unified = _direct_results
    context_module.search_unified = _direct_results
