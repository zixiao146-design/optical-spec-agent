# Adapter Architecture

> Status: v0.7 adapter foundation. Adapters generate solver-native input only;
> they do not run MPB, Gmsh, Elmer, Optiland, or Meep.

## Purpose

Adapters are the boundary between a validated `OpticalSpec` and a solver-native
input file. They are deliberately narrower than the full schema: each adapter
declares which fields it consumes, which solver methods and physical systems it
supports, and which missing fields prevent strict generation.

The strongest production path remains:

```text
natural language -> OpticalSpec -> validation -> Meep script -> optional meep-run artifacts
```

v0.7 adds a generic scaffold path:

```text
OpticalSpec -> adapter registry -> MPB / Gmsh / Elmer / Optiland preview input
```

## Core Interfaces

`src/optical_spec_agent/adapters/base.py` defines:

- `BaseAdapter`: abstract `can_handle(spec)` and `generate(spec)` contract.
- `AdapterMetadata`: tool name, output language, extension, supported methods,
  supported systems, consumed fields, status, and limitations.
- `AdapterReadiness`: adapter-level readiness result with errors, warnings,
  `missing_required`, and defaults.
- `AdapterResult`: generated content plus optional warnings, errors, metadata,
  generated files, defaults, and limitations.

General `SpecValidator` answers: “is the spec generally complete?”

Adapter readiness answers: “is this spec enough for this adapter to generate an
honest solver input?”

These concepts intentionally stay separate.

## Registry

`src/optical_spec_agent/adapters/registry.py` keeps a simple in-process registry:

- `list_adapters()`
- `get_adapter(tool_name)`
- `dispatch_adapter(spec, preferred_tool=None)`

No dynamic plugin discovery is used yet. The current registered adapters are:

| Tool | Status | Output | Scope |
|------|--------|--------|-------|
| `meep` | preview | Python | Specialized nanoparticle-on-film FDTD scripts |
| `mpb` | mvp | Python | Band/eigenmode scaffold |
| `gmsh` | mvp | `.geo` | Geometry/mesh scaffold |
| `elmer` | mvp | `.sif` | FEM solver-input scaffold |
| `optiland` | mvp | Python | Imaging/ray-tracing scaffold |

`preferred_tool="auto"` first checks `simulation.software_tool`, then
`simulation.solver_method`, then a small physical-system fallback map.

## Generic CLI

```bash
optical-spec adapter-list
optical-spec adapter-list --json

optical-spec adapter-generate spec.json --tool auto --output outputs/generated_input.py
optical-spec adapter-generate spec.json --tool mpb --output outputs/mpb_band.py
optical-spec adapter-generate spec.json --tool gmsh --output outputs/geometry.geo
optical-spec adapter-generate spec.json --tool elmer --mesh outputs/geometry.msh --output outputs/case.sif
optical-spec adapter-generate spec.json --tool optiland --output outputs/optiland_design.py
```

`--strict` exits nonzero when readiness reports errors or missing required
fields. Without `--strict`, MVP adapters may still generate annotated scaffolds
with warnings and limitations.

`meep-generate` remains the backward-compatible Meep-specific command because it
exposes Meep script modes and dedicated readiness reporting.

## Adapter Boundaries

Adapters may:

- consume only the subset of `OpticalSpec` they need;
- apply documented scaffold defaults;
- report `missing_required`;
- emit warnings for unsupported or placeholder fields;
- generate comments/TODOs in solver-native files.

Adapters must not:

- run external solvers;
- hide missing physics behind silent defaults;
- claim production-grade validation;
- mutate the `OpticalSpec`;
- require MPB/Gmsh/Elmer/Optiland/Meep to be installed for tests.

## Current Limitations

- MPB, Gmsh, Elmer, and Optiland outputs are MVP scaffolds, not complete research
  inputs.
- Optiland support is especially scaffold-level because the current schema does
  not encode full sequential lens surfaces, glass catalogs, fields, stops, and
  operands.
- Gmsh/Elmer need richer FEM geometry/material/boundary schema before they can
  produce precise solver-ready models.
- Auto dispatch is intentionally simple and may require `--tool` for ambiguous
  FEM or geometry workflows.
