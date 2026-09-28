import asyncio

import pytest

from src.sap.mcp_client import SapMcpClient
from src.sap.mcp_registry import build_target


class FakeTextContent:
    def __init__(self, text: str) -> None:
        self.text = text


class FakeResult:
    def __init__(self, content: list[object]) -> None:
        self.content = content


class FakeClient:
    def __init__(self) -> None:
        self.calls: list[tuple[str, dict]] = []

    async def call_tool(self, tool_name: str, arguments: dict) -> FakeResult:
        self.calls.append((tool_name, arguments))
        return FakeResult(
            [
                FakeTextContent('{"count": 1, "results": [{"title": "SAP Help"}]}'),
            ]
        )


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
        asyncio.run(client.list_tools())


def test_allowlist_is_explicit():
    target = build_target(
        "sap_devs",
        command="sap-devs",
        args=("mcp", "serve"),
    )

    assert "search_resources" in target.allowed_tools
    assert "update_tutorial_progress" not in target.allowed_tools


def test_call_read_tool_rejects_non_allowlisted_tool():
    target = build_target(
        "sap_devs",
        command="sap-devs",
        args=("mcp", "serve"),
        allowed_tools=("search_resources",),
    )
    client = SapMcpClient(target)
    client._client = FakeClient()

    with pytest.raises(PermissionError, match="not allowed"):
        asyncio.run(
            client.call_read_tool(
                "update_tutorial_progress",
                {"tutorial_id": "example"},
            )
        )


def test_call_read_tool_normalizes_result_and_preserves_provenance():
    target = build_target(
        "sap_devs",
        command="sap-devs",
        args=("mcp", "serve"),
        allowed_tools=("search_resources",),
        metadata={"system": "sap-devs-local", "landscape": "local"},
    )
    client = SapMcpClient(target)
    fake_client = FakeClient()
    client._client = fake_client

    evidence = asyncio.run(
        client.call_read_tool(
            "search_resources",
            {"query": "Fiori", "limit": 5},
        )
    )

    assert fake_client.calls == [
        ("search_resources", {"query": "Fiori", "limit": 5})
    ]
    assert evidence.provider == "sap_devs"
    assert evidence.operation == "search_resources"
    assert evidence.source == "MCP provider: sap_devs"
    assert evidence.certainty == "external_source"
    assert evidence.observation_type == "developer_context"
    assert evidence.system == "sap-devs-local"
    assert evidence.landscape == "local"
    assert evidence.provenance == {"transport": "stdio"}
    assert evidence.content == [
        '{"count": 1, "results": [{"title": "SAP Help"}]}'
    ]


def test_call_read_tool_uses_empty_arguments_when_omitted():
    target = build_target(
        "sap_devs",
        command="sap-devs",
        args=("mcp", "serve"),
        allowed_tools=("list_packs",),
    )
    client = SapMcpClient(target)
    fake_client = FakeClient()
    client._client = fake_client

    asyncio.run(client.call_read_tool("list_packs"))

    assert fake_client.calls == [("list_packs", {})]
