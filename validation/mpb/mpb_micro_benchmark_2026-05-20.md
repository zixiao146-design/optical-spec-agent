# MPB Optional Micro-benchmark Evidence - 2026-05-20

- solver: MPB / `meep.mpb`
- benchmark type: optional manual micro-benchmark
- approval record: `docs/optional_solver_approval_records/mpb_micro_benchmark_approval_2026-05-20.md`
- decision packet: `docs/optional_solver_approval_records/mpb_micro_benchmark_decision_packet.md`
- command used:

```bash
OSA_RUN_OPTIONAL_MPB_VALIDATION=1 \
OSA_SOLVER_PYTHON=/opt/homebrew/Caskroom/miniforge/base/envs/osa-solvers/bin/python \
OSA_MPB_VALIDATION_REPORT=/tmp/osa-mpb-micro-benchmark-report.json \
OSA_MPB_OUTPUT_DIR=/tmp/osa-mpb-micro-benchmark-output \
./scripts/run_optional_solver_micro_benchmarks.sh
```

- `OSA_SOLVER_PYTHON`: `/opt/homebrew/Caskroom/miniforge/base/envs/osa-solvers/bin/python`
- input fixture: `examples/specs/mpb_preview.json`
- generated preview artifact: `/tmp/osa-mpb-micro-benchmark-output/mpb_preview.py`
- generated validation script: `/tmp/osa-mpb-micro-benchmark-output/mpb_minimal_validation.py`
- output artifact: `/tmp/osa-mpb-micro-benchmark-output/mpb_validation_result.json`
- report path: `/tmp/osa-mpb-micro-benchmark-report.json`
- MPB / `meep.mpb` path: Python import through `from meep import mpb`
- PyMeep version reported by the MPB path: `1.33.0`
- passed: true
- exit code: 0
- external solver/package executed: yes, MPB / `meep.mpb` only
- MPB CLI required: no
- Meep FDTD benchmark executed: no
- Gmsh executed: no
- Optiland executed: no
- Elmer executed: no
- PyPI/TestPyPI upload actions: no
- tag/release actions: no
- external LLM called: no

## Report Summary

- `mpb_executed`: true
- `passed`: true
- `mpb_available`: true
- `mpb_cli_available`: false
- `solver_version`: `1.33.0`
- `meep_fdtd_benchmark_executed`: false
- `gmsh_executed`: false
- `optiland_executed`: false
- `elmer_executed`: false
- `production_grade_validation_claimed`: false
- `production_grade_mpb_validation_claimed`: false
- `production_band_structure_validation_claimed`: false
- `formal_convergence_proof_claimed`: false
- `optical_correctness_claimed`: false
- `proprietary_required`: false

## Artifact Summary

The validation result recorded:

- adapter artifact contains `from meep import mpb`: true
- adapter artifact contains `mpb.ModeSolver`: true
- validation type: `tiny_project_owned_mpb_pilot`
- k-points: 1
- bands: 1
- resolution: 4

The raw generated files remain under `/tmp` and are not committed.

## Non-claims

- no production-grade physical validation
- no production-grade MPB validation
- no production band-structure validation
- no formal convergence proof
- no optical correctness claim
- no default solver dependency
- no release gate behavior

## Scope Boundary

This evidence is optional manual MPB/band-structure smoke evidence only. It
shows that the local adapter-generated MPB scaffold and a tiny `meep.mpb` path
can execute after explicit maintainer approval with `OSA_SOLVER_PYTHON`. It does
not authorize Meep FDTD, Gmsh, Optiland, Elmer, PyPI/TestPyPI upload, tag
creation, GitHub release creation, or `v1.0.0` release.
