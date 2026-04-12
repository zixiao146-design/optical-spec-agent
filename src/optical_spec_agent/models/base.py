"""Base helpers: StatusField, ValidationStatus, structured sub-models."""

from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, Field

from optical_spec_agent.models.enums import (
    BoundaryType,
    ExcitationSource,
    GeometryType,
    MaterialModel,
    MeshType,
    MonitorType,
    Polarization,
    PostprocessTarget,
    SweepType,
    SymmetryType,
)


# ---------------------------------------------------------------------------
# Provenance wrapper
# ---------------------------------------------------------------------------

class StatusField(BaseModel):
    """A value annotated with its provenance (confirmed / inferred / missing)."""
    value: Any = None
    status: str = "missing"
    note: str = ""


def confirmed(value: Any, note: str = "") -> StatusField:
    return StatusField(value=value, status="confirmed", note=note)


def inferred(value: Any, note: str = "") -> StatusField:
    return StatusField(value=value, status="inferred", note=note)


def missing(note: str = "") -> StatusField:
    return StatusField(note=note)


# ---------------------------------------------------------------------------
# ValidationStatus
# ---------------------------------------------------------------------------

class ValidationStatus(BaseModel):
    """Outcome of validating a full spec."""
    is_executable: bool = False
    errors: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Structured sub-models for geometry_material section
# ---------------------------------------------------------------------------

class GeometryDefinition(BaseModel):
    """Structured description of the geometry."""
    geometry_type: Optional[str] = Field(
        None, description="Shape type: sphere, cube, cylinder, cross, film, waveguide, etc."
    )
    description: str = Field("", description="Free-text description of the geometry")
    dimensions: dict[str, Any] = Field(
        default_factory=dict,
        description="Named dimensions, e.g. {'diameter': '100 nm', 'thickness': '30 nm'}",
    )
    units: str = Field("nm", description="Default length unit")


class MaterialEntry(BaseModel):
    """A single material with its properties."""
    name: str = Field(..., description="Material name, e.g. Au, SiO2")
    role: str = Field("", description="Role in system: particle, substrate, film, medium, etc.")
    model: Optional[str] = Field(None, description="Dispersion model: Drude, Johnson-Christy, etc.")
    refractive_index: Optional[float] = Field(None, description="Constant n (if applicable)")
    notes: str = ""


class MaterialSystem(BaseModel):
    """Collection of materials in the system."""
    materials: list[MaterialEntry] = Field(default_factory=list)
    description: str = ""


class SubstrateOrFilmInfo(BaseModel):
    """Substrate or film details."""
    has_substrate: bool = False
    substrate_material: str = Field("", description="Substrate material name")
    substrate_thickness: str = Field("", description="Substrate thickness with unit")
    has_film: bool = False
    film_material: str = Field("", description="Film material name")
    film_thickness: str = Field("", description="Film thickness with unit")
    notes: str = ""


class ParticleInfo(BaseModel):
    """Nanoparticle / micro-particle details."""
    particle_type: str = Field("", description="Shape: sphere, cube, rod, etc.")
    material: str = Field("", description="Particle material")
    dimensions: dict[str, str] = Field(
        default_factory=dict,
        description="Named dimensions, e.g. {'edge_length': '80 nm'}",
    )
    notes: str = ""


# ---------------------------------------------------------------------------
# Structured sub-models for simulation section
# ---------------------------------------------------------------------------

class SweepPlan(BaseModel):
    """Parameter sweep plan."""
    sweep_type: Optional[str] = Field(None, description="Type: wavelength, parameter, angle, etc.")
    variable: str = Field("", description="Name of the swept variable, e.g. gap_nm, diameter_nm, period_nm")
    range_start: Optional[float] = Field(None, description="Start value")
    range_end: Optional[float] = Field(None, description="End value")
    num_points: Optional[int] = Field(None, description="Number of points")
    step: Optional[float] = Field(None, description="Step size")
    unit: str = Field("nm", description="Unit for start/end/step")
    description: str = ""


class SourceSetting(BaseModel):
    """Excitation source configuration."""
    source_type: Optional[str] = Field(None, description="plane_wave, tfsf, dipole, mode_source, etc.")
    wavelength_range: str = Field("", description="e.g. 400-900 nm")
    polarization: Optional[str] = Field(None, description="Polarization state")
    incident_angle: str = Field("0 deg", description="Incident angle")
    amplitude: Optional[float] = Field(None, description="Source amplitude (if specified)")
    description: str = ""


class BoundaryConditionSetting(BaseModel):
    """Boundary conditions for each direction."""
    x_min: Optional[str] = Field(None, description="Boundary type for x min")
    x_max: Optional[str] = Field(None, description="Boundary type for x max")
    y_min: Optional[str] = Field(None, description="Boundary type for y min")
    y_max: Optional[str] = Field(None, description="Boundary type for y max")
    z_min: Optional[str] = Field(None, description="Boundary type for z min")
    z_max: Optional[str] = Field(None, description="Boundary type for z max")
    description: str = ""


class SymmetrySetting(BaseModel):
    """Symmetry exploit settings."""
    symmetry_type: Optional[str] = Field(None, description="none, mirror_x, mirror_y, etc.")
    description: str = ""


class MeshSetting(BaseModel):
    """Mesh configuration."""
    mesh_type: Optional[str] = Field(None, description="auto, uniform, non_uniform, adaptive")
    global_mesh_accuracy: Optional[int] = Field(None, description="Accuracy level (1-5 for some tools)")
    min_mesh_size: Optional[str] = Field(None, description="Minimum mesh size with unit")
    max_mesh_size: Optional[str] = Field(None, description="Maximum mesh size with unit")
    mesh_override_regions: list[dict[str, Any]] = Field(
        default_factory=list, description="Specific mesh override regions"
    )
    description: str = ""


class StabilitySetting(BaseModel):
    """Numerical stability settings."""
    time_step: Optional[str] = Field(None, description="Time step or Courant factor")
    auto_shutoff: Optional[str] = Field(None, description="Auto shutoff threshold")
    simulation_time: Optional[str] = Field(None, description="Total simulation time")
    description: str = ""


class MonitorSetting(BaseModel):
    """Monitor / sensor placement settings."""
    monitor_type: Optional[str] = Field(None, description="frequency_domain, time_domain, field_profile, etc.")
    locations: list[dict[str, Any]] = Field(
        default_factory=list, description="Monitor placement details"
    )
    frequency_points: Optional[int] = Field(None, description="Number of frequency points")
    description: str = ""


# ---------------------------------------------------------------------------
# Structured sub-models for output section
# ---------------------------------------------------------------------------

class PostprocessTargetSpec(BaseModel):
    """Structured post-processing target."""
    target_type: Optional[str] = Field(None, description="lorentzian_fit, fwhm_extraction, etc.")
    parameters: dict[str, Any] = Field(
        default_factory=dict, description="Target-specific parameters"
    )
    description: str = ""
