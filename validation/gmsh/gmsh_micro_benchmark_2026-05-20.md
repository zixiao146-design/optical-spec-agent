# Gmsh Optional Micro-benchmark Evidence - 2026-05-20

- Solver: Gmsh
- Benchmark type: optional manual solver-backed micro-benchmark
- Approval record path: `docs/optional_solver_approval_records/gmsh_micro_benchmark_approval_2026-05-20.md`
- Review decision path: `docs/optional_solver_approval_records/gmsh_micro_benchmark_review_2026-05-20.md`
- Project version: `0.9.0rc8.dev0`
- Current public prerelease: `v0.9.0rc7`
- Solver path: `/opt/homebrew/bin/gmsh`
- Gmsh version: `4.15.2-git`
- Input fixture: `examples/specs/gmsh_preview.json`
- Generated preview artifact: `/tmp/osa-gmsh-micro-benchmark-output/gmsh_preview.geo`
- Output mesh artifact: `/tmp/osa-gmsh-micro-benchmark-output/gmsh_preview.msh`
- Report path: `/tmp/osa-gmsh-micro-benchmark-report.json`

## Command Used

```bash
OSA_RUN_OPTIONAL_GMSH_VALIDATION=1 \
OSA_GMSH_VALIDATION_REPORT=/tmp/osa-gmsh-micro-benchmark-report.json \
OSA_GMSH_OUTPUT_DIR=/tmp/osa-gmsh-micro-benchmark-output \
./scripts/run_optional_solver_micro_benchmarks.sh
```

The wrapper executed only the Gmsh optional pilot:

```bash
/opt/homebrew/bin/gmsh -3 /tmp/osa-gmsh-micro-benchmark-output/gmsh_preview.geo -format msh2 -o /tmp/osa-gmsh-micro-benchmark-output/gmsh_preview.msh
```

## Report Summary

- `gmsh_available`: true
- `optional_validation_enabled`: true
- `gmsh_executed`: true
- `passed`: true
- Passed: yes
- `exit_code`: 0
- `solver_version`: `4.15.2-git`
- `proprietary_required`: false
- `production_grade_validation_claimed`: false
- `formal_convergence_proof_claimed`: false

The run generated a local `.geo` preview artifact and a Gmsh `.msh` mesh
artifact in `/tmp`. The Gmsh stdout summary reported 3D meshing completion with
`362 nodes` and `1092 elements`. The stderr summary was empty.

## Boundaries

- External solver executed: yes, Gmsh only.
- Meep executed: no.
- MPB executed: no.
- Optiland executed: no.
- Elmer executed: no.
- PyPI upload or publication: no.
- TestPyPI upload: no.
- Git tag or GitHub release creation: no.
- `v1.0.0` release action: no.
- Production-grade physical validation claimed: no.
- Formal convergence proof claimed: no.
- Optical correctness claimed: no.

## Interpretation

This evidence supports only a narrow optional manual claim: the local Gmsh
adapter-preview path can produce a `.geo` artifact from the project fixture and
Gmsh can mesh that artifact in the maintainer's local environment. It is smoke /
mesh generation evidence, not optical correctness evidence.

The maintainer review decision accepts this record only as optional manual
mesh-generation smoke evidence. It does not authorize Optiland, Meep, MPB,
Elmer, any future Gmsh rerun, PyPI/TestPyPI upload, tag creation, or release
creation.

The generated `/tmp` artifacts are intentionally not committed. This repository
record preserves the reviewed report summary and safety boundaries.
