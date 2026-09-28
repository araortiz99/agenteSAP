"""Command-line entry point for the read-only SAP consultant."""

from __future__ import annotations

import argparse
from dataclasses import asdict, is_dataclass
import json
import os

from src.agent.router import run_agent
from src.github.client import GitHubClient


def main() -> int:
    parser = argparse.ArgumentParser(description="agenteSAP LLM consultant")
    parser.add_argument("request", help="Consultative request in natural language")
    parser.add_argument("--owner", default=os.getenv("GITHUB_OWNER", "araortiz99"))
    parser.add_argument("--repo", default=os.getenv("GITHUB_REPO", "agenteSAP"))
    parser.add_argument("--ref", default=os.getenv("GITHUB_REF", "main"))
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print the complete agent response as JSON",
    )
    args = parser.parse_args()

    github = GitHubClient(args.owner, args.repo, token=os.getenv("GITHUB_TOKEN"))
    response = run_agent(github, args.request, ref=args.ref)

    if args.json:
        if not is_dataclass(response):
            raise TypeError("Agent response is not serializable")
        print(json.dumps(asdict(response), ensure_ascii=False, indent=2))
    elif hasattr(response.result, "answer"):
        print(response.result.answer)
    else:
        print(response.result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
