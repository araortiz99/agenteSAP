from src.document.source import DocumentSource
from src.document.structure import parse_text_structure
from src.document.chunking import chunk_document

def test_structure_preserves_headings():
    s = DocumentSource("x", "x.md", "# Inventario\n\nMIGO mueve stock.\n\n## Ajuste\n\n551 registra merma.")
    st = parse_text_structure(s)
    assert st.blocks[0].kind == "heading"
    assert st.blocks[1].heading == "Inventario"
    assert st.blocks[2].heading == "Ajuste"

def test_chunking_is_deterministic_and_bounded():
    s = DocumentSource("x", "x.txt", "A" * 5000)
    st = parse_text_structure(s)
    a = chunk_document(st, max_chunk_chars=500, max_chunks=20)
    b = chunk_document(st, max_chunk_chars=500, max_chunks=20)
    assert a == b
    assert len(a) <= 20
    assert all(len(x.content) <= 500 for x in a)

def test_chunk_ids_change_with_content():
    a = chunk_document(parse_text_structure(DocumentSource("a", "a.txt", "one")))
    b = chunk_document(parse_text_structure(DocumentSource("b", "b.txt", "two")))
    assert a[0].chunk_id != b[0].chunk_id

def test_invalid_limits_fail_closed():
    st = parse_text_structure(DocumentSource("x", "x.txt", "x"))
    try:
        chunk_document(st, max_chunks=0)
    except ValueError as exc:
        assert "chunk limits" in str(exc)
    else:
        raise AssertionError("expected ValueError")
