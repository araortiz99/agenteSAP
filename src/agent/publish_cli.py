"""Explicit CLI for controlled Knowledge publication."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

from src.github.client import GitHubClient
from src.github.writer import GitHubWriteClient
from src.tools.knowledge_change import KnowledgeChangeError, build_change_proposal
from src.tools.publish_knowledge import publish_knowledge


def main() -> int:
    parser = argparse.ArgumentParser(description="agenteSAP controlled Knowledge publication")
    parser.add_argument("--path", required=True)
    parser.add_argument("--file", required=True, help="Local Markdown proposal file")
    parser.add_argument("--base-ref", default="main")
    parser.add_argument("--branch", required=True)
    parser.add_argument("--ticket", default=None)
    parser.add_argument("--change-type", choices=("patch", "minor", "major"), default="minor")
    parser.add_argument("--commit-message", default=None)
    parser.add_argument("--pr-title", default=None)
    parser.add_argument("--pr-body", default=None)
    parser.add_argument("--publish", action="store_true")
    parser.add_argument("--owner", default="araortiz99")
    parser.add_argument("--repo", default="agenteSAP")
    args = parser.parse_args()

    content = Path(args.file).read_text(encoding="utf-8")
    if args.branch.strip() == args.base_ref.strip():
        parser.error("--branch debe ser diferente de --base-ref")

    reader = GitHubClient(args.owner, args.repo, token=None)
    existing = None
    try:
        existing = reader.get_file(args.path, ref=args.base_ref)
    except Exception as exc:
        if "HTTP 404" not in str(exc):
            raise

    try:
        proposal = build_change_proposal(
            path=args.path,
            content=content,
            base_ref=args.base_ref,
            branch=args.branch,
            ticket_id=args.ticket,
            existing_content=existing,
            change_type=args.change_type,
        )
    except KnowledgeChangeError as exc:
        print(f"Knowledge Governance rejected the proposal: {exc}", file=sys.stderr)
        return 2

    print(f"Operation: {proposal.operation}")
    print(f"Path: {proposal.path}")
    print(f"Version: {proposal.new_version}")
    print(f"Base: {proposal.base_ref}")
    print(f"Branch: {proposal.branch}")
    print("Security: PASS")

    if not args.publish:
        print("Dry-run: no GitHub changes were made.")
        return 0

    writer = GitHubWriteClient(args.owner, args.repo)
    result = publish_knowledge(
        writer,
        proposal,
        commit_message=args.commit_message or f"docs: publish knowledge {proposal.path}",
        pr_title=args.pr_title or f"docs: update knowledge {proposal.path}",
        pr_body=args.pr_body or (
            "## Knowledge Governance\n\n"
            f"- Ticket: {proposal.ticket_id or 'N/A'}\n"
            f"- Path: {proposal.path}\n"
            f"- Version: {proposal.new_version}\n"
            f"- Change type: {proposal.change_type}\n"
            f"- Operation: {proposal.operation}\n\n"
            "Created by controlled Knowledge publication. No automatic merge or functional approval."
        ),
    )
    print(f"PR: {result.pull_request_url}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
