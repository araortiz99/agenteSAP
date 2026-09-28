from src.tools.entity_resolution import ResolvedEntity, _merge_candidate, _normalize_id


def test_entity_id_normalization_is_deterministic():
    assert _normalize_id("  mara   ") == "MARA"


def test_same_entity_keeps_cross_layer_provenance():
    internal = ResolvedEntity("MARA", "SAP_OBJECT", "internal.md", 0.8, "metadata", "confirmed", "internal")
    standard = ResolvedEntity(" mara ", "SAP_OBJECT", "standard.md", 0.9, "content", "confirmed", "sap_standard")
    merged = _merge_candidate(internal, standard)
    assert merged.entity_id == "MARA"
    assert merged.path == "internal.md"
    assert merged.provenance_paths == ("internal.md", "standard.md")
    assert merged.provenance_layers == ("internal", "sap_standard")


def test_exact_match_rank_beats_higher_content_score():
    metadata = ResolvedEntity("MARA", "SAP_OBJECT", "metadata.md", 0.6, "metadata", "confirmed", "internal")
    content = ResolvedEntity("MARA", "SAP_OBJECT", "content.md", 0.99, "content", "confirmed", "sap_standard")
    merged = _merge_candidate(metadata, content)
    assert merged.path == "metadata.md"
    assert merged.match_type == "metadata"
