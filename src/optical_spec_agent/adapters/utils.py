"""Shared helpers for lightweight solver adapters."""

from __future__ import annotations

from typing import Any

from optical_spec_agent.models.base import StatusField
from optical_spec_agent.models.spec import OpticalSpec


def get_status_value(spec: OpticalSpec, dotted_path: str) -> Any:
    """Read a StatusField value by dotted path, returning None if missing."""
    section_name, _, field_name = dotted_path.partition(".")
    if not section_name or not field_name:
        return None

    section = getattr(spec, section_name, None)
    if section is None:
        return None

    field = getattr(section, field_name, None)
    if isinstance(field, StatusField):
        if field.status == "missing":
            return None
        return field.value
    return field


def as_lower(value: Any) -> str:
    """Normalize arbitrary spec values for routing comparisons."""
    return str(value or "").strip().lower().replace("-", "_")


def list_material_names(spec: OpticalSpec) -> list[str]:
    """Return material names from geometry_material.material_system when present."""
    material_system = get_status_value(spec, "geometry_material.material_system")
    materials = getattr(material_system, "materials", None)
    if not materials:
        return []
    names: list[str] = []
    for material in materials:
        name = getattr(material, "name", None)
        if name:
            names.append(str(name))
    return names
