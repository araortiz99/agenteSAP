from src.document.chunking import chunk_document
from src.document.provenance import chunk_to_record
from src.document.sap_entities import extract_sap_entities
from src.document.source import DocumentSource
from src.document.structure import parse_text_structure

def test_extracts_sap_entities_with_position():
    s=DocumentSource("s","x.txt","MIGO ZMM_IM_0002 uses MARA and movement 551")
    c=chunk_document(parse_text_structure(s))[0]
    entities=extract_sap_entities(chunk_to_record(c,s.filename))
    values={(x.entity_type,x.value) for x in entities}
    assert ("TABLE","MARA") in values
    assert ("Z_PROGRAM","ZMM_IM_0002") in values
    assert all(x.position>=0 for x in entities)

def test_entity_limit_is_bounded():
    s=DocumentSource("s","x.txt","MIGO MARA MARC MARD EKKO EKPO BKPF BSEG ACDOCA")
    c=chunk_document(parse_text_structure(s))[0]
    assert len(extract_sap_entities(chunk_to_record(c,s.filename),max_entities=2))==2


def test_document_links_are_bounded():
    from src.document.links import document_links
    class E:
        value="MARA"
        entity_type="TABLE"
    assert document_links("DOC-1",(E(),),"R")[0][1]=="MARA"
