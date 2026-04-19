"""Meep adapter input model — flat, adapter-specific representation.

This model contains only the fields needed to generate a Meep Python script.
It is NOT a general Meep simulation configuration — it is deliberately minimal,
covering only the nanoparticle_on_film + plane_wave + scattering_spectrum path.
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class MeepInputModel(BaseModel):
    """All parameters needed to render a Meep nanoparticle-on-film script."""

    # --- Particle ---
    particle_material: str = Field(description="e.g. 'Au', 'Ag'")
    particle_shape: str = Field(description="'sphere' or 'cube'")
    particle_radius_um: float = Field(description="Particle radius in μm")

    # --- Film ---
    film_material: str = Field(description="e.g. 'Au', 'Ag'")
    film_thickness_um: float = Field(description="Film thickness in μm")

    # --- Gap ---
    gap_medium_n: float = Field(description="Refractive index of gap dielectric")
    gap_thickness_um: float = Field(description="Gap thickness in μm")

    # --- Source ---
    wavelength_min_um: float = Field(description="Min wavelength in μm")
    wavelength_max_um: float = Field(description="Max wavelength in μm")

    # --- Simulation settings ---
    resolution: int = Field(default=50, description="Pixels per μm")
    pml_thickness_um: float = Field(default=1.0, description="PML thickness in μm")
    freq_points: int = Field(default=200, description="Frequency points for flux")

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
