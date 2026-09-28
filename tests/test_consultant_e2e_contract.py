from src.agent.consultant import consult
from src.investigation.contracts import InvestigationEvidence
from src.tools.search_unified import UnifiedResult
from src.agent.consultant import ConsultationResult


class E2EClient:
    def __init__(self):
        self.files = {
            "knowledge/sap-standard/mm/mara.md": """---
source_id: SAP-MM-MARA
knowledge_type: standard
knowledge_scope: global
certainty: confirmed
---
MARA es parte del maestro de materiales SAP.
""",
            "knowledge/internal/inventory.md": """---
source_id: INT-MM-INVENTORY
knowledge_type: custom
knowledge_scope: organization
certainty: confirmed
---
El proceso interno de Inventario Materia Prima usa una característica específica.
""",
        }

    def get_tree(self, ref="main"):
        return [{"path": p, "type": "blob"} for p in self.files]

    def get_file(self, path, ref="main"):
        return self.files[path]


class E2ELLM:
    model = "fake-e2e"

    def generate(self, *, system_prompt, user_prompt):
        import re
        ids = re.findall(r"EVD-[A-Z0-9]+", user_prompt)
        ids = list(dict.fromkeys(ids))
        citations = " ".join(f"[{x}]" for x in ids[:3])
        return (
            "## Resumen\nConsulta integrada basada en evidencia. " + citations + "\n\n"
            "## Qué está confirmado\nLa evidencia documental y las capas recuperadas se mantienen separadas. " + citations + "\n\n"
            "## Qué corresponde a nuestra implementación\nLa regla interna aparece como evidencia custom. " + citations + "\n\n"
            "## Qué no está confirmado\nEl estado runtime debe verificarse en QAS.\n\n"
            "## Evidencias\n" + citations + "\n\n"
            "## Ticket\nNo se suministró ticket.\n\n"
            "## Próximos pasos\nValidar cualquier discrepancia contra QAS."
        )


def test_consultative_e2e_fuses_standard_internal_document_and_runtime_without_merging_meaning(monkeypatch):
    class RuntimeGateway:
        def supports_source(self, source):
            return source == "runtime"

        def search_resources(self, query):
            return (
                UnifiedResult(
                    path="mcp://sap_mcp_server/read_query",
                    score=1.0,
                    matched_terms=("MARA",),
                    content='{"object":"MARA","landscape":"QAS","rows":[{"MATNR":"100123"}]}',
                    source_layer="mcp",
                    match_type="mcp",
                    source_id="MARA",
                    knowledge_type="runtime_observation",
                    knowledge_scope="runtime",
                    certainty="observed",
                    provenance=(
                        ("provider", "sap_mcp_server"),
                        ("operation", "read_query"),
                        ("landscape", "QAS"),
                        ("system", "S4QAS"),
                    ),
                ),
            )

    monkeypatch.setattr(
        "src.agent.consultant.McpEvidenceGateway.for_request",
        lambda request: RuntimeGateway(),
    )

    document = InvestigationEvidence(
        evidence_id="EVD-DOC-E2E",
        provider="document",
        operation="ingest",
        landscape="KNOWLEDGE",
        system=None,
        object_type="DOCUMENT",
        object_id="DOC-INVENTORY-001",
        observation_type="document_chunk",
        content="La especificación funcional define la regla de Inventario Materia Prima.",
        certainty="documented",
        provenance=(
            ("document_id", "DOC-INVENTORY-001"),
            ("filename", "inventario-materia-prima.md"),
            ("chunk_id", "CH-01"),
        ),
    )

    result = consult(
        E2EClient(),
        "¿Cuál es el estado actual de MARA en QAS y qué indica nuestra documentación?",
        E2ELLM(),
        additional_evidence=(document,),
    )

    assert isinstance(result, ConsultationResult)
    assert result.investigation is not None
    assert result.retrieval.sap_standard
    assert result.retrieval.internal
    assert result.retrieval.mcp
    assert any(x.knowledge_type == "document_chunk" for x in result.retrieval.results)
    assert any(x.knowledge_type == "runtime_observation" for x in result.retrieval.results)
    assert all(x.knowledge_scope == "runtime" for x in result.retrieval.mcp)
    assert any(x.source_id == "DOC-INVENTORY-001" for x in result.retrieval.results)
    assert result.traceability.evidence
    assert result.citations
