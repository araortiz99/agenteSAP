from src.tools.knowledge_context import ContextEvidence, ContextRelationship, KnowledgeContext
from src.tools.get_related_knowledge import Relationship
from src.tools.object_workspace import build_object_workspace
from src.tools.entity_resolution import ResolvedEntity
from src.tools.search_unified import UnifiedResult


class FakeClient:
    pass


def _relationship():
    return ContextRelationship(
        relationship=Relationship(
            path="knowledge/relationships/object-ticket.md",
            source_id="ZMM_IMX_0004",
            source_type="SAP_OBJECT",
            relation_type="related_to",
            target_id="31426",
            target_type="TICKET",
            content="documented",
            certainty="confirmed",
            status="confirmed",
            evidence_source_id="REL-1",
        ),
        hop=1,
    )


def _evidence():
    return ContextEvidence(
        result=UnifiedResult(
            path="knowledge/objects/zmm_imx_0004.md",
            score=0.95,
            matched_terms=("ZMM_IMX_0004",),
            content="documented",
            source_layer="internal",
            match_type="identifier",
            source_id="ZMM_IMX_0004",
            knowledge_type="implementation",
            knowledge_scope="internal",
            certainty="confirmed",
            provenance=(),
        ),
        hop=0,
        discovery="direct",
    )


def test_object_workspace_reuses_knowledge_context(monkeypatch):
    context = KnowledgeContext(
        query="ZMM_IMX_0004",
        entities=(
            ResolvedEntity(
                entity_id="ZMM_IMX_0004",
                entity_type="SAP_OBJECT",
                path="knowledge/objects/zmm_imx_0004.md",
                score=1.0,
                match_type="identifier",
                certainty="confirmed",
                source_layer="internal",
            ),
        ),
        relationships=(_relationship(),),
        evidence=(_evidence(),),
        gaps=(),
        conflicts=(),
        max_hops=2,
    )
    monkeypatch.setattr(
        "src.tools.object_workspace.build_knowledge_context",
        lambda *args, **kwargs: context,
    )

    result = build_object_workspace(FakeClient(), "ZMM_IMX_0004")

    assert result.identity.status == "resolved"
    assert result.object["id"] == "ZMM_IMX_0004"
    assert result.relationships[0]["target_id"] == "31426"
    assert result.tickets[0]["target_id"] == "31426"
    assert result.runtime["status"] == "disabled"
    assert result.diagnostics["read_only"] is True


def test_object_workspace_does_not_invent_runtime(monkeypatch):
    context = KnowledgeContext(
        query="ZMM_IMX_0004",
        entities=(
            ResolvedEntity(
                entity_id="ZMM_IMX_0004",
                entity_type="SAP_OBJECT",
                path="object.md",
                score=1.0,
                match_type="identifier",
                certainty="confirmed",
                source_layer="internal",
            ),
        ),
        relationships=(),
        evidence=(_evidence(),),
        gaps=(),
        conflicts=(),
        max_hops=2,
    )
    monkeypatch.setattr(
        "src.tools.object_workspace.build_knowledge_context",
        lambda *args, **kwargs: context,
    )
    result = build_object_workspace(FakeClient(), "ZMM_IMX_0004")
    assert result.runtime["status"] == "disabled"
    assert result.runtime["evidence_count"] == 0
