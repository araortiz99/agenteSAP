"""Opt-in live smoke test for the real QAS SAP MCP server."""
from __future__ import annotations
import asyncio
import os
import shlex
import pytest
from src.sap.mcp_client import SapMcpClient
from src.sap.mcp_registry import build_target

LIVE = os.getenv("AGENTESAP_QAS_LIVE_TESTS", "").lower() in {"1","true","yes","on"}
pytestmark = pytest.mark.skipif(not LIVE, reason="set AGENTESAP_QAS_LIVE_TESTS=true to execute the real QAS smoke test")

def _qas_target():
    if os.getenv("AGENTESAP_SAP_RUNTIME_ENABLED", "").lower() not in {"1","true","yes","on"}:
        raise RuntimeError("QAS runtime must be explicitly enabled")
    if os.getenv("AGENTESAP_SAP_RUNTIME_LANDSCAPE", "QAS").upper() != "QAS":
        raise RuntimeError("live smoke is restricted to QAS")
    if os.getenv("AGENTESAP_SAP_RUNTIME_SCOPE", "mcp_readonly") != "mcp_readonly":
        raise RuntimeError("live smoke requires mcp_readonly scope")
    allowed = tuple(x.strip() for x in os.getenv("AGENTESAP_SAP_RUNTIME_READ_TOOLS", "").split(",") if x.strip())
    query_tool = os.getenv("AGENTESAP_SAP_RUNTIME_QUERY_TOOL", "")
    if not allowed:
        raise RuntimeError("live smoke requires an explicit read-tool allowlist")
    if not query_tool or query_tool not in allowed:
        raise RuntimeError("query tool must be explicitly allowlisted")
    return build_target(
        "sap_mcp_server",
        command=os.getenv("AGENTESAP_SAP_MCP_COMMAND", "sap-mcp-server"),
        args=tuple(shlex.split(os.getenv("AGENTESAP_SAP_MCP_ARGS", ""))),
        allowed_tools=allowed,
        metadata={"landscape": "QAS", **({"system": os.environ["AGENTESAP_SAP_RUNTIME_SYSTEM"]} if os.getenv("AGENTESAP_SAP_RUNTIME_SYSTEM") else {})},
    )

async def _catalog_and_read():
    target = _qas_target()
    query_tool = os.environ["AGENTESAP_SAP_RUNTIME_QUERY_TOOL"]
    argument = os.getenv("AGENTESAP_SAP_RUNTIME_QUERY_ARGUMENT", "").strip()
    query = os.getenv("AGENTESAP_QAS_LIVE_QUERY", "MARA")
    async with SapMcpClient(target) as client:
        server = client.server_info()
        descriptors = await client.list_tool_descriptors()
        descriptor = next((x for x in descriptors if x.name == query_tool), None)
        assert descriptor is not None, f"configured QAS tool '{query_tool}' is not advertised"
        assert descriptor.read_only_hint is True
        assert descriptor.destructive_hint is not True
        arguments = {argument: query} if argument else {}
        evidence = await client.call_read_tool(query_tool, arguments)
        return server, descriptor, evidence

def test_real_qas_mcp_catalog_and_read_are_reachable():
    server, descriptor, evidence = asyncio.run(_catalog_and_read())
    assert server is not None and server.name and server.version
    assert descriptor.read_only_hint is True
    assert descriptor.destructive_hint is not True
    assert evidence.provider == "sap_mcp_server"
    assert evidence.landscape == "QAS"
    assert evidence.observation_type == "runtime_observation"
    assert evidence.content

def test_real_qas_evidence_has_runtime_provenance():
    _, _, evidence = asyncio.run(_catalog_and_read())
    assert evidence.landscape == "QAS"
    assert evidence.observation_type == "runtime_observation"
    assert evidence.provider == "sap_mcp_server"
