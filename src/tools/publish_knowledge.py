"""Controlled Knowledge publication through a Pull Request."""

from __future__ import annotations

from dataclasses import dataclass

from src.github.writer import GitHubWriteClient
from src.tools.knowledge_change import KnowledgeChangeProposal


@dataclass(frozen=True)
class PublishResult:
    path: str
    branch: str
    base_ref: str
    commit_sha: str
    operation: str
    version: str
    pull_request_number: int
    pull_request_url: str


def publish_knowledge(
    writer: GitHubWriteClient,
    proposal: KnowledgeChangeProposal,
    *,
    commit_message: str,
    pr_title: str,
    pr_body: str,
) -> PublishResult:
    """Create branch, persist one validated Knowledge file and open a PR.

    Never merges the PR.
    """
    writer.create_branch(proposal.branch, base_ref=proposal.base_ref)
    existing = writer.get_file(proposal.path, ref=proposal.branch)
    sha = existing.get("sha") if existing else None

    if proposal.operation == "create" and existing:
        raise RuntimeError(f"Target path already exists on branch: {proposal.path}")
    if proposal.operation == "update" and not existing:
        raise RuntimeError(f"Expected existing Knowledge file not found on branch: {proposal.path}")

    commit_sha = writer.put_file(
        proposal.path,
        proposal.content,
        branch=proposal.branch,
        message=commit_message,
        sha=sha,
    )
    pull_request = writer.create_pull_request(
        title=pr_title,
        body=pr_body,
        head=proposal.branch,
        base=proposal.base_ref,
    )

    try:
        pr_number = int(pull_request["number"])
        pr_url = str(pull_request["html_url"])
    except (KeyError, TypeError, ValueError) as exc:
        raise RuntimeError("GitHub did not return a valid Pull Request") from exc

    return PublishResult(
        path=proposal.path,
        branch=proposal.branch,
        base_ref=proposal.base_ref,
        commit_sha=commit_sha,
        operation=proposal.operation,
        version=proposal.new_version,
        pull_request_number=pr_number,
        pull_request_url=pr_url,
    )
