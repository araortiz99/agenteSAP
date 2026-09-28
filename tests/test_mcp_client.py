import pytest

from src.sap.mcp_client import SapMcpClient
from src.sap.mcp_registry import build_target


def test_client_rejects_non_stdio_target():
    target = build_target(
        "abap_ai",
        url="https://example.invalid/mcp",
        allowed_tools=("read_object",),
    )

    with pytest.raises(ValueError, match="stdio"):
        SapMcpClient(target)


def test_client_lifecycle_guard_requires_connection():
    target = build_target(
        "sap_devs",
        command="sap-devs",
        args=("mcp", "serve"),
    )
    client = SapMcpClient(target)

    with pytest.raises(RuntimeError, match="not connected"):
        import asyncio
        asyncio.run(client.list_tools())


def test_allowlist_is_explicit():
    target = build_target(
        "sap_devs",
        command="sap-devs",
        args=("mcp", "serve"),
    )

    assert "search_resources" in target.allowed_tools
    assert "update_tutorial_progress" not in target.allowed_tools
