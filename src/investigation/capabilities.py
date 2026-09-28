"""MCP capability discovery, safe matching and query validation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ToolCapability:
    name: str
    description: str
    input_schema: object
    read_only: bool | None
    destructive: bool | None
    supported_entities: tuple[str, ...]
    supported_operations: tuple[str, ...]
    availability: str


def _tokens(text: str) -> set[str]:
    return {
        token
        for token in text.lower().replace("_", " ").replace("-", " ").split()
        if token
    }


def _valid_schema(schema: object) -> bool:
    if not isinstance(schema, dict):
        return False
    if schema.get("type", "object") != "object":
        return False
    properties = schema.get("properties", {})
    required = schema.get("required", [])
    if not isinstance(properties, dict) or not isinstance(required, list):
        return False
    if not all(isinstance(item, str) for item in required):
        return False
    return all(item in properties for item in required)


def _infer_capability(descriptor: dict[str, Any]) -> ToolCapability:
    name = str(descriptor.get("name", ""))
    description = str(descriptor.get("description", ""))
    schema = descriptor.get("input_schema", {})
    tokens = _tokens(name + " " + description)
    entity_map = {
        "material": {"material", "matnr"},
        "plant": {"plant", "center", "centro", "werks"},
        "storage_location": {"storage", "storage_location", "almacen", "almacén", "lgort"},
        "movement_type": {"movement", "movimiento", "bwart"},
        "material_document": {"material", "document", "documento", "mseg", "materialdocument"},
        "stock": {"stock", "inventory", "inventario", "mard", "labst"},
    }
    supported_entities = tuple(
        entity for entity, markers in entity_map.items()
        if tokens.intersection(markers)
    )
    operations = tuple(
        operation
        for operation, markers in {
            "read_stock": {"stock", "inventory", "inventario", "mard", "labst"},
            "read_movements": {
                "movement", "movements", "movimiento", "movimientos",
                "mseg", "materialdocument", "documents",
            },
            "read_master": {"material", "matnr", "master", "maestro", "plant", "werks"},
        }.items()
        if tokens.intersection(markers)
    )
    metadata_valid = (
        bool(name)
        and descriptor.get("read_only_hint") is True
        and descriptor.get("destructive_hint") is not True
        and _valid_schema(schema)
    )
    return ToolCapability(
        name=name,
        description=description,
        input_schema=schema,
        read_only=descriptor.get("read_only_hint"),
        destructive=descriptor.get("destructive_hint"),
        supported_entities=supported_entities,
        supported_operations=operations,
        availability="available" if metadata_valid else "invalid",
    )


def discover_capabilities(gateway) -> tuple[ToolCapability, ...]:
    """Use only tools/list metadata; never invoke a SAP tool."""
    descriptors = gateway.inspect_runtime_tools()
    return tuple(_infer_capability(item) for item in descriptors)


def match_capabilities(
    required_evidence: tuple[str, ...],
    capabilities: tuple[ToolCapability, ...],
    required_entities: tuple[str, ...] = ("material", "plant"),
) -> dict[str, ToolCapability]:
    selected: dict[str, ToolCapability] = {}
    aliases = {
        "material_master": {"read_master"},
        "plant_data": {"read_master"},
        "current_stock": {"read_stock"},
        "relevant_movements": {"read_movements"},
        "material_documents": {"read_movements"},
    }
    for evidence_type in required_evidence:
        candidates = [
            capability
            for capability in capabilities
            if capability.availability == "available"
            and capability.read_only is True
            and capability.destructive is not True
            and set(aliases.get(evidence_type, ())).intersection(
                capability.supported_operations
            )
            and set(required_entities).issubset(capability.supported_entities)
        ]
        if candidates:
            selected[evidence_type] = sorted(
                candidates,
                key=lambda item: item.name,
            )[0]
    return selected


def validate_query_arguments(
    capability: ToolCapability,
    arguments: dict[str, object],
    entities: tuple[Any, ...] = (),
) -> tuple[bool, str]:
    """Validate generated tool arguments without invoking the capability."""
    if capability.availability != "available":
        return False, "capability metadata is invalid"
    schema = capability.input_schema
    if not _valid_schema(schema):
        return False, "input schema is invalid"

    properties = schema.get("properties", {})
    required = schema.get("required", [])
    additional_properties = schema.get("additionalProperties", True)

    missing = [key for key in required if key not in arguments]
    if missing:
        return False, "missing required parameters: " + ", ".join(sorted(missing))

    unknown = [key for key in arguments if key not in properties]
    if unknown and additional_properties is False:
        return False, "unknown parameters: " + ", ".join(sorted(unknown))

    entity_values = {getattr(item, "entity_type", None): getattr(item, "value", None) for item in entities}
    argument_entity_aliases = {
        "material": "material",
        "matnr": "material",
        "material_number": "material",
        "plant": "plant",
        "center": "plant",
        "centro": "plant",
        "werks": "plant",
        "storage_location": "storage_location",
        "storage": "storage_location",
        "almacen": "storage_location",
        "lgort": "storage_location",
        "movement_type": "movement_type",
        "movement": "movement_type",
        "bwart": "movement_type",
        "material_document": "material_document",
        "material_doc": "material_document",
        "mblnr": "material_document",
    }

    for key, value in arguments.items():
        definition = properties.get(key)
        if not isinstance(definition, dict):
            return False, f"parameter schema is invalid: {key}"
        expected = definition.get("type")
        if expected and not _matches_type(value, expected):
            return False, f"parameter '{key}' has invalid type"
        enum = definition.get("enum")
        if enum is not None and value not in enum:
            return False, f"parameter '{key}' has a value outside enum"
        entity_type = argument_entity_aliases.get(key)
        if entity_type in entity_values and value != entity_values[entity_type]:
            return False, f"parameter '{key}' does not match resolved entity"

    return True, ""


def _matches_type(value: object, expected: object) -> bool:
    if isinstance(expected, list):
        return any(_matches_type(value, item) for item in expected)
    if expected == "string":
        return isinstance(value, str)
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if expected == "boolean":
        return isinstance(value, bool)
    if expected == "object":
        return isinstance(value, dict)
    if expected == "array":
        return isinstance(value, list)
    if expected == "null":
        return value is None
    return False
