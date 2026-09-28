from dataclasses import dataclass

import pytest

from src.tools.knowledge_change import KnowledgeChangeError, build_change_proposal
from src.tools.publish_knowledge import publish_knowledge


VALID = """---
ticket_id: "31426"
document_type: "sap-object"
knowledge_type: "custom"
knowledge_scope: "ticket"
version: "1.0"
status: "draft"
date: "2026-09-28"
author: "agent"
---

# ZMM_IMX_0004
"""


def test_scope_gate_rejects_non_knowledge_path():
    with pytest.raises(KnowledgeChangeError):
        build_change_proposal(
            path="standards/security.md",
            content=VALID,
            base_ref="main",
            branch="docs/knowledge-test",
        )


def test_branch_gate_rejects_main():
    with pytest.raises(KnowledgeChangeError):
        build_change_proposal(
            path="knowledge/test.md",
            content=VALID,
            base_ref="main",
            branch="main",
        )


def test_metadata_gate_rejects_missing_metadata():
    with pytest.raises(KnowledgeChangeError):
        build_change_proposal(
            path="knowledge/test.md",
            content="# incomplete",
            base_ref="main",
            branch="docs/knowledge-test",
        )


def test_security_gate_rejects_private_key():
    with pytest.raises(KnowledgeChangeError):
        build_change_proposal(
            path="knowledge/test.md",
            content=VALID + "\n-----BEGIN PRIVATE KEY-----\nsecret\n",
            base_ref="main",
            branch="docs/knowledge-test",
        )


def test_version_gate_requires_higher_version():
    existing = VALID
    with pytest.raises(KnowledgeChangeError):
        build_change_proposal(
            path="knowledge/test.md",
            content=VALID,
            base_ref="main",
            branch="docs/knowledge-test",
            existing_content=existing,
        )


def test_update_accepts_higher_version():
    updated = VALID.replace('version: "1.0"', 'version: "1.1"')
    proposal = build_change_proposal(
        path="knowledge/test.md",
        content=updated,
        base_ref="main",
        branch="docs/knowledge-test",
        existing_content=VALID,
    )
    assert proposal.operation == "update"
    assert proposal.old_version == "1.0"
    assert proposal.new_version == "1.1"


@dataclass
class FakeWriter:
    calls: list

    def create_branch(self, branch, *, base_ref):
        self.calls.append(("branch", branch, base_ref))
        return "base-sha"

    def get_file(self, path, *, ref):
        self.calls.append(("get_file", path, ref))
        return None

    def put_file(self, path, content, *, branch, message, sha=None):
        self.calls.append(("put_file", path, branch, message, sha))
        return "commit-sha"

    def create_pull_request(self, *, title, body, head, base):
        self.calls.append(("pr", title, head, base))
        return {"number": 7, "html_url": "https://example.invalid/pr/7"}


def test_publish_creates_branch_commit_and_pr_without_merge():
    proposal = build_change_proposal(
        path="knowledge/test.md",
        content=VALID,
        base_ref="main",
        branch="docs/knowledge-test",
    )
    writer = FakeWriter([])
    result = publish_knowledge(
        writer,
        proposal,
        commit_message="docs: publish knowledge test",
        pr_title="docs: publish knowledge test",
        pr_body="governance",
    )

    assert result.pull_request_number == 7
    assert result.commit_sha == "commit-sha"
    assert [call[0] for call in writer.calls] == [
        "branch",
        "get_file",
        "put_file",
        "pr",
    ]
    assert all(call[0] != "merge" for call in writer.calls)
