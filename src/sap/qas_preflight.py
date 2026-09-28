"""CLI preflight for the optional QAS read-only SAP MCP runtime."""

from __future__ import annotations

import argparse
import json
import sys

from src.sap.mcp_gateway import McpEvidenceGateway


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Preflight the configured QAS read-only SAP MCP server."
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Render the discovered tool catalog as JSON.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        gateway = McpEvidenceGateway.from_qas_runtime_env()
        if gateway is None:
            print(
                "QAS runtime is disabled. Set "
                "AGENTESAP_SAP_RUNTIME_ENABLED=true to opt in."
            )
            return 2

        tools = gateway.preflight_runtime_tools()
    except Exception as exc:
        print(f"QAS MCP preflight failed: {exc}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps({"landscape": "QAS", "tools": tools}, indent=2))
    else:
        print("QAS MCP preflight: OK")
        print("landscape=QAS")
        print(f"tools={len(tools)}")
        for tool in tools:
            print(f"- {tool}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
