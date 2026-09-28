from src.investigation.capabilities import (
    ToolCapability,
    discover_capabilities,
    match_capabilities,
    validate_query_arguments,
)
from src.investigation.contracts import InvestigationEntity


def descriptor(
    name="read_stock",
    description="Read material stock by material and plant",
    schema=None,
    read_only=True,
    destructive=False,
):
    return {
        "name": name,
        "description": description,
        "input_schema": schema or {
            "type": "object",
            "properties": {"material": {"type": "string"}, "plant": {"type": "string"}},
            "required": ["material", "plant"],
            "additionalProperties": False,
        },
        "read_only_hint": read_only,
        "destructive_hint": destructive,
    }


def test_discovery_marks_missing_readonly_metadata_invalid():
    class Gateway:
        def inspect_runtime_tools(self):
            return (descriptor(read_only=None),)

    result = discover_capabilities(Gateway())

    assert result[0].availability == "invalid"


def test_discovery_marks_malformed_schema_invalid():
    class Gateway:
        def inspect_runtime_tools(self):
            return (descriptor(schema={"type": "array"}),)

    result = discover_capabilities(Gateway())

    assert result[0].availability == "invalid"


def test_matching_requires_entity_compatibility():
    capabilities = discover_capabilities(
        type(
            "Gateway",
            (),
            {
                "inspect_runtime_tools": lambda self: (
                    descriptor(
                        description="Read stock",
                        schema={
                            "type": "object",
                            "properties": {"material": {"type": "string"}},
                            "required": ["material"],
                        },
                    ),
                )
            },
        )()
    )

    assert match_capabilities(
        ("current_stock",),
        capabilities,
        required_entities=("material", "plant"),
    ) == {}


def test_matching_is_deterministic_when_multiple_tools_are_compatible():
    first = descriptor("z_read_stock", "Read stock material plant")
    second = descriptor("a_read_stock", "Read stock material plant")

    class Gateway:
        def inspect_runtime_tools(self):
            return (first, second)

    capabilities = discover_capabilities(Gateway())
    selected = match_capabilities(("current_stock",), capabilities)

    assert selected["current_stock"].name == "a_read_stock"


def test_query_validation_rejects_missing_required_parameters():
    capability = discover_capabilities(
        type("Gateway", (), {"inspect_runtime_tools": lambda self: (descriptor(),)})()
    )[0]

    valid, reason = validate_query_arguments(
        capability,
        {"material": "100123"},
    )

    assert not valid
    assert "missing required parameters" in reason


def test_query_validation_rejects_unknown_parameters_when_schema_forbids_them():
    capability = discover_capabilities(
        type("Gateway", (), {"inspect_runtime_tools": lambda self: (descriptor(),)})()
    )[0]

    valid, reason = validate_query_arguments(
        capability,
        {"material": "100123", "plant": "5023", "unsafe": "x"},
    )

    assert not valid
    assert "unknown parameters" in reason


def test_query_validation_rejects_wrong_types_and_enum_values():
    cap = discover_capabilities(
        type(
            "Gateway",
            (),
            {
                "inspect_runtime_tools": lambda self: (
                    descriptor(
                        schema={
                            "type": "object",
                            "properties": {
                                "material": {"type": "string"},
                                "plant": {"type": "integer", "enum": [5023, 6208]},
                            },
                            "required": ["material", "plant"],
                        }
                    ),
                )
            },
        )()
    )[0]

    valid, reason = validate_query_arguments(
        cap,
        {"material": "100123", "plant": "5023"},
    )
    assert not valid
    assert "invalid type" in reason

    valid, reason = validate_query_arguments(
        cap,
        {"material": "100123", "plant": 9999},
    )
    assert not valid
    assert "outside enum" in reason


def test_query_validation_rejects_entity_mismatch():
    capability = discover_capabilities(
        type("Gateway", (), {"inspect_runtime_tools": lambda self: (descriptor(),)})()
    )[0]

    valid, reason = validate_query_arguments(
        capability,
        {"material": "999999", "plant": "5023"},
        (
            InvestigationEntity("material", "100123"),
            InvestigationEntity("plant", "5023"),
        ),
    )

    assert not valid
    assert "does not match resolved entity" in reason


def test_query_validation_accepts_matching_arguments():
    capability = discover_capabilities(
        type("Gateway", (), {"inspect_runtime_tools": lambda self: (descriptor(),)})()
    )[0]

    valid, reason = validate_query_arguments(
        capability,
        {"material": "100123", "plant": "5023"},
        (
            InvestigationEntity("material", "100123"),
            InvestigationEntity("plant", "5023"),
        ),
    )

    assert valid
    assert reason == ""
