from src.tools.search_unified import UnifiedResult, unified_result_key
from src.tools.knowledge_context import ContextEvidence


def _result(system):
    return UnifiedResult(
        path="mcp://sap_mcp_server/read_table",
        score=0.9,
        matched_terms=("MARA",),
        content=f"Observation from {system}",
        source_layer="mcp",
        match_type="mcp",
        source_id="MARA",
        knowledge_type="runtime_observation",
        knowledge_scope="runtime",
        certainty="partial",
        provenance=(
            ("provider", "sap_mcp_server"),
            ("operation", "read_table"),
            ("system", system),
            ("landscape", system),
            ("object_id", "MARA"),
            ("observation_type", "runtime_observation"),
        ),
    )


def test_unified_result_key_distinguishes_runtime_systems():
    assert unified_result_key(_result("QAS")) != unified_result_key(_result("PRD"))


def test_unified_result_key_is_stable_for_provenance_order():
    first = _result("QAS")
    second = UnifiedResult(
        path=first.path,
        score=first.score,
        matched_terms=first.matched_terms,
        content=first.content,
        source_layer=first.source_layer,
        match_type=first.match_type,
        source_id=first.source_id,
        knowledge_type=first.knowledge_type,
        knowledge_scope=first.knowledge_scope,
        certainty=first.certainty,
        provenance=tuple(reversed(first.provenance)),
    )
    assert unified_result_key(first) == unified_result_key(second)


def test_context_evidence_keeps_result_reference():
    result = _result("QAS")
    evidence = ContextEvidence(result=result, hop=0, discovery="direct")
    assert evidence.result is result
