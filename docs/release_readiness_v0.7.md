# v0.7 Release Readiness Draft

> This is a readiness note for the main branch, not a GitHub release or tag.

## Achieved

- Adapter registry for `meep`, `mpb`, `gmsh`, `elmer`, and `optiland`.
- Generic CLI:
  - `optical-spec adapter-list`
  - `optical-spec adapter-generate`
- MVP preview/scaffold adapters:
  - MPB Python scaffold
  - Gmsh `.geo` scaffold
  - Elmer `.sif` scaffold
  - Optiland Python scaffold
- Parser keyword support for v0.7 adapter intents.
- Semantic benchmark expanded to 27 cases.
- Existing Meep and diagnose commands preserved.

## Verification Commands

```bash
pip install -e ".[dev]"
pytest -q
python benchmarks/run_benchmark.py --mode key_fields
python benchmarks/run_semantic_benchmark.py
python benchmarks/run_semantic_benchmark.py --report outputs/semantic_benchmark_report.json
make check
```

Manual smoke:

```bash
optical-spec adapter-list
optical-spec adapter-list --json
optical-spec adapter-generate outputs/mpb_spec.json --tool mpb --output outputs/mpb_band.py
optical-spec adapter-generate outputs/gmsh_spec.json --tool gmsh --output outputs/waveguide.geo
optical-spec adapter-generate outputs/elmer_spec.json --tool elmer --mesh outputs/waveguide.msh --output outputs/case.sif
optical-spec adapter-generate outputs/optiland_spec.json --tool optiland --output outputs/optiland_design.py
```

## Known Limitations

- Adapters generate solver input only.
- MPB/Gmsh/Elmer/Optiland are not executed.
- No real LLM parser is implemented.
- No production-grade physical validation is claimed.
- No formal convergence proof is provided.
- Optiland support is scaffold-level because lens-surface data is not in the
  current schema.
- Gmsh/Elmer are preview-level until FEM geometry/material/boundary fields are
  richer.

## Release Blockers to Review

- Decide whether to bump package version from `0.5.0` to `0.7.0` or publish v0.6
  first.
- Review generated scaffold wording for any accidental production-ready claims.
- Confirm CI remains solver-install-free.
