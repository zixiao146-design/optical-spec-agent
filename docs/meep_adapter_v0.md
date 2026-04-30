# Meep Adapter v0.4 Research-Preview

> Status: **Script generation only** — no execution, no result parsing pipeline.

## What it does

Converts a validated `OpticalSpec` JSON into a Meep Python script (`.py`) that
can be run manually by the user.

The adapter now supports three script generation modes:

| Mode | Purpose | Output characteristics |
|------|---------|------------------------|
| `preview` | 快速脚本预览 | 保留当前简化 preview 路径，帮助检查几何、参数和基本脚本结构 |
| `research_preview` | 更可信的研究预览脚本 | reference run + structure run + flux subtraction + CSV/JSON output |
| `smoke` | 结构性冒烟验证 | 最小材料/分辨率/步数，只验证脚本能否被 Meep 实例化和短步运行 |

## What it does NOT do

- Run simulations or manage execution
- Parse simulation results into a project-managed pipeline
- Support all physical systems (only `nanoparticle_on_film`)
- Support all source types (only `plane_wave`)
- Support all observables (only `scattering_spectrum`-related)
- Handle arbitrary geometries
- Claim production-grade or publication-ready physical fidelity

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

### Preview mode

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

### Research-preview mode

```
Import Meep + materials library + CSV/JSON helpers
  ↓
Resolve Au/Ag from meep.materials
  ↓
Resolve dielectric gap medium from library or constant-index fallback
  ↓
Build geometry(include_particle=False)  # reference run
  ↓
Closed flux box / multi-surface flux regions
  ↓
get_flux_data() on reference run
  ↓
Build geometry(include_particle=True)   # structure run
  ↓
load_minus_flux_data() on structure run
  ↓
Aggregate particle-induced flux
  ↓
Save scattering_spectrum.csv
  ↓
Save postprocess_results.json
  ↓
Save scattering_spectrum.png
```

The research-preview script is still not production-grade. It improves physical
credibility versus the preview path, but it is still a generated starting point,
not a fully validated Meep workflow.

## Usage

```bash
# Generate a spec first
optical-spec parse "用Meep FDTD仿真金纳米球-金膜gap plasmon..." -o spec.json

# Generate Meep preview script
optical-spec meep-generate spec.json -o sim.py

# Generate research-preview script
optical-spec meep-generate spec.json -o sim_research.py --mode research-preview

# Generate smoke script
optical-spec meep-generate spec.json -o smoke.py --mode smoke

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

## Research-preview limitations

- It still generates scripts only; this project does not run Meep yet.
- It does not provide a managed result parsing pipeline yet.
- Peak finding / resonance / FWHM extraction remain heuristic.
- Closed-box flux subtraction is a research-preview workflow, not a final validated scattering observable definition.
- Any dielectric fallback using `mp.Medium(epsilon=n**2)` should be treated as an approximation.

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
