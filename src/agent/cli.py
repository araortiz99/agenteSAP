"""Command-line entry point for the read-only SAP consultant."""

from __future__ import annotations

import argparse
import os

from src.agent.router import run_agent
from src.github.client import GitHubClient


def main() -> int:
    parser = argparse.ArgumentParser(description="agenteSAP LLM consultant")
    parser.add_argument("request", help="Consultative request in natural language")
    parser.add_argument("--owner", default=os.getenv("GITHUB_OWNER", "araortiz99"))
    parser.add_argument("--repo", default=os.getenv("GITHUB_REPO", "agenteSAP"))
    parser.add_argument("--ref", default=os.getenv("GITHUB_REF", "main"))
    args = parser.parse_args()

    github = GitHubClient(args.owner, args.repo, token=os.getenv("GITHUB_TOKEN"))
    response = run_agent(github, args.request, ref=args.ref)
    result = response.result

    if hasattr(result, "answer"):
        print(result.answer)
    else:
        print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
