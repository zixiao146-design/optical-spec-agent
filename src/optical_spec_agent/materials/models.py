"""Models for the local preview material catalog."""

from __future__ import annotations

from pydantic import BaseModel, Field


class RefractiveIndexModel(BaseModel):
    """Preview refractive-index model.

    Values in this starter catalog are approximate design-assist hints unless a
    material entry explicitly documents stronger provenance. They are not a
    production-grade optical-constants database.
    """

    kind: str = Field("placeholder", description="constant, placeholder, or tabulated_preview")
    n: float | None = None
    k: float | None = None
    wavelength_nm: float | None = None


class MaterialSummary(BaseModel):
    material_id: str
    display_name: str
    aliases: list[str] = Field(default_factory=list)
    category: str
    common_use: list[str] = Field(default_factory=list)
    optical_role: str
    production_grade: bool = False
    validation_level: str = "preview"
    source_note: str


class MaterialDetail(MaterialSummary):
    wavelength_range_nm: tuple[float, float] | None = None
    refractive_index_model: RefractiveIndexModel
    notes: list[str] = Field(default_factory=list)
