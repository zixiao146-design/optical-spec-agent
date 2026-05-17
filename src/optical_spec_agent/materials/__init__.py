"""Local preview material catalog for optical design assistance."""

from .catalog import (
    get_material,
    list_materials,
    search_materials,
    suggest_materials_for_application,
)
from .models import MaterialDetail, MaterialSummary, RefractiveIndexModel

__all__ = [
    "MaterialDetail",
    "MaterialSummary",
    "RefractiveIndexModel",
    "get_material",
    "list_materials",
    "search_materials",
    "suggest_materials_for_application",
]
