# Schema Stability Policy

> Version: 0.1.x — applies until v0.2.0

This document defines the **stable surface** of the optical-spec-agent schema: the set of fields whose names, paths, and semantics downstream consumers (solver adapters, benchmark runners, external tools) can rely on across 0.1.x patch releases.

## Stable fields (v0.1 core surface)

The following dotted paths are **frozen** for the 0.1.x series. They will not be renamed, relocated, or have their value semantics changed without a minor-version bump.

### Task section

| Path | Type | Description |
|------|------|-------------|
| `task.task_type` | enum string | `simulation`, `fitting`, `modeling`, `data_analysis`, `plotting`, `writing` |
| `task.research_goal` | free text | User's research objective |

### Physics section

| Path | Type | Description |
|------|------|-------------|
| `physics.physical_system` | enum string | `nanoparticle_on_film`, `single_particle`, `waveguide`, `grating`, `metasurface`, etc. |
| `physics.structure_type` | enum string | `sphere_on_film`, `cube_on_film`, `cross_structure`, `waveguide`, `array`, etc. |
| `physics.physical_mechanism` | enum string | `gap_plasmon`, `plasmon`, `scattering`, `waveguide`, `resonance`, etc. |
| `physics.model_dimension` | enum string | `2d`, `3d`, `axisymmetric` |

### Simulation section

| Path | Type | Description |
|------|------|-------------|
| `simulation.solver_method` | enum string | `fdtd`, `fem`, `rcwa`, `analytical`, `coupled_oscillator` |
| `simulation.software_tool` | enum string | `meep`, `lumerical`, `comsol`, `python`, etc. |
| `simulation.excitation_source` | enum string | `plane_wave`, `tfsf`, `dipole`, `mode_source`, etc. |
| `simulation.source_setting` | SourceSetting obj | Structured: `source_type`, `wavelength_range`, `polarization`, `incident_angle` |
| `simulation.boundary_condition` | BoundaryConditionSetting obj | Structured: `x_min/max`, `y_min/max`, `z_min/max` |
| `simulation.monitor_setting` | MonitorSetting obj | Structured: `monitor_type`, `locations`, `frequency_points` |
| `simulation.sweep_plan` | SweepPlan obj | Structured: `sweep_type`, `variable`, `range_start`, `range_end`, `step`, `unit` |

### Output section

| Path | Type | Description |
|------|------|-------------|
| `output.output_observables` | list[string] | `spectrum`, `scattering_spectrum`, `field_distribution`, `mode_profile`, `FWHM`, etc. |
| `output.postprocess_target` | list[PostprocessTargetSpec] | `lorentzian_fit`, `fwhm_extraction`, `T2_extraction`, `resonance_wavelength`, etc. |

### System fields

| Path | Type | Description |
|------|------|-------------|
| `confirmed_fields` | dict[path → value] | All confirmed field values |
| `inferred_fields` | dict[path → {value, note}] | All inferred field values with derivation notes |
| `missing_fields` | list[path] | Dotted paths for all missing fields |
| `assumption_log` | list[string] | Human-readable inference statements |
| `validation_status.is_executable` | bool | Whether the spec can be forwarded to a solver |
| `validation_status.errors` | list[string] | Critical issues that block execution |
| `validation_status.warnings` | list[string] | Non-critical issues |

### Enum values

The enum member strings in `TaskType`, `SolverMethod`, `SoftwareTool`, `PhysicalSystem`, `StructureType`, `ExcitationSource`, `OutputObservable`, and `PostprocessTarget` are also part of the stable surface. New members may be **appended**; existing members will not be renamed or removed.

## Fields that may still change

The following are **not** frozen and may evolve within 0.1.x:

- `task.task_name` — heuristically generated, format may change
- `geometry_material.geometry_definition.dimensions` — key names are free-form
- `geometry_material.key_parameters` — format and extraction heuristics may change
- `geometry_material.particle_info` — sub-field structure may be refined
- `geometry_material.gap_medium` — may be promoted to a structured object
- `simulation.mesh_setting` — sub-fields may be added or renamed
- `simulation.stability_setting` — sub-fields may be added
- `simulation.symmetry_setting` — may be restructured
- All `description` free-text fields within structured sub-models

## Compatibility principles for 0.1.x

1. **Append-only for new fields.** New StatusField paths will be added under existing sections. Existing paths will not be renamed or removed.
2. **Enum members are append-only.** New enum values may be added; existing values will not be renamed.
3. **Structured sub-model fields are append-only.** New optional fields may be added to `SweepPlan`, `SourceSetting`, etc. Existing fields keep their names and types.
4. **`validation_status` structure is stable.** The three fields (`is_executable`, `errors`, `warnings`) will not change. New top-level fields (e.g., `info`) may be added.
5. **Breaking changes require v0.2.0.** Any rename, removal, or semantic change to a stable field will bump the minor version.

## How to use this document

- **Solver adapter authors:** Depend only on stable fields. Use `missing_fields` and `validation_status` to decide whether a spec is ready for your tool.
- **Benchmark contributors:** Golden cases should assert stable fields in `key_fields` mode. Non-stable fields should only be tested in `exact` mode.
- **Parser authors:** Your output must populate all stable fields. Non-stable fields are best-effort.
