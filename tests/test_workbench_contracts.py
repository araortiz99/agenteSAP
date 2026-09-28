from src.app.contracts import build_workbench_analysis
from src.agent.consultant import ConsultationResult, Citation, TicketContextReference
from src.tools.evidence import EvidenceAssessment, EvidenceItem
from src.tools.evidence_trace import TraceabilityReport, EvidenceTrace
from src.tools.reason import ReasoningResult
from src.tools.search_unified import UnifiedSearchResult
from src.tools.get_related_knowledge import RelatedKnowledge, Relationship


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
    return ConsultationResult(
        request="material master",
        retrieval=UnifiedSearchResult("material master", (), (), (), ()),
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
    )


def test_workbench_response_is_structured_and_traceable():
    result = build_workbench_analysis(
        _consultation(),
        request_id="REQ-TEST",
        intent="consult",
        diagnostics={"total_latency_ms": 1.2},
        runtime={"mode": "QAS", "status": "disabled", "access": "read-only"},
    )

    assert result.request_id == "REQ-TEST"
    assert result.trace_id == "TRACE-TEST"
    assert result.intent == "consult"
    assert result.evidence[0]["evidence_id"] == "EVD-TEST"
    assert result.relationships[0]["target_id"] == "ZMM_TEST"
    assert result.confirmed == ("Hecho confirmado.",)
    assert result.implementation == ("Implementación documentada.",)
    assert result.gaps == ()
    assert result.runtime["writes_exposed"] is not True
