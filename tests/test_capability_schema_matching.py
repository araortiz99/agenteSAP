from src.investigation.capabilities import ToolCapability, match_capabilities, validate_query_arguments


def cap(name, operation, properties, required, entities=("material", "plant")):
    schema = {"type": "object", "properties": properties, "required": required}
    return ToolCapability(name, name, schema, True, False, entities, (operation,), "available")


def test_matching_prefers_schema_that_covers_required_entities():
    weak = cap(
        "read_stock_generic",
        "read_stock",
        {"material": {"type": "string"}},
        ["material"],
        ("material",),
    )
    strong = cap(
        "read_stock_material_plant",
        "read_stock",
        {"material": {"type": "string"}, "plant": {"type": "string"}},
        ["material", "plant"],
    )
    selected = match_capabilities(
        ("current_stock",),
        (weak, strong),
        required_entities=("material", "plant"),
    )
    assert selected["current_stock"].name == "read_stock_material_plant"


def test_query_schema_constraints_are_enforced_without_invocation():
    capability = cap(
        "read_stock",
        "read_stock",
        {
            "material": {"type": "string", "pattern": r"^\d{6}$"},
            "plant": {"type": "string", "minLength": 4, "maxLength": 4},
        },
        ["material", "plant"],
    )
    ok, reason = validate_query_arguments(
        capability,
        {"material": "100123", "plant": "5023"},
    )
    assert ok and reason == ""

    ok, reason = validate_query_arguments(
        capability,
        {"material": "123", "plant": "5023"},
    )
    assert not ok
    assert "pattern" in reason


def test_query_schema_rejects_numeric_bounds():
    capability = cap(
        "read_stock",
        "read_stock",
        {"plant": {"type": "integer", "minimum": 1000, "maximum": 9999}},
        ["plant"],
        ("plant",),
    )
    ok, reason = validate_query_arguments(capability, {"plant": 999})
    assert not ok
    assert "minimum" in reason
