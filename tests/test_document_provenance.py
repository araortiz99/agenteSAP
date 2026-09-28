from src.document.chunking import chunk_document
from src.document.provenance import chunk_to_record
from src.document.source import DocumentSource
from src.document.structure import parse_text_structure

def test_chunk_record_has_stable_source_provenance():
    source=DocumentSource("s","manual.md","# MM\n\nMIGO mueve stock.")
    chunk=chunk_document(parse_text_structure(source))[0]
    a=chunk_to_record(chunk,source.filename)
    b=chunk_to_record(chunk,source.filename)
    assert a==b
    assert a.provenance.document_id==source.document_id
    assert a.provenance.chunk_id==chunk.chunk_id
    assert a.provenance.filename=="manual.md"

def test_record_identity_is_deterministic():
    source=DocumentSource("s","x.txt","551")
    chunk=chunk_document(parse_text_structure(source))[0]
    assert chunk_to_record(chunk,"x.txt").record_id==chunk_to_record(chunk,"x.txt").record_id
