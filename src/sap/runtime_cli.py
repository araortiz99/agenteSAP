"""Safe QAS MCP catalog inspection CLI.

This command calls only MCP tools/list. It never invokes a SAP tool.
Credentials remain in the local sap-mcp-server configuration.
"""

from __future__ import annotations

import argparse
import json

from src.sap.mcp_gateway import McpEvidenceGateway


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Inspect the allowlisted SAP MCP QAS tool catalog without calling tools."
    )
    parser.add_argument(
        "--catalog",
        action="store_true",
        help="List the QAS MCP server tool catalog; no SAP operation is invoked.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if not args.catalog:
        print("Use --catalog to inspect the QAS MCP tool catalog.")
        return 2

    gateway = McpEvidenceGateway.for_qas_catalog_inspection()
    catalog = gateway.inspect_runtime_tools()

    # In catalog-only mode the sentinel intentionally filters everything out,
    # so inspect the underlying client directly through a dedicated path.
    # This function is replaced below by the gateway's catalog-only inspector.
    print(json.dumps(catalog, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
