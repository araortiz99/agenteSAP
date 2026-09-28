import pytest

from src.sap.mcp_client import SapMcpClient
from src.sap.mcp_contracts import McpTarget


def test_streamable_http_target_is_supported():
    target = McpTarget(
        provider="sap_developer_public",
        transport="streamable_http",
        url="https://developers.sap.com/mcp/search",
        allowed_tools=("search_tutorials",),
        observation_type="external_source",
    )
    client = SapMcpClient(target)
    assert client.target.transport == "streamable_http"


def test_stdio_target_remains_supported():
    target = McpTarget(
        provider="sap_devs",
        transport="stdio",
        command="sap-devs",
        args=("mcp", "serve"),
        allowed_tools=("search_resources",),
        observation_type="developer_context",
    )
    client = SapMcpClient(target)
    assert client.target.transport == "stdio"
