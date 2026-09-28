"""CLI for safe QAS MCP tool discovery.

Discovery performs only MCP tools/list. It never executes an SAP tool.
"""

from __future__ import annotations

import argparse
import json
import os

from src.sap.mcp_gateway import McpEvidenceGateway
from src.sap.qas_runtime import SapQasRuntimeConfig


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

    validate = subparsers.add_parser(
        "validate-qas",
        help="Validate the configured QAS read-tool allowlist using only tools/list.",
    )
    validate.add_argument(
        "--pretty",
        action="store_true",
        help="Pretty-print the JSON validation.",
    )
    readiness = subparsers.add_parser(
        "readiness-qas",
        help="Report QAS runtime readiness without executing a SAP tool.",
    )
    readiness.add_argument(
        "--pretty",
        action="store_true",
        help="Pretty-print the JSON readiness report.",
    )

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    if args.command == "validate-qas":
        gateway = McpEvidenceGateway.from_qas_runtime_env()
        if gateway is None:
            raise PermissionError(
                "QAS runtime validation is disabled; set "
                "AGENTESAP_SAP_RUNTIME_ENABLED=true"
            )
        results = gateway.validate_runtime_allowlist()
        print(
            json.dumps(
                list(results),
                ensure_ascii=False,
                indent=2 if args.pretty else None,
            )
        )
        if not all(bool(item.get("valid")) for item in results):
            return 2
        return 0

    if args.command == "readiness-qas":
        try:
            config = SapQasRuntimeConfig.from_env()
        except ValueError as exc:
            report = {
                "enabled": os.getenv("AGENTESAP_SAP_RUNTIME_ENABLED", "false").lower()
                in {"1", "true", "yes", "on"},
                "landscape": os.getenv("AGENTESAP_SAP_RUNTIME_LANDSCAPE", "QAS"),
                "scope": os.getenv("AGENTESAP_SAP_RUNTIME_SCOPE", "mcp_readonly"),
                "discovery_only": os.getenv(
                    "AGENTESAP_SAP_RUNTIME_DISCOVERY_ONLY", "false"
                ).lower()
                in {"1", "true", "yes", "on"},
                "allowlist_configured": bool(
                    os.getenv("AGENTESAP_SAP_RUNTIME_READ_TOOLS", "").strip()
                ),
                "command_configured": bool(
                    os.getenv("AGENTESAP_SAP_RUNTIME_COMMAND", "sap-mcp-server").strip()
                ),
                "runtime_ready": False,
                "reason": str(exc),
            }
            print(
                json.dumps(
                    report,
                    ensure_ascii=False,
                    indent=2 if args.pretty else None,
                )
            )
            return 2

        report = {
            "enabled": config.enabled,
            "landscape": config.landscape,
            "scope": config.scope,
            "discovery_only": config.discovery_only,
            "allowlist_configured": bool(config.allowed_tools),
            "command_configured": bool(config.command),
            "runtime_ready": False,
            "reason": "live MCP catalog not verified",
        }
        if config.landscape != "QAS":
            report["reason"] = "landscape must be QAS"
        elif config.scope != "mcp_readonly":
            report["reason"] = "scope must be mcp_readonly"
        elif not config.enabled:
            report["reason"] = "runtime disabled"
        elif not config.allowed_tools and not config.discovery_only:
            report["reason"] = "explicit allowlist or discovery_only is required"
        elif not config.command:
            report["reason"] = "MCP command is not configured"
        print(
            json.dumps(
                report,
                ensure_ascii=False,
                indent=2 if args.pretty else None,
            )
        )
        return 0 if report["runtime_ready"] else 2

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
