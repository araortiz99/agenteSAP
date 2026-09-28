from src.app.contracts import build_workbench_analysis
from src.agent.consultant import ConsultationResult, Citation, TicketContextReference
from src.tools.evidence import EvidenceAssessment, EvidenceItem
from src.tools.evidence_trace import TraceabilityReport, EvidenceTrace
from src.tools.reason import ReasoningResult
from src.tools.search_unified import UnifiedResult, UnifiedSearchResult
from src.tools.get_related_knowledge import RelatedKnowledge, Relationship
from src.tools.entity_resolution import ResolvedEntity
from src.tools.knowledge_context import ContextRelationship, KnowledgeContext


def _consultation() -> ConsultationResult:
    evidence_item = EvidenceItem(
        path="knowledge/sap-standard/mm/material-master.md",
        source_layer="sap_standard",
        source_id="SAP-HELP-MM",
        knowledge_type="standard",
        knowledge_scope="global",
        certainty="confirmed",
        weight=4.0,
        supports=True,
        reason="documented",
    )
    assessment = EvidenceAssessment(
        query="material master",
        items=(evidence_item,),
        confirmed=(evidence_item,),
        partial=(),
        under_validation=(),
        unsupported=(),
        conflicts=(),
        gaps=(),
        requires_analysis=False,
    )
    reasoning = ReasoningResult(
        query="material master",
        conclusion_status="supported",
        conclusion="Supported by retrieved evidence.",
        evidence=assessment,
        conflicts=(),
    )
    trace = EvidenceTrace(
        evidence_id="EVD-TEST",
        path=evidence_item.path,
        source_layer=evidence_item.source_layer,
        source_id=evidence_item.source_id,
        knowledge_type=evidence_item.knowledge_type,
        knowledge_scope=evidence_item.knowledge_scope,
        certainty=evidence_item.certainty,
        weight=evidence_item.weight,
        role="supporting",
        reason=evidence_item.reason,
    )
    traceability = TraceabilityReport(
        trace_id="TRACE-TEST",
        query="material master",
        conclusion_status="supported",
        conclusion=reasoning.conclusion,
        evidence=(trace,),
        supporting_evidence_ids=("EVD-TEST",),
        unresolved_evidence_ids=(),
        gaps=(),
        conflicts=(),
    )
    relation = Relationship(
        path="knowledge/relationships/test.md",
        source_id="TICKET-1",
        source_type="TICKET",
        relation_type="documents",
        target_id="ZMM_TEST",
        target_type="SAP_OBJECT",
        content="documented",
        certainty="confirmed",
        status="confirmed",
        evidence_source_id="REL-1",
    )
    entity = ResolvedEntity(
        entity_id="TICKET-1",
        entity_type="TICKET",
        path="knowledge/tickets/test.md",
        score=1.0,
        match_type="identifier",
        certainty="confirmed",
        source_layer="internal",
    )
    knowledge_context = KnowledgeContext(
        query="material master",
        entities=(entity,),
        relationships=(ContextRelationship(relation, 1),),
        evidence=(),
        gaps=(),
        conflicts=(),
        max_hops=2,
    )
    return ConsultationResult(
        request="material master",
        retrieval=UnifiedSearchResult(
            "material master",
            (
                UnifiedResult(
                    path=evidence_item.path,
                    score=0.91,
                    matched_terms=("material", "master"),
                    content="documented",
                    source_layer="sap_standard",
                    match_type="identifier",
                    source_id="SAP-HELP-MM",
                    knowledge_type="standard",
                    knowledge_scope="global",
                    certainty="confirmed",
                ),
            ),
            (),
            (),
            (),
        ),
        evidence=assessment,
        reasoning=reasoning,
        traceability=traceability,
        answer=(
            "## Resumen\nResultado.\n\n"
            "## Qué está confirmado\n- Hecho confirmado.\n\n"
            "## Qué corresponde a nuestra implementación\n- Implementación documentada.\n\n"
            "## Qué no está confirmado\n- Nada adicional.\n\n"
            "## Evidencias\n[EVD-TEST]\n\n"
            "## Ticket\nSin ticket.\n\n"
            "## Próximos pasos\nValidar."
        ),
        model="fake",
        citations=(
            Citation("CIT-1", "EVD-TEST", evidence_item.path, evidence_item.source_id, "confirmed"),
        ),
        uncited_evidence_ids=(),
        ticket_context=(),
        ticket_relationships=RelatedKnowledge(
            entity_type="TICKET",
            entity_id="TICKET-1",
            relationships=(relation,),
        ),
        knowledge_context=knowledge_context,
    )


def test_workbench_response_is_structured_and_traceable():
    result = build_workbench_analysis(
        _consultation(),
        request_id="REQ-TEST",
        intent="consult",
        diagnostics={"total_latency_ms": 1.2},
        runtime={"mode": "QAS", "status": "disabled", "access": "read-only", "writes_exposed": False},
    )

    assert result.request_id == "REQ-TEST"
    assert result.trace_id == "TRACE-TEST"
    assert result.intent == "consult"
    assert result.evidence[0]["evidence_id"] == "EVD-TEST"
    assert result.retrieval[0]["path"] == "knowledge/sap-standard/mm/material-master.md"
    assert result.retrieval[0]["score"] == 0.91
    assert result.retrieval[0]["source_layer"] == "sap_standard"
    assert result.retrieval[0]["provenance"] == ()
    assert result.relationships[0]["target_id"] == "ZMM_TEST"
    assert result.knowledge_intelligence["max_hops"] == 2
    assert result.knowledge_intelligence["entities"][0]["entity_id"] == "TICKET-1"
    assert result.knowledge_intelligence["relationships"][0]["hop"] == 1
    assert result.confirmed == ("Hecho confirmado.",)
    assert result.implementation == ("Implementación documentada.",)
    assert result.gaps == ()
    assert result.runtime["writes_exposed"] is False
    assert result.hypotheses == ()
    assert result.findings == ()
    assert result.evidence_states == ()


def test_workbench_html_has_evidence_and_provenance_explorer():
    from pathlib import Path
    html = Path("src/app/static/index.html").read_text(encoding="utf-8")
    for marker in ("evidenceList", "provenanceViewer", "retrievalExplorer", "renderEvidenceExplorer", "renderRetrievalExplorer", "kiEntities", "kiGraph", "renderKnowledgeIntelligence", "conclusionStatus", "findingsList"):
        assert marker in html
    assert "source_layer" in html
    assert "provenance" in html


def test_workbench_exposes_conclusion_and_report_when_investigation_exists():
    from types import SimpleNamespace
    consultation = _consultation()
    consultation = ConsultationResult(**{
        **consultation.__dict__,
        "investigation": SimpleNamespace(
            hypotheses=(),
            findings=("finding",),
            conclusion_status="QUALIFIED",
            conclusion_reason="missing evidence",
            evidence_states=(),
            report=SimpleNamespace(as_dict=lambda: {"case_id": "WB-TEST", "conclusion_status": "QUALIFIED"}),
        ),
    })
    result = build_workbench_analysis(
        consultation,
        request_id="REQ-REPORT",
        intent="consult",
        diagnostics={},
        runtime={"mode": "QAS", "writes_exposed": False},
    )
    assert result.conclusion_status == "QUALIFIED"
    assert result.conclusion_reason == "missing evidence"
    assert result.findings == ("finding",)
    assert result.investigation_report["case_id"] == "WB-TEST"
