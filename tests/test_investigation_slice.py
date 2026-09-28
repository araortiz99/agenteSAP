from datetime import date

from src.investigation.capabilities import ToolCapability, match_capabilities
from src.investigation.case_id import build_case_id
from src.investigation.entities import extract_entities, missing_required_entities
from src.investigation.engine import investigate, render_investigation
from src.investigation.planner import create_plan


def test_extracts_material_and_plant():
    entities = extract_entities("¿Por qué el material 100123 tiene stock diferente en el centro 5023?")
    assert [(x.entity_type, x.value) for x in entities] == [
        ("material", "100123"),
        ("plant", "5023"),
    ]
    assert not missing_required_entities(entities)


def test_missing_material_is_explicit():
    entities = extract_entities("¿Por qué el stock del centro 5023 es diferente?")
    assert "material" in missing_required_entities(entities)


def test_planner_is_deterministic_and_bounded():
    plan = create_plan("¿Por qué el material 100123 difiere en centro 5023?", extract_entities("material 100123 centro 5023"))
    assert plan.intent == "stock_discrepancy"
    assert plan.required_evidence[:3] == ("material_master", "plant_data", "current_stock")
    assert len(plan.steps) == 5
    assert "max_steps_reached" in plan.stop_conditions


def test_capability_match_rejects_write_or_unreadable_tools():
    capabilities = (
        ToolCapability("write_stock", "update stock", {}, False, True, ("stock",), ("read_stock",), "available"),
        ToolCapability("read_stock", "read stock", {}, True, False, ("stock",), ("read_stock",), "available"),
    )
    selected = match_capabilities(("current_stock",), capabilities)
    assert selected["current_stock"].name == "read_stock"


def test_case_id_is_compact_and_stable():
    first = build_case_id("material 100123 centro 5023", day=date(2026, 9, 28))
    second = build_case_id("material 100123 centro 5023", day=date(2026, 9, 28))
    assert first == second
    assert len(first) <= 18
    assert first.startswith("INV-20260928-")


class FakeClient:
    def get_tree(self, ref="main"):
        return []

    def get_file(self, path, ref="main"):
        raise AssertionError("no file should be read in this fake")


class FakeGateway:
    def validate_runtime_allowlist(self):
        return tuple({"name": name, "valid": True} for name in (
            "read_master", "read_stock", "read_movements",
        ))

    def inspect_runtime_tools(self):
        return (
            {
                "name": "read_master",
                "description": "Read material master and plant data",
                "input_schema": {"properties": {"material": {}, "plant": {}}, "required": ["material", "plant"]},
                "read_only_hint": True,
                "destructive_hint": False,
            },
            {
                "name": "read_stock",
                "description": "Read material stock by material and plant",
                "input_schema": {"properties": {"material": {}, "plant": {}}, "required": ["material", "plant"]},
                "read_only_hint": True,
                "destructive_hint": False,
            },
            {
                "name": "read_movements",
                "description": "Read material movements and material documents by material and plant",
                "input_schema": {"properties": {"material": {}, "plant": {}}, "required": ["material", "plant"]},
                "read_only_hint": True,
                "destructive_hint": False,
            },
        )

    def read_runtime(self, tool_name, arguments):
        assert tool_name in {"read_master", "read_stock", "read_movements"}
        assert arguments == {"material": "100123", "plant": "5023"}
        from src.sap.mcp_contracts import SapMcpEvidence
        return SapMcpEvidence(
            provider="sap_mcp_server",
            operation=tool_name,
            content={"material": "100123", "plant": "5023", "stock": 125},
            source="QAS",
            system="QAS",
            landscape="QAS",
            object_id="100123",
            certainty="partial",
            observation_type="runtime_observation",
            provenance={"query": "material/plant"},
        )


def test_investigation_runs_end_to_end_with_fake_qas():
    result = investigate(
        FakeClient(),
        "¿Por qué el material 100123 tiene stock diferente al esperado en el centro 5023?",
        mcp_gateway=FakeGateway(),
        day=date(2026, 9, 28),
    )
    assert result.case_id.startswith("INV-20260928-")
    assert result.intent == "stock_discrepancy"
    assert {x.entity_type for x in result.entities} == {"material", "plant"}
    assert any(x.landscape == "QAS" for x in result.evidence_collected)
    assert result.stop_reason == "evidence_sufficient"
    rendered = render_investigation(result)
    assert "Confidence:" in rendered
    assert "Provenance:" in rendered


def test_investigation_stops_on_missing_critical_entity():
    result = investigate(
        FakeClient(),
        "¿Por qué el stock del centro 5023 es diferente?",
        mcp_gateway=FakeGateway(),
        day=date(2026, 9, 28),
    )
    assert result.stop_reason == "missing_entity"
    assert "critical_entity:material" in result.evidence_missing


def test_non_readonly_capability_is_not_selected():
    capabilities = (
        ToolCapability("query", "read stock", {}, None, False, ("stock",), ("read_stock",), "available"),
    )
    assert match_capabilities(("current_stock",), capabilities) == {}
