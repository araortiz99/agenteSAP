"""CLI helpers for the opt-in SAP QAS runtime integration."""

from __future__ import annotations

import argparse
import json
import sys

from src.sap.mcp_gateway import McpEvidenceGateway


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Controlled AgenteSAP SAP runtime operations."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    discover = subparsers.add_parser(
        "discover-qas",
        help="List the MCP tool catalog exposed by the configured QAS server.",
    )
    discover.add_argument(
        "--pretty",
        action="store_true",
        help="Pretty-print JSON output.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    if args.command == "discover-qas":
        gateway = McpEvidenceGateway.from_qas_runtime_env()
        if gateway is None:
            print(
                "ERROR: QAS runtime discovery is disabled. "
                "Set AGENTESAP_SAP_RUNTIME_ENABLED=true and "
                "AGENTESAP_SAP_RUNTIME_DISCOVERY=true.",
                file=sys.stderr,
            )
            return 2

        tools = gateway.discover_qas_tools()
        payload = [
            {
                "name": tool.name,
                "description": tool.description,
                "input_schema": tool.input_schema,
                "read_only_hint": tool.read_only_hint,
                "destructive_hint": tool.destructive_hint,
            }
            for tool in tools
        ]
        print(
            json.dumps(
                payload,
                ensure_ascii=False,
                indent=2 if args.pretty else None,
                default=str,
            )
        )
        return 0

    raise RuntimeError(f"Unsupported command: {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())
