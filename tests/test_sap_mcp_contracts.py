import pytest

from src.sap.mcp_contracts import McpTarget, SapMcpEvidence
from src.sap.mcp_registry import build_target, get_provider


def test_sap_devs_profile_is_read_only_and_explicit():
    target = build_target(
        "sap_devs",
        command="sap-devs",
        args=("mcp", "serve"),
    )

    assert target.read_only is True
    assert target.observation_type == "developer_context"
    assert "search_resources" in target.allowed_tools


def test_runtime_provider_requires_explicit_tools():
    with pytest.raises(ValueError, match="allowed_tools"):
        build_target("sap_mcp_server", command="sap-mcp-server")


def test_explicit_empty_allowlist_does_not_fall_back_to_defaults():
    with pytest.raises(ValueError, match="allowed_tools"):
        build_target(
            "sap_devs",
            command="sap-devs",
            args=("mcp", "serve"),
            allowed_tools=(),
        )


def test_abap_provider_requires_an_endpoint():
    with pytest.raises(ValueError, match="streamable_http"):
        build_target("abap_ai")


def test_provider_purpose_is_explicit():
    assert "developer knowledge" in get_provider("sap_devs").purpose


def test_provider_observation_types_are_distinct():
    assert get_provider("sap_devs").observation_type == "developer_context"
    assert (
        get_provider("sap_mcp_server").observation_type
        == "runtime_observation"
    )
    assert (
        get_provider("abap_ai").observation_type
        == "custom_runtime_observation"
    )


def test_evidence_preserves_provider_provenance():
    evidence = SapMcpEvidence(
        provider="sap_devs",
        operation="search_resources",
        content={"count": 1},
        source="SAP Developer knowledge",
        provenance={"source_id": "SAP-DEV-001"},
    )

    metadata = evidence.as_metadata()
    assert metadata["provider"] == "sap_devs"
    assert metadata["source_id"] == "SAP-DEV-001"
    assert metadata["observation_type"] == "external_source"
