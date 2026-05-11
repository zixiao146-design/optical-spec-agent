# Draft Release Notes v0.7.0

> Draft only. No GitHub release or tag has been created. The packaged version
> may still be `0.5.0` until release owners choose the v0.7 version-bump path.

## Summary

v0.7 introduces a multi-solver adapter foundation. The release keeps the Meep
hero workflow intact while adding MVP preview/scaffold generation for MPB,
Gmsh, Elmer, and Optiland.

## New

- Adapter registry with metadata and dispatch.
- `optical-spec adapter-list`.
- `optical-spec adapter-generate`.
- MPB adapter MVP for band/eigenmode Python scaffolds.
- Gmsh adapter MVP for `.geo` geometry/mesh scaffolds.
- Elmer adapter MVP for `.sif` solver-input scaffolds.
- Optiland adapter MVP for Python ray-tracing scaffolds.
- Parser keyword support for MPB, Gmsh, Elmer, Optiland, band diagrams,
  eigenmodes, FEM mesh workflows, ray tracing, MTF, and spot diagrams.
- Semantic benchmark expanded from 15 to 27 cases.

## Preserved

- `meep-generate`
- `meep-check`
- `meep-run`
- `diagnose`
- parser/validator/schema public surface
- no external solver requirement in tests

## Limitations

- Adapters generate solver-native input only; they do not run solvers.
- MPB/Gmsh/Elmer/Optiland outputs are MVP scaffolds, not production-ready inputs.
- No real LLM parser is included.
- No production-grade physical validation or formal convergence proof is claimed.
- Optiland support is scaffold-level until the schema can represent sequential
  lens prescriptions.
- Gmsh/Elmer support remains preview-level until the schema carries richer FEM
  geometry, material, mesh, boundary-condition, and monitor definitions.

## Suggested Verification

```bash
pytest -q
python benchmarks/run_benchmark.py --mode key_fields
python benchmarks/run_semantic_benchmark.py
python benchmarks/run_semantic_benchmark.py --report outputs/semantic_benchmark_report.json
make check
```
