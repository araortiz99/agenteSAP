from src.agent.investigation import investigate
from src.investigation.contracts import InvestigationEvidence


class EmptyClient:
    def get_tree(self, ref="main"):
        return []

    def get_file(self, path, ref="main"):
        raise KeyError(path)


def test_investigation_accepts_explicit_document_evidence():
    evidence = InvestigationEvidence(
        evidence_id="EVD-DOC123",
        provider="document",
        operation="ingest",
        landscape="KNOWLEDGE",
        system=None,
        object_type="DOCUMENT",
        object_id="DOC-1",
        observation_type="document_chunk",
        content="ZMM_IM_0002 registra la merma con movimiento 551.",
        certainty="documented",
        provenance=(
            ("document_id", "DOC-1"),
            ("chunk_id", "CH-1"),
            ("filename", "merma.md"),
        ),
    )

    result = investigate(
        EmptyClient(),
        "¿Qué indica la documentación sobre ZMM_IM_0002?",
        max_results=8,
        additional_evidence=(evidence,),
    )

    assert any(item.source_layer == "internal" for item in result.retrieval.results)
    assert any(item.source_id == "DOC-1" for item in result.retrieval.results)
    assert any(item.provenance for item in result.retrieval.results)
