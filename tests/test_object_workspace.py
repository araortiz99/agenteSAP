from dataclasses import dataclass
from src.tools.knowledge_context import ContextEvidence, ContextRelationship, KnowledgeContext
from src.tools.object_workspace import _select_identity, _runtime_payload


@dataclass(frozen=True)
class FakeResult:
    path: str
    score: float = 0.9
    matched_terms: tuple[str, ...] = ()
    source_layer: str = "internal"
    match_type: str = "identifier"
    source_id: str | None = None
    knowledge_type: str = "internal"
    knowledge_scope: str = "implementation"
    certainty: str = "confirmed"
    provenance: tuple[tuple[str, str], ...] = ()


@dataclass(frozen=True)
class FakeEntity:
    entity_id: str
    entity_type: str
    path: str
    score: float
    match_type: str
    certainty: str
    source_layer: str


def _context(entities=(), evidence=(), relationships=()):
    return KnowledgeContext(
        query="ZMM_IMX_0004",
        entities=tuple(entities),
        relationships=tuple(relationships),
        evidence=tuple(evidence),
        gaps=(),
        conflicts=(),
        max_hops=2,
    )


def test_object_identity_resolves_exact_sap_object():
    entity = FakeEntity(
        "ZMM_IMX_0004", "SAP_OBJECT", "knowledge/objects/zmm.md",
        1.0, "identifier", "confirmed", "internal",
    )
    identity = _select_identity("zmm_imx_0004", _context((entity,)))
    assert identity.status == "resolved"
    assert identity.match_type == "exact"
    assert identity.object_id == "ZMM_IMX_0004"


def test_object_identity_is_ambiguous_when_multiple_supported_candidates():
    entities = (
        FakeEntity("MIRO", "SAP_OBJECT", "a.md", 0.9, "content", "confirmed", "internal"),
        FakeEntity("MIRO", "TICKET", "b.md", 0.8, "content", "confirmed", "internal"),
    )
    identity = _select_identity("MIRO", _context(entities))
    assert identity.status == "ambiguous"
    assert len(identity.candidates) == 2


def test_object_identity_does_not_promote_unsupported_entities():
    entity = FakeEntity(
        "PROC-001", "PROCESS", "knowledge/processes/p.md",
        1.0, "identifier", "confirmed", "internal",
    )
    identity = _select_identity("PROC-001", _context((entity,)))
    assert identity.status == "unresolved"
    assert identity.certainty == "unknown"


def test_runtime_payload_only_marks_observed_from_runtime_evidence():
    evidence = ContextEvidence(
        result=FakeResult(
            path="mcp://sap/query",
            source_layer="mcp",
            source_id="ZMM_IMX_0004",
            knowledge_type="runtime_observation",
            knowledge_scope="runtime",
            certainty="confirmed",
        ),
        hop=0,
        discovery="direct",
    )
    payload = _runtime_payload(_context(evidence=(evidence,)))
    assert payload["status"] == "observed"
    assert payload["landscape"] == "QAS"
    assert payload["access"] == "read-only"


def test_runtime_payload_without_runtime_evidence_is_not_observed():
    payload = _runtime_payload(_context())
    assert payload["status"] == "disabled"
    assert payload["landscape"] == "QAS"


def test_runtime_and_knowledge_are_not_merged():
    knowledge = ContextEvidence(
        result=FakeResult(
            path="knowledge/internal/object.md",
            source_layer="internal",
            source_id="ZMM_IMX_0004",
            knowledge_type="implementation",
            knowledge_scope="internal",
            certainty="confirmed",
        ),
        hop=0,
        discovery="direct",
    )
    payload = _runtime_payload(_context(evidence=(knowledge,)))
    assert payload["status"] == "not_observed"
