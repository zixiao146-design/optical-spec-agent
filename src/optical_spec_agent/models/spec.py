"""Top-level spec model — all sections with structured sub-models."""

from __future__ import annotations

import json
from typing import Any, Optional

from pydantic import BaseModel, Field

from optical_spec_agent.models.base import (
    BoundaryConditionSetting,
    GeometryDefinition,
    MaterialSystem,
    MeshSetting,
    MonitorSetting,
    ParticleInfo,
    PostprocessTargetSpec,
    SourceSetting,
    StabilitySetting,
    StatusField,
    SubstrateOrFilmInfo,
    SweepPlan,
    SymmetrySetting,
    ValidationStatus,
    confirmed,
    inferred,
    missing,
)


# ---------------------------------------------------------------------------
# Section models
# ---------------------------------------------------------------------------

class TaskSection(BaseModel):
    """Task metadata."""
    task_id: str = Field("", description="Unique task identifier (auto-generated if empty)")
    task_name: StatusField = Field(
        default_factory=missing, description="Short human-readable task name"
    )
    task_type: StatusField = Field(
        default_factory=missing,
        description="Task category: modeling | simulation | fitting | data_analysis | plotting | writing",
    )
    research_goal: StatusField = Field(
        default_factory=missing, description="Free-text research goal or objective"
    )


class PhysicsSection(BaseModel):
    """Physical system and mechanism."""
    physical_system: StatusField = Field(
        default_factory=missing,
        description="Physical system type, e.g. nanoparticle_on_film, single_particle, waveguide",
    )
    physical_mechanism: StatusField = Field(
        default_factory=missing,
        description="Dominant mechanism: plasmon, scattering, waveguide, resonance, etc.",
    )
    model_dimension: StatusField = Field(
        default_factory=missing,
        description="Simulation dimensionality: 2d | 3d | axisymmetric",
    )
    structure_type: StatusField = Field(
        default_factory=missing,
        description="Structure type: single_particle, array, film, waveguide, etc.",
    )


class GeometryMaterialSection(BaseModel):
    """Geometry definition and material system."""
    geometry_definition: StatusField = Field(
        default_factory=missing,
        description="Structured geometry: type, dimensions, units",
    )
    material_system: StatusField = Field(
        default_factory=missing,
        description="Structured material system: list of materials with roles and models",
    )
    material_model: StatusField = Field(
        default_factory=missing,
        description="Primary dispersion model: Drude, Johnson-Christy, etc.",
    )
    substrate_or_film_info: StatusField = Field(
        default_factory=missing,
        description="Substrate / film details: material, thickness",
    )
    particle_info: StatusField = Field(
        default_factory=missing,
        description="Nanoparticle details: type, material, dimensions",
    )
    gap_medium: StatusField = Field(
        default_factory=missing,
        description="Medium filling the gap (e.g. SiO2, water, air)",
    )
    key_parameters: StatusField = Field(
        default_factory=missing,
        description="Key named parameters extracted from description (list of strings)",
    )


class SimulationSection(BaseModel):
    """Solver and simulation settings."""
    solver_method: StatusField = Field(
        default_factory=missing,
        description="Solver: fdtd | fem | rcwa | analytical | coupled_oscillator",
    )
    software_tool: StatusField = Field(
        default_factory=missing,
        description="Software: meep, lumerical, comsol, matlab, or free-form string",
    )
    sweep_plan: StatusField = Field(
        default_factory=missing,
        description="Parameter sweep plan: type, range, step, unit",
    )
    excitation_source: StatusField = Field(
        default_factory=missing,
        description="Excitation type: plane_wave, tfsf, dipole, mode_source, etc.",
    )
    source_setting: StatusField = Field(
        default_factory=missing,
        description="Source configuration: wavelength range, polarization, angle, amplitude",
    )
    polarization: StatusField = Field(
        default_factory=missing,
        description="Polarization: linear_x, linear_y, TM, TE, circular, etc.",
    )
    incident_direction: StatusField = Field(
        default_factory=missing,
        description="Incident direction: normal, oblique, etc.",
    )
    boundary_condition: StatusField = Field(
        default_factory=missing,
        description="Boundary conditions per direction: PML, periodic, PEC, PMC, Bloch",
    )
    symmetry_setting: StatusField = Field(
        default_factory=missing,
        description="Symmetry exploitation: mirror, rotational, periodic",
    )
    mesh_setting: StatusField = Field(
        default_factory=missing,
        description="Mesh config: type, accuracy, size limits, override regions",
    )
    stability_setting: StatusField = Field(
        default_factory=missing,
        description="Stability: time step, auto-shutoff, simulation time",
    )
    monitor_setting: StatusField = Field(
        default_factory=missing,
        description="Monitor placement: type, locations, frequency points",
    )


class OutputSection(BaseModel):
    """Desired outputs and post-processing."""
    output_observables: StatusField = Field(
        default_factory=missing,
        description="List of observable types: spectrum, cross_section, field_distribution, etc.",
    )
    postprocess_target: StatusField = Field(
        default_factory=missing,
        description="Post-processing targets: lorentzian_fit, fwhm_extraction, T2_extraction, etc.",
    )


# ---------------------------------------------------------------------------
# Root spec
# ---------------------------------------------------------------------------

class OpticalSpec(BaseModel):
    """The unified optical simulation specification."""

    task: TaskSection = Field(default_factory=TaskSection, description="Task metadata")
    physics: PhysicsSection = Field(default_factory=PhysicsSection, description="Physical system description")
    geometry_material: GeometryMaterialSection = Field(
        default_factory=GeometryMaterialSection, description="Geometry and materials"
    )
    simulation: SimulationSection = Field(
        default_factory=SimulationSection, description="Solver and simulation settings"
    )
    output: OutputSection = Field(default_factory=OutputSection, description="Output and post-processing")

    # system fields
    confirmed_fields: dict[str, Any] = Field(
        default_factory=dict,
        description="All fields with status='confirmed' — path → value",
    )
    inferred_fields: dict[str, Any] = Field(
        default_factory=dict,
        description="All fields with status='inferred' — path → {value, note}",
    )
    missing_fields: list[str] = Field(
        default_factory=list,
        description="List of dotted paths for all missing fields",
    )
    assumption_log: list[str] = Field(
        default_factory=list,
        description="Human-readable assumption statements from inferred fields",
    )
    validation_status: ValidationStatus = Field(
        default_factory=ValidationStatus,
        description="Validation outcome: is_executable, errors, warnings",
    )

    # ------------------------------------------------------------------
    # Convenience helpers
    # ------------------------------------------------------------------

    _SECTION_NAMES = ("task", "physics", "geometry_material", "simulation", "output")

    def collect_missing_fields(self) -> list[str]:
        """Walk through every StatusField and collect paths whose status is 'missing'."""
        missing_paths: list[str] = []
        for section_name in self._SECTION_NAMES:
            section = getattr(self, section_name)
            for field_name in type(section).model_fields:
                sf = getattr(section, field_name)
                if isinstance(sf, StatusField) and sf.status == "missing":
                    missing_paths.append(f"{section_name}.{field_name}")
        self.missing_fields = missing_paths
        return missing_paths

    def collect_confirmed_inferred(self) -> tuple[dict[str, Any], dict[str, Any]]:
        """Populate confirmed_fields and inferred_fields dicts."""
        confirmed_d: dict[str, Any] = {}
        inferred_d: dict[str, Any] = {}
        for section_name in self._SECTION_NAMES:
            section = getattr(self, section_name)
            for field_name in type(section).model_fields:
                sf = getattr(section, field_name)
                if not isinstance(sf, StatusField):
                    continue
                path = f"{section_name}.{field_name}"
                if sf.status == "confirmed":
                    confirmed_d[path] = sf.value
                elif sf.status == "inferred":
                    inferred_d[path] = {"value": sf.value, "note": sf.note}
        self.confirmed_fields = confirmed_d
        self.inferred_fields = inferred_d
        return confirmed_d, inferred_d

    def collect_assumptions(self) -> list[str]:
        """Collect notes from all inferred fields."""
        assumptions: list[str] = []
        for section_name in self._SECTION_NAMES:
            section = getattr(self, section_name)
            for field_name in type(section).model_fields:
                sf = getattr(section, field_name)
                if isinstance(sf, StatusField) and sf.status == "inferred" and sf.note:
                    assumptions.append(f"[{section_name}.{field_name}] {sf.note}")
        self.assumption_log = assumptions
        return assumptions

    def collect_all(self) -> None:
        """Run all collectors at once."""
        self.collect_missing_fields()
        self.collect_confirmed_inferred()
        self.collect_assumptions()

    def to_flat_dict(self) -> dict[str, Any]:
        """Export as a plain dict suitable for JSON serialization."""
        result: dict[str, Any] = {}
        for section_name in self._SECTION_NAMES:
            section = getattr(self, section_name)
            result[section_name] = {}
            for field_name in type(section).model_fields:
                val = getattr(section, field_name)
                if isinstance(val, StatusField):
                    # If value is a Pydantic model, serialize it
                    v = val.value
                    if isinstance(v, BaseModel):
                        v = v.model_dump()
                    elif isinstance(v, list):
                        v = [
                            item.model_dump() if isinstance(item, BaseModel) else item
                            for item in v
                        ]
                    result[section_name][field_name] = {
                        "value": v,
                        "status": val.status,
                        "note": val.note,
                    }
                else:
                    # Plain field (e.g. task_id)
                    result[section_name][field_name] = val
        result["confirmed_fields"] = self.confirmed_fields
        result["inferred_fields"] = self.inferred_fields
        result["missing_fields"] = self.missing_fields
        result["assumption_log"] = self.assumption_log
        result["validation_status"] = self.validation_status.model_dump()
        return result

    # ------------------------------------------------------------------
    # JSON Schema export
    # ------------------------------------------------------------------

    @classmethod
    def export_json_schema(cls, *, indent: int = 2) -> str:
        """Export the full spec as a JSON Schema string."""
        schema = cls.model_json_schema()
        return json.dumps(schema, indent=indent, ensure_ascii=False)

    @classmethod
    def export_json_schema_dict(cls) -> dict[str, Any]:
        """Export the full spec as a JSON Schema dict."""
        return cls.model_json_schema()
