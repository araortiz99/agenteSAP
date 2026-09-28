from src.document.provenance import DocumentRecord
from src.investigation.contracts import InvestigationEvidence

def record_to_investigation_evidence(record: DocumentRecord) -> InvestigationEvidence:
    p=record.provenance
    provenance=(
        ("source_type","DOCUMENT"),
        ("document_id",p.document_id),
        ("chunk_id",p.chunk_id),
        ("filename",p.filename),
        ("sequence",str(p.sequence)),
        ("heading",p.heading or ""),
    )
    return InvestigationEvidence(
        evidence_id="EVD-"+record.record_id.removeprefix("REC-"),
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
