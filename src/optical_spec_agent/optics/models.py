"""Shared models for preview optical design calculators."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class CalculatorSafety(BaseModel):
    external_solver_executed: bool = False
    external_llm_required: bool = False
    proprietary_solver_required: bool = False
    production_grade_validation_claimed: bool = False
    formal_convergence_proof_claimed: bool = False


class CalculatorResult(CalculatorSafety):
    status: str = "ok"
    result: dict[str, Any] = Field(default_factory=dict)
    assumptions: list[str] = Field(default_factory=list)
    diagnostics: list[str] = Field(default_factory=list)
    limitations: list[str] = Field(
        default_factory=lambda: [
            "Preview/design-assist calculation only.",
            "Verify with appropriate validated tools and material data before physical conclusions.",
        ]
    )


class SpectrumSample(BaseModel):
    wavelength_nm: float
    reflectance: float | None = None
    transmittance: float | None = None
    absorptance_estimate: float | None = None


class SweepSample(BaseModel):
    parameter_value: float
    parameter_name: str
    result: dict[str, Any] = Field(default_factory=dict)


class CalculatorSummary(BaseModel):
    title: str
    summary: str
    key_values: dict[str, Any] = Field(default_factory=dict)
    assumptions: list[str] = Field(default_factory=list)
    diagnostics: list[str] = Field(default_factory=list)


class ThinFilmLayer(BaseModel):
    n: float
    thickness_nm: float
    k: float = 0.0


class RayVector(BaseModel):
    height_mm: float
    angle_rad: float
