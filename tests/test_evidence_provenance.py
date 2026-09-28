from src.tools.evidence import EvidenceItem, EvidenceAssessment
from src.tools.reason import ReasoningResult
from src.tools.evidence_trace import build_traceability


def _reasoning(item: EvidenceItem) -> ReasoningResult:
    assessment = EvidenceAssessment(
        query="material master",
        items=(item,),
        confirmed=(item,) if item.certainty == "confirmed" else (),
        partial=(),
        under_validation=(),
        unsupported=(),
        conflicts=(),
        gaps=(),
        requires_analysis=False,
    )
    return ReasoningResult(
        query=assessment.query,
        conclusion_status="supported",
        conclusion="bounded",
        evidence=assessment,
        conflicts=(),
    )


def _item(provenance=()):
    return EvidenceItem(
        path="mcp://sap_mcp_server/read_table",
        source_layer="mcp",
        source_id="MARA",
        knowledge_type="runtime_observation",
        knowledge_scope="runtime",
        certainty="confirmed",
        weight=2.0,
        supports=True,
        reason="runtime observation",
        provenance=provenance,
    )


def test_provenance_changes_evidence_identity():
    first = build_traceability(
        _reasoning(_item((("system", "QAS"), ("landscape", "QAS"))))
    ).evidence[0].evidence_id
    second = build_traceability(
        _reasoning(_item((("system", "PRD"), ("landscape", "PRD"))))
    ).evidence[0].evidence_id

    assert first != second


def test_provenance_order_is_stable_for_same_key_values():
    first = build_traceability(
        _reasoning(_item((("system", "QAS"), ("landscape", "QAS"))))
    ).evidence[0].evidence_id
    second = build_traceability(
        _reasoning(_item((("landscape", "QAS"), ("system", "QAS"))))
    ).evidence[0].evidence_id

    assert first == second
