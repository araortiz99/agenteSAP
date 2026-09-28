"""MVP 5.4 end-to-end contract test for canonical ticket 31426."""

import re
import pytest

from src.agent.consultant import ConsultationFormatError, consult
from src.tools.knowledge_context import build_knowledge_context
from src.tools.search_unified import UnifiedResult, UnifiedSearchResult


class Canonical31426Client:
    def __init__(self):
        self.files = {
            "tickets/31426/ticket.md": """---
ticket_id: "31426"
title: "Error de XML SNC K1 con posiciones de pedido marcadas para borrado"
module: "MM"
status: "candidate"
knowledge_type: "custom"
knowledge_scope: "ticket"
certainty: "partial"
evidence_source_id: "SRC-31426-KB-20260918"
---
# Ticket
ZMM_IMX_0004
SNC K1
EKPO-LOEKZ
No permite afirmar causa raíz, solución definitiva ni QA.
""",
            "knowledge/sap-objects/zmm-imx-0004.md": """---
object_id: "OBJ-0001"
object_type: "Z development"
object_name: "ZMM_IMX_0004"
technical_name: "ZMM_IMX_0004"
module: "MM"
origin: "custom"
implementation_type: "z_development"
knowledge_type: "custom"
knowledge_scope: "process"
certainty: "partial"
---
# SAP Object
ZMM_IMX_0004 es desarrollo Z.
""",
            "knowledge/processes/snc-k1-xml-generation.md": """---
process_id: "PROC-0001"
process_name: "Generación XML SNC K1"
process_type: "custom"
module: "MM"
knowledge_type: "custom"
knowledge_scope: "process"
certainty: "partial"
---
# Process
Generación XML SNC K1 y control de EKPO-LOEKZ.
""",
            "knowledge/relationships/rel-31426-zmm-imx-0004.md": """---
relationship_id: "REL-31426-001"
source_id: "31426"
source_type: "TICKET"
relation_type: "relacionado_con"
target_id: "ZMM_IMX_0004"
target_type: "SAP_OBJECT"
knowledge_type: "custom"
knowledge_scope: "ticket"
certainty: "confirmed"
evidence_source_id: "SRC-31426-KB-20260918"
status: "confirmed"
---
# Relationship
La fuente identifica ZMM_IMX_0004.
## Conflictos
La misma fuente utiliza 31426 posteriormente para K4.
""",
            "knowledge/relationships/rel-31426-snc-k1.md": """---
relationship_id: "REL-31426-002"
source_id: "31426"
source_type: "TICKET"
relation_type: "participa_en"
target_id: "PROC-0001"
target_type: "PROCESS"
knowledge_type: "custom"
knowledge_scope: "ticket"
certainty: "partial"
evidence_source_id: "SRC-31426-KB-20260918"
status: "candidate"
---
# Relationship
Relación derivada del registro textual.
## Conflictos
Existe material posterior que utiliza 31426 para K4.
""",
            "knowledge/sources/src-31426-kb-20260918.md": """---
source_id: "SRC-31426-KB-20260918"
source_type: "other"
source_name: "SAP Functional Knowledge Base — MM / Retail / Inventarios — 2026-09-18"
origin: "internal"
knowledge_type: "mixed"
knowledge_scope: "ticket"
status: "active"
---
# Source
Fuente interna consolidada. No es SAP Standard.
La misma fuente contiene material posterior que usa 31426 para K4.
""",
            "knowledge/sap-standard/mm/material-master.md": """---
knowledge_type: standard
knowledge_scope: global
source_id: SAP-MM-MATERIAL
certainty: confirmed
---
# Material Master
SAP Standard material master information.
""",
        }

    def get_tree(self, ref="main"):
        return [{"path": p, "type": "blob"} for p in self.files]

    def get_file(self, path, ref="main"):
        return self.files[path]


class E2E31426LLM:
    model = "mvp54-fake-model"

    def __init__(self):
        self.system_prompt = ""
        self.user_prompt = ""

    def generate(self, *, system_prompt, user_prompt):
        self.system_prompt = system_prompt
        self.user_prompt = user_prompt
        evidence_ids = re.findall(r"EVD-[A-Z0-9]+", user_prompt)
        assert evidence_ids
        assert "ZMM_IMX_0004" in user_prompt
        assert "SNC K1" in user_prompt
        assert "K4" in user_prompt
        assert "partial" in user_prompt
        assert "candidate" in user_prompt
        assert "SAP Standard" in user_prompt
        assert "## Conflicts" in user_prompt

        evidence_id = evidence_ids[0]
        ticket_id = re.search(r"TKT-[A-Z0-9]+", user_prompt)
        assert ticket_id

        return (
            "## Resumen\n"
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


def _direct_results(client, query, max_results, ref):
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

    def _internal(client, query, max_results=8, ref="main"):
        return tuple(
            SearchResult(
                path=path,
                score=1.0,
                matched_terms=tuple(query.split()),
                content=content,
                match_type="content",
            )
            for path, content in client.files.items()
            if not path.startswith("knowledge/sap-standard")
        )[:max_results]

    def _standard(client, query, max_results=8, ref="main"):
        return tuple(
            SearchResult(
                path=path,
                score=1.0,
                matched_terms=tuple(query.split()),
                content=content,
                match_type="content",
            )
            for path, content in client.files.items()
            if path.startswith("knowledge/sap-standard")
        )[:max_results]

    entity_module.search_knowledge = _internal
    entity_module.search_sap_standard = _standard
    return (module, context_module, entity_module), original


def test_mvp54_canonical_31426_end_to_end():
    client = Canonical31426Client()
    (module, context_module, entity_module), original = _with_retrieval_patch()
    try:
        llm = E2E31426LLM()
        request = (
            "Consultá el ticket 31426: explicame qué está confirmado sobre "
            "ZMM_IMX_0004, SNC K1 y la discrepancia K1/K4."
        )
        result = consult(client, request, llm, ticket_id="31426", max_results=8)
        context = build_knowledge_context(client, request, max_hops=2, ref="main")

        assert any(e.entity_id == "ZMM_IMX_0004" for e in context.entities)
        assert any(
            r.relationship.target_id == "ZMM_IMX_0004"
            and r.relationship.certainty == "confirmed"
            for r in context.relationships
        )
        assert any(
            r.relationship.target_id == "PROC-0001"
            and r.relationship.certainty == "partial"
            and r.relationship.status == "candidate"
            for r in context.relationships
        )
        assert context.conflicts
        assert any("K4" in conflict.description for conflict in context.conflicts)
        assert result.ticket_context
        assert result.ticket_relationships is not None
        assert result.ticket_relationships.relationships
        assert result.citations
        assert result.answer.startswith("## Resumen")
        assert "TKT-" in result.answer
        assert "ZMM_IMX_0004" in llm.user_prompt
        assert "K1" in llm.user_prompt
        assert "K4" in llm.user_prompt
    finally:
        (module.search_unified, context_module.search_unified, entity_module.search_knowledge, entity_module.search_sap_standard) = original


def test_mvp54_rejects_missing_ticket_reference():
    client = Canonical31426Client()
    class BadLLM(E2E31426LLM):
        def generate(self, *, system_prompt, user_prompt):
            super().generate(system_prompt=system_prompt, user_prompt=user_prompt)
            evidence_id = re.search(r"EVD-[A-Z0-9]+", user_prompt).group(0)
            return (
                "## Resumen\nRespuesta.\n\n"
                "## Qué está confirmado\nConfirmado [" + evidence_id + "].\n\n"
                "## Qué corresponde a nuestra implementación\nCustom [" + evidence_id + "].\n\n"
                "## Qué no está confirmado\nPendiente.\n\n"
                "## Evidencias\n[" + evidence_id + "]\n\n"
                "## Ticket\nNo referencia ticket.\n\n"
                "## Próximos pasos\nValidar."
            )

    module, original = _with_retrieval_patch()
    try:
        with pytest.raises(ConsultationFormatError, match="TKT"):
            consult(client, "Consultá el ticket 31426", BadLLM(), ticket_id="31426")
    finally:
        (module.search_unified, context_module.search_unified, entity_module.search_knowledge, entity_module.search_sap_standard) = original
