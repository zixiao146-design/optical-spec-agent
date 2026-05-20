# MPB Optional Micro-benchmark Approval - 2026-05-20

- Approval status: approved for this MPB run
- Solver: MPB / `meep.mpb`
- Execution authorized: yes, MPB only
- `OSA_SOLVER_PYTHON`: `/opt/homebrew/Caskroom/miniforge/base/envs/osa-solvers/bin/python`
- Other solvers authorized: no
- Meep benchmark authorized: no
- Gmsh authorized: no
- Optiland authorized: no
- Elmer authorized: no
- PyPI/TestPyPI/tag/release authorized: no

## Approval Phrase

`I approve running the optional MPB micro-benchmark for optical-spec-agent using OSA_SOLVER_PYTHON=/opt/homebrew/Caskroom/miniforge/base/envs/osa-solvers/bin/python.`

## Expected Command

```bash
OSA_RUN_OPTIONAL_MPB_VALIDATION=1 \
OSA_SOLVER_PYTHON=/opt/homebrew/Caskroom/miniforge/base/envs/osa-solvers/bin/python \
OSA_MPB_VALIDATION_REPORT=/tmp/osa-mpb-micro-benchmark-report.json \
OSA_MPB_OUTPUT_DIR=/tmp/osa-mpb-micro-benchmark-output \
./scripts/run_optional_solver_micro_benchmarks.sh
```

## Expected Artifacts

- `/tmp/osa-mpb-micro-benchmark-output/mpb_preview.py`
- `/tmp/osa-mpb-micro-benchmark-output/mpb_minimal_validation.py`
- `/tmp/osa-mpb-micro-benchmark-output/mpb_validation_result.json`
- `/tmp/osa-mpb-micro-benchmark-output/mpb_stdout.log`
- `/tmp/osa-mpb-micro-benchmark-output/mpb_stderr.log`
- `/tmp/osa-mpb-micro-benchmark-report.json`

## Expected Report

- `mpb_executed: true`
- `passed: true` if the local `meep.mpb` smoke path succeeds
- `meep_fdtd_benchmark_executed: false`
- `gmsh_executed: false`
- `optiland_executed: false`
- `elmer_executed: false`
- `production_grade_validation_claimed: false`
- `production_grade_mpb_validation_claimed: false`
- `production_band_structure_validation_claimed: false`
- `formal_convergence_proof_claimed: false`
- `optical_correctness_claimed: false`

## Non-claims

- no production-grade physical validation
- no production-grade MPB validation
- no formal convergence proof
- no optical correctness claim
- no production band-structure validation
- no PyPI/TestPyPI publication approval
- no tag/release creation approval
- no `v1.0.0` release approval

## Cleanup Notes

- Keep raw generated artifacts under `/tmp`.
- Commit only the Markdown evidence summary and manifest/docs/tests updates unless
  the maintainer separately approves committing raw generated artifacts.
- Do not rerun MPB, Meep, Gmsh, Optiland, or Elmer during default verification.
