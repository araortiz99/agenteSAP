"""MCP capability discovery and deterministic matching."""

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
    return {token for token in text.lower().replace("_", " ").replace("-", " ").split() if token}


def _infer_capability(descriptor: dict[str, Any]) -> ToolCapability:
    name = str(descriptor.get("name", ""))
    description = str(descriptor.get("description", ""))
    tokens = _tokens(name + " " + description)
    entity_map = {
        "material": {"material", "matnr"},
        "plant": {"plant", "center", "centro", "werks"},
        "storage_location": {"storage", "storage_location", "almacen", "almacén", "lgort"},
        "movement": {"movement", "movimiento", "mseg", "materialdocument"},
        "material_document": {"material", "document", "documento", "mseg"},
        "stock": {"stock", "inventory", "inventario", "mard", "labst"},
    }
    supported_entities = tuple(
        entity for entity, markers in entity_map.items()
        if tokens.intersection(markers)
    )
    operations = tuple(
        operation for operation, markers in {
            "read_stock": {"stock", "inventory", "inventario", "mard", "labst"},
            "read_movements": {"movement", "movimiento", "mseg", "materialdocument"},
            "read_master": {"material", "matnr", "master", "maestro", "plant", "werks"},
        }.items()
        if tokens.intersection(markers)
    )
    return ToolCapability(
        name=name,
        description=description,
        input_schema=descriptor.get("input_schema", {}),
        read_only=descriptor.get("read_only_hint"),
        destructive=descriptor.get("destructive_hint"),
        supported_entities=supported_entities,
        supported_operations=operations,
        availability="available",
    )


def discover_capabilities(gateway) -> tuple[ToolCapability, ...]:
    """Use only tools/list metadata; never invoke a SAP tool."""
    descriptors = gateway.inspect_runtime_tools()
    return tuple(_infer_capability(item) for item in descriptors)


def match_capabilities(
    required_evidence: tuple[str, ...],
    capabilities: tuple[ToolCapability, ...],
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
            capability for capability in capabilities
            if capability.read_only is True
            and capability.destructive is not True
            and (
                evidence_type in aliases
                and set(aliases[evidence_type]).intersection(capability.supported_operations)
            )
        ]
        if candidates:
            selected[evidence_type] = sorted(candidates, key=lambda item: item.name)[0]
    return selected
