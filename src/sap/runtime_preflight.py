"""QAS runtime preflight: validate MCP readiness without executing SAP operations."""

from __future__ import annotations

from src.sap.mcp_gateway import McpEvidenceGateway


def run_preflight() -> dict[str, object]:
    """Validate QAS MCP configuration and advertised read-only tools."""
    try:
        gateway = McpEvidenceGateway.from_qas_runtime_env()
    except (PermissionError, ValueError) as exc:
        return {"enabled": True, "ready": False, "reason": str(exc)}

    if gateway is None:
        return {
            "enabled": False,
            "ready": False,
            "reason": "AGENTESAP_SAP_RUNTIME_ENABLED is not enabled",
        }

    try:
        validation = gateway.validate_runtime_allowlist()
    except (PermissionError, ValueError) as exc:
        return {
            "enabled": True,
            "ready": False,
            "provider": gateway.target.provider,
            "landscape": gateway.target.metadata.get("landscape"),
            "read_only": gateway.target.read_only,
            "reason": str(exc),
        }

    invalid = [item for item in validation if not item.get("valid")]
    return {
        "enabled": True,
        "ready": not invalid,
        "provider": gateway.target.provider,
        "landscape": gateway.target.metadata.get("landscape"),
        "system": gateway.target.metadata.get("system"),
        "read_only": gateway.target.read_only,
        "allowlisted_tools": list(gateway.target.allowed_tools),
        "validation": list(validation),
        "invalid_tools": [item["name"] for item in invalid],
    }
