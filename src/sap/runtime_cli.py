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
    readiness.add_argument(
        "--verify-catalog",
        action="store_true",
        help="Verify the live MCP tools/list catalog without executing an SAP tool.",
    )

    read = subparsers.add_parser(
        "read-qas",
        help="Execute exactly one explicitly allowlisted QAS read-only MCP tool.",
    )
    read.add_argument("--tool", required=True, help="Exact allowlisted MCP tool name.")
    read.add_argument(
        "--arguments",
        default="{}",
        help="JSON object passed to the selected read-only MCP tool.",
    )
    read.add_argument("--pretty", action="store_true", help="Pretty-print the evidence.")

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    if args.command == "read-qas":
        gateway = McpEvidenceGateway.from_qas_runtime_env()
        if gateway is None:
            raise PermissionError(
                "QAS runtime reads are disabled; set AGENTESAP_SAP_RUNTIME_ENABLED=true"
            )
        try:
            arguments = json.loads(args.arguments)
        except json.JSONDecodeError as exc:
            raise ValueError("--arguments must be valid JSON") from exc
        if not isinstance(arguments, dict):
            raise ValueError("--arguments must be a JSON object")
        validation = {
            item["name"]: item
            for item in gateway.validate_runtime_allowlist()
        }
        selected = validation.get(args.tool)
        if selected is None:
            raise PermissionError(f"MCP runtime tool '{args.tool}' is not allowlisted")
        if not selected.get("valid"):
            raise PermissionError(
                f"MCP runtime tool '{args.tool}' is not ready: {selected.get('reason')}"
            )
        evidence = gateway.read_runtime(args.tool, arguments)
        print(
            json.dumps(
                {
                    "provider": evidence.provider,
                    "operation": evidence.operation,
                    "landscape": evidence.landscape,
                    "system": evidence.system,
                    "object_id": evidence.object_id,
                    "observation_type": evidence.observation_type,
                    "certainty": evidence.certainty,
                    "content": evidence.content,
                    "provenance": dict(evidence.provenance),
                },
                ensure_ascii=False,
                indent=2 if args.pretty else None,
                default=str,
            )
        )
        return 0

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
            landscape = os.getenv("AGENTESAP_SAP_RUNTIME_LANDSCAPE", "QAS").upper()
            scope = os.getenv("AGENTESAP_SAP_RUNTIME_SCOPE", "mcp_readonly")
            if landscape != "QAS":
                reason = "landscape must be QAS"
            elif scope != "mcp_readonly":
                reason = "scope must be mcp_readonly"
            else:
                reason = str(exc)
            report = {
                "enabled": os.getenv("AGENTESAP_SAP_RUNTIME_ENABLED", "false").lower()
                in {"1", "true", "yes", "on"},
                "landscape": landscape,
                "scope": scope,
                "discovery_only": os.getenv(
                    "AGENTESAP_SAP_RUNTIME_DISCOVERY", "false"
                ).lower()
                in {"1", "true", "yes", "on"},
                "allowlist_configured": bool(
                    os.getenv("AGENTESAP_SAP_RUNTIME_READ_TOOLS", "").strip()
                ),
                "command_configured": bool(
                    os.getenv("AGENTESAP_SAP_MCP_COMMAND", "sap-mcp-server").strip()
                ),
                "runtime_ready": False,
                "reason": reason,
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
            "catalog_verified": False,
            "allowlist_validated": False,
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
        elif config.discovery_only:
            report["reason"] = "discovery-only mode does not authorize runtime reads"
        elif args.verify_catalog:
            try:
                gateway = McpEvidenceGateway.from_qas_runtime_env()
                if gateway is None:
                    report["reason"] = "runtime disabled"
                else:
                    results = gateway.validate_runtime_allowlist()
                    report["catalog_verified"] = True
                    report["allowlist_validated"] = all(
                        bool(item.get("valid")) for item in results
                    )
                    if report["allowlist_validated"]:
                        report["runtime_ready"] = True
                        report["reason"] = "live MCP catalog verified and allowlist is read-only"
                    else:
                        invalid = next(
                            item for item in results if not bool(item.get("valid"))
                        )
                        report["reason"] = (
                            f"configured tool '{invalid.get('name')}' is not ready: "
                            f"{invalid.get('reason')}"
                        )
            except (OSError, PermissionError, RuntimeError, ValueError) as exc:
                report["reason"] = f"catalog verification failed: {exc}"
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
