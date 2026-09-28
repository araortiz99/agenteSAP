"""Explicit QAS read-only runtime invocation CLI.

This command intentionally requires the tool name and JSON arguments. It does
not let an LLM invent or discover an executable operation implicitly.
"""

from __future__ import annotations

import argparse
import json
import sys

from src.sap.mcp_gateway import McpEvidenceGateway


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Execute one explicitly allowlisted QAS read-only MCP tool."
    )
    parser.add_argument("--tool", required=True)
    parser.add_argument(
        "--args",
        default="{}",
        help="JSON object passed to the allowlisted read tool.",
    )
    parser.add_argument("--json", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        arguments = json.loads(args.args)
        if not isinstance(arguments, dict):
            raise ValueError("--args must be a JSON object")

        gateway = McpEvidenceGateway.from_qas_runtime_env()
        if gateway is None:
            print(
                "QAS runtime is disabled. Set "
                "AGENTESAP_SAP_RUNTIME_ENABLED=true to opt in.",
                file=sys.stderr,
            )
            return 2

        gateway.preflight_runtime_tools()
        evidence = gateway.read_runtime(args.tool, arguments)
    except Exception as exc:
        print(f"QAS MCP read failed: {exc}", file=sys.stderr)
        return 1

    payload = evidence.as_metadata()
    payload["content"] = evidence.content

    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print("QAS MCP read: OK")
        print(f"provider={evidence.provider}")
        print(f"operation={evidence.operation}")
        print(f"landscape={evidence.landscape}")
        if evidence.system:
            print(f"system={evidence.system}")
        print("content:")
        print(evidence.content)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
