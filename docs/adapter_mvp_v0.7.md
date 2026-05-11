# v0.7 Adapter MVP

> Scope: multi-solver adapter foundation and preview/scaffold generation.
> Non-goal: running solvers or claiming production-grade physical validation.

## What v0.7 Adds

- A simple adapter registry.
- `optical-spec adapter-list`.
- `optical-spec adapter-generate`.
- MPB, Gmsh, Elmer, and Optiland MVP adapters.
- Semantic benchmark coverage for adapter-intent parsing.

## Commands

```bash
optical-spec adapter-list
optical-spec adapter-list --json

optical-spec adapter-generate spec.json --tool auto --output outputs/generated_input.py
optical-spec adapter-generate spec.json --tool mpb --output outputs/mpb_band.py
optical-spec adapter-generate spec.json --tool gmsh --output outputs/geometry.geo
optical-spec adapter-generate spec.json --tool elmer --mesh outputs/geometry.msh --output outputs/case.sif
optical-spec adapter-generate spec.json --tool optiland --output outputs/optiland_design.py
```

Use `--strict` to fail when adapter readiness reports missing required fields.
Without `--strict`, adapters can generate annotated scaffolds that clearly list
warnings, missing fields, defaults, and limitations.

## Adapter Scopes

| Adapter | Output | MVP behavior |
|---------|--------|--------------|
| Meep | Python | Existing specialized nanoparticle-on-film script path |
| MPB | Python | Band/eigenmode preview script with default lattice, k-points, resolution, and bands |
| Gmsh | `.geo` | Annotated geometry/mesh scaffold with physical groups |
| Elmer | `.sif` | FEM solver-input scaffold, optionally referencing `--mesh` |
| Optiland | Python | Imaging/ray-tracing scaffold with TODOs for lens surfaces and glass catalog |

## Limitations

- Adapters generate input only; they do not run MPB, Gmsh, Elmer, or Optiland.
- MPB/Gmsh/Elmer outputs are schematic until the schema carries richer geometry,
  material, boundary, mesh, and monitor definitions.
- Optiland is scaffold-level because `OpticalSpec` does not yet encode a full
  sequential lens prescription.
- Auto dispatch is intentionally small and may require explicit `--tool`.
- No generated input should be interpreted as production-ready without expert
  review and solver-side validation.

## Test Coverage

v0.7 adds tests for:

- adapter registry lookup and dispatch;
- per-adapter scaffold generation;
- CLI JSON and file-writing behavior;
- strict vs non-strict missing-field behavior;
- parser keyword extraction for MPB/Gmsh/Elmer/Optiland;
- semantic benchmark cases for adapter intent routing.
