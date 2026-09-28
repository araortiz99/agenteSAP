"""CLI for safe QAS MCP tool discovery.

Discovery performs only MCP tools/list. It never executes an SAP tool.
"""

from __future__ import annotations

import argparse
import json

from src.sap.mcp_gateway import McpEvidenceGateway


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Discover the QAS MCP tool catalog without executing SAP tools."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    discover = subparsers.add_parser(
        "discover-qas",
        help="List the tools advertised by the QAS MCP server.",
    )
    discover.add_argument(
        "--pretty",
        action="store_true",
        help="Pretty-print the JSON catalog.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    if args.command == "discover-qas":
        gateway = McpEvidenceGateway.from_qas_runtime_env()
        if gateway is None:
            raise PermissionError(
                "QAS runtime discovery is disabled; set "
                "AGENTESAP_SAP_RUNTIME_ENABLED=true"
            )
        catalog = gateway.discover_qas_tools()
        print(
            json.dumps(
                [
                    {
                        "name": item.name,
                        "description": item.description,
                        "input_schema": item.input_schema,
                        "read_only_hint": item.read_only_hint,
                        "destructive_hint": item.destructive_hint,
                    }
                    for item in catalog
                ],
                ensure_ascii=False,
                indent=2 if args.pretty else None,
                default=str,
            )
        )
        return 0

    raise AssertionError(f"Unsupported command: {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())
