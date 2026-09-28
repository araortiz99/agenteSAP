"""Optional live smoke test for the installed sap-devs MCP server.

This test is disabled by default so CI remains independent of local SAP tooling.
Enable it locally with AGENTESAP_MCP_LIVE_TESTS=true.
"""

import asyncio
import json
import os

import pytest

from src.sap.mcp_client import SapMcpClient
from src.sap.mcp_registry import build_target


LIVE = os.getenv("AGENTESAP_MCP_LIVE_TESTS", "").lower() in {
    "1",
    "true",
    "yes",
    "on",
}

pytestmark = pytest.mark.skipif(
    not LIVE,
    reason="set AGENTESAP_MCP_LIVE_TESTS=true to run the live sap-devs MCP smoke test",
)


async def _run_live_smoke() -> tuple[object, tuple[str, ...]]:
    target = build_target("sap_devs")
    async with SapMcpClient(target) as client:
        server = client.server_info()
        tools = await client.list_tools()
        return server, tools


def test_sap_devs_live_server_is_reachable():
    server, tools = asyncio.run(_run_live_smoke())

    assert server is not None
    assert server.name == "sap-devs"
    assert server.version
    assert "search_resources" in tools
    assert "update_tutorial_progress" in tools


async def _search_live() -> object:
    target = build_target("sap_devs")
    async with SapMcpClient(target) as client:
        return await client.call_read_tool(
            "search_resources",
            {"query": "ABAP", "limit": 3},
        )


def test_sap_devs_live_search_preserves_external_classification():
    evidence = asyncio.run(_search_live())

    assert evidence.provider == "sap_devs"
    assert evidence.operation == "search_resources"
    assert evidence.observation_type == "developer_context"
    assert evidence.certainty == "external_source"
    assert evidence.content

    first = evidence.content[0]
    if isinstance(first, str):
        payload = json.loads(first)
        assert isinstance(payload, dict)
        assert "results" in payload
