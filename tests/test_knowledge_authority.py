import hashlib
import pytest

from src.knowledge.authority import (
    KnowledgeAuthority,
    KnowledgeOrigin,
    build_authority_record,
    can_promote_to_authoritative,
    content_hash,
)


def test_content_hash_is_deterministic():
    assert content_hash("abc") == hashlib.sha256(b"abc").hexdigest()


def test_authoritative_requires_explicit_approval():
    with pytest.raises(ValueError, match="approved_by"):
        build_authority_record(
            source_id="DOC-1",
            content="business rule",
            version="1.0",
            authority=KnowledgeAuthority.AUTHORITATIVE,
            origin=KnowledgeOrigin.BUSINESS_DOCUMENT,
            scope="organization",
            title="Inventory rule",
            source_path="knowledge/business-rules/inventory.md",
        )


def test_authoritative_record_is_reusable_as_truth():
    record = build_authority_record(
        source_id="DOC-1",
        content="business rule",
        version="1.0",
        authority=KnowledgeAuthority.AUTHORITATIVE,
        origin=KnowledgeOrigin.BUSINESS_DOCUMENT,
        scope="organization",
        title="Inventory rule",
        source_path="knowledge/business-rules/inventory.md",
        approved_by="functional-owner",
    )
    assert record.reusable_as_truth is True
    assert record.metadata()["authority"] == "authoritative"


def test_superseded_requires_predecessor():
    with pytest.raises(ValueError, match="supersedes"):
        build_authority_record(
            source_id="DOC-2",
            content="old rule",
            version="1.0",
            authority=KnowledgeAuthority.SUPERSEDED,
            origin=KnowledgeOrigin.BUSINESS_DOCUMENT,
            scope="organization",
            title="Old rule",
            source_path="knowledge/business-rules/old.md",
        )


def test_generated_knowledge_can_never_be_authoritative():
    assert can_promote_to_authoritative(
        origin=KnowledgeOrigin.GENERATED,
        version="1.0",
        approved_by="owner",
        has_provenance=True,
        has_security_review=True,
    ) is False


def test_authoritative_promotion_requires_all_gates():
    assert can_promote_to_authoritative(
        origin=KnowledgeOrigin.BUSINESS_DOCUMENT,
        version="1.0",
        approved_by="owner",
        has_provenance=True,
        has_security_review=True,
    ) is True

    assert can_promote_to_authoritative(
        origin=KnowledgeOrigin.BUSINESS_DOCUMENT,
        version="1.0",
        approved_by="owner",
        has_provenance=False,
        has_security_review=True,
    ) is False
