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


class FakeAnnotations:
    def __init__(self, read_only_hint=None, destructive_hint=None) -> None:
        self.readOnlyHint = read_only_hint
        self.destructiveHint = destructive_hint


class FakeTool:
    def __init__(self, name: str, read_only_hint=None, destructive_hint=None) -> None:
        self.name = name
        self.description = "test tool"
        self.inputSchema = {"type": "object"}
        self.annotations = FakeAnnotations(read_only_hint, destructive_hint)


class FakeToolsResult:
    def __init__(self, tools: list[FakeTool]) -> None:
        self.tools = tools


class FakeClient:
    def __init__(self, tools: list[FakeTool] | None = None) -> None:
        self.calls: list[tuple[str, dict]] = []
        self.tools = tools or [
            FakeTool("search_resources"),
            FakeTool("list_packs"),
            FakeTool("read_table"),
        ]

    async def list_tools(self) -> FakeToolsResult:
        return FakeToolsResult(self.tools)

    async def call_tool(self, tool_name: str, arguments: dict) -> FakeResult:
        self.calls.append((tool_name, arguments))
        return FakeResult(
            [
                FakeTextContent('{"count": 1, "results": [{"title": "SAP Help"}]}'),
            ]
        )


def test_client_accepts_streamable_http_target():
    target = build_target(
        "abap_ai",
        url="https://example.invalid/mcp",
        allowed_tools=("read_object",),
    )

    client = SapMcpClient(target)

    assert client.target.transport == "streamable_http"


def test_sap_devs_default_target_is_usable_by_client():
    target = build_target("sap_devs")
    client = SapMcpClient(target)

    assert target.command == "sap-devs"
    assert target.args == ("mcp", "serve")
    assert target.read_only is True
    assert target.observation_type == "developer_context"
    assert client.target == target


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
    assert dict(evidence.provenance)["transport"] == "stdio"
    assert dict(evidence.provenance)["tool_description"] == "test tool"
    assert dict(evidence.provenance)["tool_input_schema"] == {"type": "object"}
    assert dict(evidence.provenance)["tool_read_only_hint"] is None
    assert dict(evidence.provenance)["tool_destructive_hint"] is None
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



def test_call_read_tool_classifies_runtime_observation_as_partial():
    target = build_target(
        "sap_mcp_server",
        command="sap-mcp-server",
        args=(),
        allowed_tools=("read_table",),
        metadata={"system": "S4QAS", "landscape": "QAS"},
    )
    client = SapMcpClient(target)
    client._client = FakeClient(
        [FakeTool("read_table", read_only_hint=True, destructive_hint=False)]
    )

    evidence = asyncio.run(
        client.call_read_tool("read_table", {"table": "MARA"})
    )

    assert evidence.certainty == "partial"
    assert evidence.observation_type == "runtime_observation"
    assert evidence.system == "S4QAS"
    assert evidence.landscape == "QAS"


def test_call_read_tool_rejects_unadvertised_tool():
    target = build_target(
        "sap_mcp_server",
        command="sap-mcp-server",
        allowed_tools=("missing_tool",),
    )
    client = SapMcpClient(target)
    client._client = FakeClient([FakeTool("other_tool")])

    with pytest.raises(PermissionError, match="not advertised"):
        asyncio.run(client.call_read_tool("missing_tool"))


def test_call_read_tool_rejects_non_read_only_annotation():
    target = build_target(
        "sap_mcp_server",
        command="sap-mcp-server",
        allowed_tools=("unsafe_read",),
    )
    client = SapMcpClient(target)
    client._client = FakeClient(
        [FakeTool("unsafe_read", read_only_hint=False, destructive_hint=True)]
    )

    with pytest.raises(PermissionError, match="not marked read-only"):
        asyncio.run(client.call_read_tool("unsafe_read"))


def test_call_read_tool_accepts_advertised_read_only_tool():
    target = build_target(
        "sap_mcp_server",
        command="sap-mcp-server",
        allowed_tools=("safe_read",),
    )
    client = SapMcpClient(target)
    fake_client = FakeClient(
        [FakeTool("safe_read", read_only_hint=True, destructive_hint=False)]
    )
    client._client = fake_client

    asyncio.run(client.call_read_tool("safe_read", {"table": "MARA"}))

    assert fake_client.calls == [("safe_read", {"table": "MARA"})]



def test_runtime_tool_requires_explicit_readonly_hint():
    target = build_target(
        "sap_mcp_server",
        command="sap-mcp-server",
        allowed_tools=("read_table",),
        metadata={"landscape": "QAS"},
    )
    client = SapMcpClient(target)
    client._client = FakeClient(
        [FakeTool("read_table", read_only_hint=None, destructive_hint=None)]
    )

    with pytest.raises(PermissionError, match="explicit read-only hint"):
        asyncio.run(client.call_read_tool("read_table"))




def test_runtime_evidence_preserves_tool_contract():
    fake_tool = FakeTool(
        "read_table",
        read_only_hint=True,
        destructive_hint=False,
    )
    client = SapMcpClient(
        build_target(
            "sap_mcp_server",
            command="sap-mcp-server",
            args=(),
            allowed_tools=("read_table",),
            metadata={"system": "S4QAS", "landscape": "QAS"},
        )
    )
    client._client = FakeClient([fake_tool])

    evidence = asyncio.run(client.call_read_tool("read_table", {}))

    provenance = dict(evidence.provenance)
    assert provenance["transport"] == "stdio"
    assert provenance["tool_description"] == fake_tool.description
    assert provenance["tool_read_only_hint"] is True
    assert provenance["tool_destructive_hint"] is False
    assert provenance["tool_input_schema"] == fake_tool.inputSchema
