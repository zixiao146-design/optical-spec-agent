# Open-Source Integration Focus

> **Status**: Direction document. No adapter has been implemented yet.
> This document describes the prioritized roadmap for solver integration.

---

## Why open-source-first

Three reasons the adapter roadmap targets open-source tools exclusively:

1. **Scriptable by design.** Agents need to call tools through Python APIs or CLI, not GUI workflows. Open-source FDTD/FEM/ray-tracing tools are built for script-driven use.

2. **Reproducible by default.** No license server, no dongle, no seat limit. Anyone can clone the repo, install dependencies, and reproduce results — which is what `optical-spec-agent` is about.

3. **Composable.** Meep + Gmsh + Elmer + Optiland can be combined in a single Python process. Commercial tools cannot.

---

## Adapter priority tiers

| Priority | Tool | Method | Roadmap | Rationale |
|----------|------|--------|---------|-----------|
| **P0** | **Meep** | FDTD | v0.3 | Pure Python API, largest nanoplasmonics community, macOS-native, `is_executable` specs map directly to Meep objects |
| P1 | **MPB** | Eigenmode | v0.4 | Same ecosystem as Meep (NanoComp), shared material definitions, low marginal cost after Meep adapter |
| P1 | **Gmsh** + **Elmer** | FEM | v0.5 | Covers waveguide mode analysis, FEM scattering — problems Meep handles poorly. Gmsh is Elmer's standard mesher |
| P2 | **Optiland** / **RayOptics** | Ray tracing | v0.6 | Opens imaging optics direction. Optiland is pure Python, RayOptics adds .zmx/.seq file compatibility |
| P2 | **FreeCAD** | CAD | post-v0.6 | Auxiliary — when Gmsh geometry scripts cannot describe complex mechanical structures |

## Why Meep is P0

Meep is the first adapter target (v0.3) for specific reasons:

- **Direct spec-to-script mapping.** An `OpticalSpec` with `is_executable: true` contains `solver_method=fdtd`, `excitation_source`, `source_setting`, `boundary_condition`, `sweep_plan`, `monitor_setting` — these map 1:1 to Meep's `Simulation`, `Source`, `PML`, and `FluxMonitor` objects.
- **Pure Python.** `import meep` — no CLI wrapping, no file format parsing, no template engine needed.
- **Already in examples.** The gap plasmon demo (golden-02, golden-07) already parses Meep-specific input and produces a spec that is close to Meep-ready.
- **Validates the pipeline.** A working Meep adapter proves the full chain: NL → spec → validation → solver script → simulation output. This is the project's first end-to-end proof point.

## Why adapter comes before LLM parser

The roadmap deliberately schedules adapter work (v0.3–v0.6) before LLM integration (v0.7):

1. **Spec schema must stabilize first.** Real solver feedback reveals which spec fields are missing, ambiguous, or incorrectly typed. Building adapters before the LLM parser ensures the schema is battle-tested.
2. **Ground truth for LLM training.** The rule-based parser + golden cases provide labeled (input, expected_output) pairs. This dataset is the evaluation baseline for any future LLM parser.
3. **User value is in the adapter.** Parsing alone is a means to an end. Users want to run simulations. Shipping a Meep adapter in v0.3 delivers tangible value; a better parser in v0.7 refines the input experience.

---

## Commercial software examples

The repository contains examples referencing COMSOL and Lumerical (e.g., `example_03_lumerical_fdtd_scattering.py`, `example_04_comsol_mode_analysis.py`). These exist for **schema coverage** — they test whether the parser can handle FEM and commercial-software-specific inputs.

They are **not** adapter targets. The current roadmap does not plan adapters for COMSOL or Lumerical. If commercial-software compatibility is needed in the future, it will be a secondary, community-contributed interface.

See also: [`docs/open_source_stack.md`](open_source_stack.md) for the full tool-stack rationale and per-tool details.
