from src.sap_help.ingestion import chunk_markdown, content_hash, normalize_content
from src.sap_help.model import SAPHelpDocument, SAPHelpMetadata, validate_metadata


def metadata(**overrides):
    values = {
        "repository": "SAP-docs/example",
        "branch": "main",
        "commit_sha": "abc123",
        "path": "docs/mm/material.md",
        "document_id": "MAT-MASTER",
        "title": "Material Master",
        "product": "SAP S/4HANA",
        "component": "MM",
        "version": "2025 FPS01",
        "language": "en",
        "help_url": "https://help.sap.com/example",
        "source_url": "https://github.com/SAP-docs/example/blob/main/docs/mm/material.md",
        "license": "CC-BY-4.0",
        "authority_level": "official",
        "confidence": "confirmed",
        "status": "candidate",
    }
    values.update(overrides)
    return SAPHelpMetadata(**values)


def test_normalization_and_hash_are_deterministic():
    assert normalize_content("a  \r\nb\r") == "a\nb"
    assert content_hash("a\n") == content_hash("a\r\n")


def test_metadata_requires_provenance_for_git_identity():
    try:
        validate_metadata(metadata(repository=None, commit_sha="abc123"))
    except ValueError as exc:
        assert "commit_sha requires repository" in str(exc)
    else:
        raise AssertionError("invalid provenance was accepted")


def test_branch_requires_repository_provenance():
    try:
        validate_metadata(metadata(repository=None, branch="main", commit_sha=None, path=None))
    except ValueError as exc:
        assert "branch requires repository" in str(exc)
    else:
        raise AssertionError("branch without repository was accepted")


def test_inferred_metadata_requires_confidence():
    try:
        validate_metadata(metadata(metadata_origin="inferred", confidence=None))
    except ValueError as exc:
        assert "inferred metadata requires explicit confidence" in str(exc)
    else:
        raise AssertionError("inferred metadata without confidence was accepted")


def test_structural_chunking_preserves_heading_hierarchy_and_provenance():
    document = SAPHelpDocument(
        metadata=metadata(),
        content="# Material Master\nIntro\n## Plant Data\nPlant text\n### Storage\nStorage text",
    )
    chunks = chunk_markdown(document)
    assert len(chunks) == 3
    assert chunks[1].section_path == ("Material Master", "Plant Data")
    assert chunks[2].section_path == ("Material Master", "Plant Data", "Storage")
    assert chunks[2].parent_heading == "Plant Data"
    assert chunks[2].metadata.repository == "SAP-docs/example"
    assert chunks[2].metadata.content_hash == content_hash(document.content)
    assert chunks[2].content_hash == content_hash("Storage text")
    assert len({chunk.chunk_id for chunk in chunks}) == len(chunks)


def test_repeated_content_in_different_sections_has_distinct_chunk_ids():
    document = SAPHelpDocument(
        metadata=metadata(),
        content="# A\nSame text\n# B\nSame text",
    )
    chunks = chunk_markdown(document)
    assert len(chunks) == 2
    assert chunks[0].content_hash == chunks[1].content_hash
    assert chunks[0].chunk_id != chunks[1].chunk_id
