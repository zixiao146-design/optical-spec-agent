# v0.7 Release Readiness Draft

> This is a readiness note for the main branch, not a GitHub release or tag.

## Version and Release Status

- Historical note: when this v0.7 draft was written, the packaged baseline was
  `0.5.0`. For the current package version, use
  `docs/release_readiness_current.md`.
- Main branch contains v0.6 diagnostics and v0.7 adapter MVP work that may be
  ahead of the latest formal GitHub release.
- This document is a release-candidate checklist only. Do not infer that a
  GitHub release or tag has been created.
- Before publishing v0.7, decide whether to publish an intermediate v0.6
  release or bump directly from `0.5.0` to `0.7.0`.

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

optical-spec parse "用 MPB 计算二维光子晶体的 band diagram，扫 Γ-X-M-Γ k 点，输出前 8 条能带。" \
  --output outputs/mpb_spec.json
optical-spec adapter-generate outputs/mpb_spec.json --tool mpb --output outputs/mpb_band.py

optical-spec parse "用 Gmsh 为 Si3N4 脊波导横截面生成 FEM 网格，波长 1550 nm，SiO2 下包层，空气上包层。" \
  --output outputs/gmsh_spec.json
optical-spec adapter-generate outputs/gmsh_spec.json --tool gmsh --output outputs/waveguide.geo

optical-spec parse "用 Elmer 做 Si3N4 波导 FEM 模式分析，输入 mesh 为 waveguide.msh，输出有效折射率和模场。" \
  --output outputs/elmer_spec.json
optical-spec adapter-generate outputs/elmer_spec.json --tool elmer --mesh outputs/waveguide.msh --output outputs/case.sif

optical-spec parse "用 Optiland 设计一个简单单透镜成像系统，计算 spot diagram 和 MTF。" \
  --output outputs/optiland_spec.json
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

## Recommended Release Checklist

1. Re-run the verification commands above on a clean checkout.
2. Review `README.md`, this readiness note, and
   `docs/release_notes_v0.7.0.md` for version/status consistency.
3. Confirm no generated `outputs/` or `runs/` artifacts are committed unless
   intentionally included as small examples.
4. Decide the version bump strategy and update `pyproject.toml`,
   `src/optical_spec_agent/__init__.py`, and API health expectations together.
5. Only after review, create the GitHub release/tag outside this readiness pass.
