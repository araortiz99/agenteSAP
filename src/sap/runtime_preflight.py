"""QAS runtime preflight: connect, inspect MCP catalog, execute nothing."""

from __future__ import annotations

import json

from src.sap.mcp_gateway import McpEvidenceGateway


def run_preflight() -> dict[str, object]:
    gateway = McpEvidenceGateway.from_qas_runtime_env()
    if gateway is None:
        return {
            "enabled": False,
            "ready": False,
            "reason": "AGENTESAP_SAP_RUNTIME_ENABLED is not enabled",
        }

    descriptors = gateway.runtime_tool_catalog()
    advertised = {item.name for item in descriptors}
    allowlisted = set(gateway.target.allowed_tools)
    missing = sorted(allowlisted - advertised)

    return {
        "enabled": True,
        "ready": not missing,
        "provider": gateway.target.provider,
        "landscape": gateway.target.metadata.get("landscape"),
        "system": gateway.target.metadata.get("system"),
        "read_only": gateway.target.read_only,
        "allowlisted_tools": sorted(allowlisted),
        "advertised_allowlisted_tools": sorted(allowlisted & advertised),
        "missing_allowlisted_tools": missing,
        "tool_catalog": [
            {
                "name": item.name,
                "description": item.description,
                "input_schema": item.input_schema,
            }
            for item in descriptors
            if item.name in allowlisted
        ],
    }


def main() -> None:
    print(json.dumps(run_preflight(), ensure_ascii=False, indent=2, default=str))


if __name__ == "__main__":
    main()
