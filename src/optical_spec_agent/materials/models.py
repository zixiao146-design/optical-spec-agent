"""Models for the local preview material catalog."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


ProvenanceType = Literal[
    "curated_preview",
    "placeholder",
    "approximate_constant",
    "user_must_verify",
]


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
    provenance_type: ProvenanceType = "approximate_constant"
    source_note: str
    citation_note: str | None = None
    wavelength_validity_note: str = (
        "Approximate local preview only; verify wavelength-dependent data before physical conclusions."
    )
    known_limitations: list[str] = Field(
        default_factory=lambda: [
            "Starter catalog entry for preview/design-assist workflows.",
            "Not a production-grade optical constants database entry.",
        ]
    )
    suitable_for: list[str] = Field(default_factory=list)
    not_suitable_for: list[str] = Field(default_factory=list)
    requires_user_verification: bool = True
    production_grade_optical_constants: bool = False


class MaterialDetail(MaterialSummary):
    wavelength_range_nm: tuple[float, float] | None = None
    refractive_index_model: RefractiveIndexModel
    notes: list[str] = Field(default_factory=list)


class MaterialSuitabilityDiagnostic(BaseModel):
    material_id: str
    application: str
    suitable: bool | None = None
    suitability: Literal["suitable", "not_suitable", "unknown"] = "unknown"
    rationale: str
    warnings: list[str] = Field(default_factory=list)
    missing_context: list[str] = Field(default_factory=list)
    recommended_verification: list[str] = Field(default_factory=list)
    provenance_type: ProvenanceType = "approximate_constant"
    requires_user_verification: bool = True
    production_grade_optical_constants: bool = False
    external_solver_executed: bool = False
    external_llm_required: bool = False
    production_grade_validation_claimed: bool = False
    formal_convergence_proof_claimed: bool = False
