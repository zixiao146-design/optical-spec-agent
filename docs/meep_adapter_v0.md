# Meep Adapter v0.1

> Status: **Script generation only** — no execution, no result parsing.

## What it does

Converts a validated `OpticalSpec` JSON into a Meep Python script (`.py`) that
can be run manually by the user.

## What it does NOT do

- Run simulations or manage execution
- Parse simulation results
- Support all physical systems (only `nanoparticle_on_film`)
- Support all source types (only `plane_wave`)
- Support all observables (only `scattering_spectrum`-related)
- Handle arbitrary geometries

## Input contract

> This is an **adapter-level** contract. It defines what the Meep adapter reads
> from an `OpticalSpec`, which is a subset of the full spec schema.
> This is **not** a general-purpose Meep adapter — it covers only the
> `nanoparticle_on_film + fdtd + plane_wave + scattering_spectrum` path.

### Gate fields (must match exactly)

These fields are checked by `can_handle()` and determine whether the adapter
accepts the spec at all:

| Field | Required value |
|-------|---------------|
| `physics.physical_system` | `nanoparticle_on_film` |
| `simulation.solver_method` | `fdtd` |
| `simulation.software_tool` | `meep` |
| `simulation.excitation_source` | `plane_wave` (or missing) |

If any gate field mismatches, the adapter raises `AdapterError(category="unsupported_path")`.

### Required fields (must be present, no default)

These must exist in the spec and carry a non-missing value:

| Spec path | What the adapter reads | Error category |
|-----------|----------------------|----------------|
| `geometry_material.particle_info` | `particle_type`, `material`, `dimensions` | `missing_required_field` |
| `geometry_material.particle_info.particle_type` | shape: `sphere` / `cube` / `rod` | `unsupported_path` (if unknown) |
| `geometry_material.particle_info.dimensions` | diameter via `直径` / `diameter` / `边长` | `invalid_adapter_input` (if unparseable) |
| `geometry_material.substrate_or_film_info` | film info block | `missing_required_field` |
| `geometry_material.substrate_or_film_info.film_material` | e.g. `"Au"` | `missing_required_field` (if empty) |

### Optional fields with adapter defaults

When these fields are missing, the adapter fills in defaults and records them
in `MeepInputModel.defaults_applied` (and annotates the generated script header):

| Spec path | Default value | Note |
|-----------|--------------|------|
| `geometry_material.gap_medium` | SiO2 (n=1.45) | If empty string or missing |
| `geometry_material.substrate_or_film_info.film_thickness` | 100 nm | If empty or missing |
| `simulation.source_setting.wavelength_range` | 400–900 nm | If empty or unparseable |

### Adapter-internal parameters (always set by adapter)

These are not spec fields — they are fixed by the adapter and do not vary per spec:

| Parameter | Value | Defined in |
|-----------|-------|-----------|
| Resolution | 50 px/μm | `MeepInputModel` default |
| PML thickness | 1.0 μm | `MeepInputModel` default |
| Frequency points | 200 | `MeepInputModel` default |
| Gap thickness | 5 nm (or from sweep start) | `_ADAPTER_DEFAULTS` in translator |
| Cell padding | r_particle + 0.5 μm | template |

### Optional fields (used if present, no default)

| Spec path | Effect |
|-----------|--------|
| `simulation.boundary_condition` | Read but not directly mapped (PML always used) |
| `simulation.monitor_setting` | Read but not directly used |
| `simulation.sweep_plan` | If `parameter` type with `gap` variable → generates sweep loop |
| `output.output_observables` | Read for validation, always assumes scattering_spectrum |
| `output.postprocess_target` | Generates peak finding / FWHM / T₂ code if present |

### Currently unsupported fields

| Field | Status |
|-------|--------|
| `physics.structure_type` | Read but not enforced |
| `geometry_material.geometry_definition` | Not used — geometry is derived from particle_info + film |
| `geometry_material.material_system` | Not used — materials are hardcoded Drude |
| `mesh_setting` / resolution hints from spec | Not connected — resolution is adapter-internal |
| `simulation.time_setting` | Not connected — run time is hardcoded `until=200` |
| `simulation.convergence` | Not connected |
| `task.funding_source` / `task.paper_reference` | Not adapter-relevant |

## Error categories

All adapter errors use `AdapterError(category, field, detail)`:

| Category | Meaning |
|----------|---------|
| `unsupported_path` | Spec targets a system/solver/software/shape this adapter doesn't handle |
| `missing_required_field` | A required spec field is absent or empty |
| `invalid_adapter_input` | Field value can't be processed (unparseable, unknown, conflicting) |

Each error exposes `.category`, `.field`, and `.detail` attributes for programmatic use.

## Default values policy

When the adapter applies a default, it:

1. Records the default in `MeepInputModel.defaults_applied` as a human-readable string.
2. Annotates the generated script header with an `Adapter-applied defaults` section.
3. Emits a `UserWarning` for wavelength range defaults.

Defaults are centralized in `_ADAPTER_DEFAULTS` (translator.py) for
translator-level defaults, and in `MeepInputModel` field defaults for
model-level parameters. No magic numbers are scattered in the translation logic.

## Generated script structure

```
import meep as mp, numpy, matplotlib
  ↓
Material definitions (simplified Drude for Au/Ag)
  ↓
Geometry: sphere on film with gap dielectric
  ↓
Source: plane wave
  ↓
Cell + PML boundaries
  ↓
Flux monitors (scattering / absorption boxes)
  ↓
Simulation.run()
  ↓
Post-processing: spectrum plot, optional peak finding / FWHM
```

## Usage

```bash
# Generate a spec first
optical-spec parse "用Meep FDTD仿真金纳米球-金膜gap plasmon..." -o spec.json

# Generate Meep script
optical-spec meep-generate spec.json -o sim.py

# Run manually
python sim.py
```

## Smoke validation

The adapter ships a built-in smoke test mode (`smoke=True` on the internal model)
that generates a stripped-down version of the simulation script:

| Parameter | Normal | Smoke |
|-----------|--------|-------|
| Resolution | 50 px/μm | 10 px/μm |
| Frequency points | 200 | 3 |
| Run steps | 200 | 20 |
| Materials | Drude dispersive | Simple dielectric (`ε = const`) |
| Plotting | Yes (matplotlib) | No |
| PML | 1.0 μm | 0.5 μm |

### What it verifies

- The generated Python script is syntactically valid.
- Meep can instantiate a `Simulation` object from the generated geometry, sources,
  and boundary conditions without raising an exception.
- `sim.run()` completes for a small number of time steps.
- Flux monitors return the expected number of frequency / flux values.

### What it does NOT verify

- Physical correctness of the simulation results.
- Convergence of the FDTD solver.
- Accuracy of the dispersive material model.
- Scattering spectrum shape or resonance positions.
- Plotting or post-processing code.

In other words: **passing the smoke test means the adapter produces a structurally
valid Meep script, not that the physics is correct.**

### Running the smoke test

```bash
# From the project root
pytest tests/test_meep_adapter.py::TestMeepSmokeRun -v
```

If Meep is not installed in the current Python environment, the execution test is
automatically skipped. The syntax-validity test (`test_smoke_script_is_valid_python`)
always runs regardless of whether Meep is available.

The test probes two locations for a usable Meep:

1. Direct `import meep` in the current interpreter.
2. `micromamba run -n meep python` (conda env named `meep`).
