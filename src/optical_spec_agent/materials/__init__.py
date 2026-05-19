"""Local preview material catalog for optical design assistance."""

from .catalog import (
    diagnose_material_suitability,
    get_material,
    list_materials,
    search_materials,
    suggest_materials_for_application,
)
from .models import (
    MaterialDetail,
    MaterialSuitabilityDiagnostic,
    MaterialSummary,
    RefractiveIndexModel,
)

__all__ = [
    "MaterialDetail",
    "MaterialSuitabilityDiagnostic",
    "MaterialSummary",
    "RefractiveIndexModel",
    "diagnose_material_suitability",
    "get_material",
    "list_materials",
    "search_materials",
    "suggest_materials_for_application",
]
