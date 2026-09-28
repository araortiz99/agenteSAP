from src.document.provenance import DocumentRecord
from src.investigation.contracts import InvestigationEvidence


def record_to_investigation_evidence(record: DocumentRecord) -> InvestigationEvidence:
    p = record.provenance
    authority = record.authority
    provenance = (
        ("source_type", "DOCUMENT"),
        ("document_id", p.document_id),
        ("chunk_id", p.chunk_id),
        ("filename", p.filename),
        ("sequence", str(p.sequence)),
        ("heading", p.heading or ""),
        ("authority", authority.authority.value),
        ("origin", authority.origin.value),
        ("knowledge_version", authority.version),
        ("content_hash", authority.content_hash),
        ("source_path", authority.source_path),
    )
    return InvestigationEvidence(
        evidence_id="EVD-" + record.record_id.removeprefix("REC-"),
        provider="document",
        operation="ingest",
        landscape="KNOWLEDGE",
        system=None,
        object_type="DOCUMENT",
        object_id=p.document_id,
        observation_type="document_chunk",
        content=record.content,
        certainty="documented",
        provenance=provenance,
    )
