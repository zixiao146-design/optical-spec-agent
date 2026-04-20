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

## Minimum supported path

The adapter will only accept specs that match ALL of:

| Field | Required value |
|-------|---------------|
| `physics.physical_system` | `nanoparticle_on_film` |
| `simulation.solver_method` | `fdtd` |
| `simulation.software_tool` | `meep` |
| `simulation.excitation_source` | `plane_wave` (or missing — defaults to plane_wave) |

Required populated fields:

- `geometry_material.particle_info` — particle type, material, dimensions
- `geometry_material.substrate_or_film_info` — film material
- `simulation.source_setting` — wavelength range

Optional fields (defaults applied if missing):

- `geometry_material.gap_medium` — defaults to SiO2 (n=1.45)
- `geometry_material.substrate_or_film_info.film_thickness` — defaults to 100nm
- `simulation.sweep_plan` — if gap sweep present, generates parameter loop
- `output.postprocess_target` — resonance_wavelength / fwhm extraction code

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
