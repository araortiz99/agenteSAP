from src.document.chunking import chunk_document
from src.document.integration import record_to_investigation_evidence
from src.document.provenance import chunk_to_record
from src.document.source import DocumentSource
from src.document.structure import parse_text_structure

def test_document_record_maps_to_existing_investigation_contract():
    s=DocumentSource("s","manual.md","# MM\n\nMIGO mueve stock.")
    c=chunk_document(parse_text_structure(s))[0]
    e=record_to_investigation_evidence(chunk_to_record(c,s.filename))
    assert e.object_type=="DOCUMENT"
    assert e.landscape=="KNOWLEDGE"
    assert dict(e.provenance)["document_id"]==s.document_id
    assert e.evidence_id.startswith("EVD-DOC-")
