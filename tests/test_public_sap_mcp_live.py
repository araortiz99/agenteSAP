"""Optional live smoke test for SAP Developer Center hosted MCP.

Disabled by default so CI does not depend on the public service.
Enable with AGENTESAP_SAP_PUBLIC_MCP_LIVE_TESTS=true.
"""

import asyncio
import os

import pytest

from src.sap.mcp_client import SapMcpClient
from src.sap.mcp_registry import build_target

LIVE = os.getenv("AGENTESAP_SAP_PUBLIC_MCP_LIVE_TESTS", "").lower() in {
    "1", "true", "yes", "on"
}

pytestmark = pytest.mark.skipif(
    not LIVE,
    reason="set AGENTESAP_SAP_PUBLIC_MCP_LIVE_TESTS=true to run the live public SAP MCP smoke test",
)


async def _run_live() -> tuple[object, tuple[str, ...], object]:
    target = build_target(
        "sap_developer_public",
        url=os.getenv(
            "AGENTESAP_SAP_PUBLIC_MCP_URL",
            "https://developers.sap.com/mcp/search",
        ),
        allowed_tools=(
            "search_tutorials",
            "get_tutorial",
            "list_missions",
            "get_mission",
        ),
    )
    async with SapMcpClient(target) as client:
        server = client.server_info()
        tools = await client.list_tools()
        evidence = await client.call_read_tool(
            "search_tutorials",
            {"query": "SAP MM material master", "limit": 3},
        )
        return server, tools, evidence


def test_public_sap_mcp_live_read_only_smoke():
    server, tools, evidence = asyncio.run(_run_live())

    assert server is not None
    assert server.name
    assert server.version
    assert "search_tutorials" in tools
    assert evidence.provider == "sap_developer_public"
    assert evidence.operation == "search_tutorials"
    assert evidence.observation_type == "external_source"
    assert evidence.certainty == "external_source"
    assert evidence.provenance["transport"] == "streamable_http"
    assert evidence.provenance["tool_read_only_hint"] is True
    assert evidence.provenance["tool_destructive_hint"] is False
    assert evidence.content
