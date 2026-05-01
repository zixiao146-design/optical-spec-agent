"""Meep adapter input model — flat, adapter-specific representation.

This model contains only the fields needed to generate a Meep Python script.
It is NOT a general Meep simulation configuration — it is deliberately minimal,
covering only the nanoparticle_on_film + plane_wave + scattering_spectrum path.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class MeepInputModel(BaseModel):
    """All parameters needed to render a Meep nanoparticle-on-film script."""

    script_mode: Literal["preview", "research_preview", "smoke"] = Field(
        default="preview",
        description="Script generation mode: preview, research_preview, or smoke",
    )

    # --- Particle ---
    particle_material: str = Field(description="e.g. 'Au', 'Ag'")
    particle_shape: str = Field(description="'sphere' or 'cube'")
    particle_radius_um: float = Field(description="Particle radius in μm")

    # --- Film ---
    film_material: str = Field(description="e.g. 'Au', 'Ag'")
    film_thickness_um: float = Field(description="Film thickness in μm")

    # --- Gap ---
    gap_medium_name: str = Field(description="e.g. 'SiO2', 'Al2O3', 'Air'")
    gap_medium_n: float = Field(description="Refractive index of gap dielectric")
    gap_thickness_um: float = Field(description="Gap thickness in μm")

    # --- Source ---
    wavelength_min_um: float = Field(description="Min wavelength in μm")
    wavelength_max_um: float = Field(description="Max wavelength in μm")

    # --- Simulation settings ---
    resolution: int = Field(default=50, description="Pixels per μm")
    pml_thickness_um: float = Field(default=1.0, description="PML thickness in μm")
    freq_points: int = Field(default=200, description="Frequency points for flux")

    # --- Research-preview stability diagnostics ---
    boundary_type: Literal["pml", "absorber"] = Field(
        default="pml",
        description="Research-preview boundary layer type: pml or absorber",
    )
    courant: float | None = Field(
        default=None,
        description="Optional Meep Courant factor for research-preview runs",
    )
    eps_averaging: bool | None = Field(
        default=None,
        description="Optional Meep eps_averaging override for research-preview runs",
    )
    material_mode: Literal[
        "library",
        "dielectric_sanity",
        "particle_library_film_dielectric",
        "particle_dielectric_film_library",
    ] = Field(
        default="library",
        description="Research-preview material mode for stability diagnostics",
    )
    diagnostic_profile: Literal["normal", "low_cost", "physical_probe"] = Field(
        default="normal",
        description="Research-preview diagnostic profile: normal, low_cost, or physical_probe",
    )
    source_component: Literal["Ex", "Ey", "Ez"] = Field(
        default="Ez",
        description="Research-preview source field component. Ez preserves legacy behavior.",
    )
    stop_strategy: Literal["decay", "fixed"] | None = Field(
        default=None,
        description="Research-preview run stopping strategy override",
    )
    fixed_run_time: float | None = Field(
        default=None,
        description="Fixed run time for fixed stop strategy",
    )
    decay_threshold: float | None = Field(
        default=None,
        description="Decay threshold for decay stop strategy",
    )
    flux_mode: Literal[
        "closed_box",
        "gap_clearance_box",
        "upper_hemibox",
        "single_plane",
        "top_plane",
    ] = Field(
        default="closed_box",
        description="Research-preview flux/monitor preset. Non-closed modes are diagnostic only.",
    )

    # --- Sweep (optional) ---
    sweep_variable: str | None = Field(default=None, description="e.g. 'gap_thickness_um'")
    sweep_start_um: float | None = Field(default=None)
    sweep_end_um: float | None = Field(default=None)
    sweep_steps: int | None = Field(default=None)

    # --- Post-processing (optional) ---
    postprocess: list[str] = Field(
        default_factory=list,
        description="e.g. ['resonance_wavelength', 'fwhm_extraction']",
    )

    # --- Smoke test mode ---
    smoke: bool = Field(
        default=False,
        description="If True, generate a minimal script for smoke validation: "
                    "ultra-low resolution, few steps, no plotting, no sweep. "
                    "NOT for production use.",
    )

    # --- Translation metadata ---
    defaults_applied: list[str] = Field(
        default_factory=list,
        description="Human-readable list of fields where adapter applied default values, "
                    "e.g. ['gap_medium: SiO2 (n=1.45)', 'wavelength_range: 400–900 nm']",
    )
