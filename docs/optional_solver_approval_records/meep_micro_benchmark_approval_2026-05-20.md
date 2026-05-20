# Meep Micro-benchmark Approval Record - 2026-05-20

- Approval status: approved for this Meep run
- Solver: Meep / PyMeep
- Execution authorized: yes, Meep only
- `OSA_SOLVER_PYTHON`: `/opt/homebrew/Caskroom/miniforge/base/envs/osa-solvers/bin/python`
- Other solvers authorized: no
- MPB authorized: no
- Gmsh authorized: no
- Optiland authorized: no
- Elmer authorized: no
- PyPI/TestPyPI/tag/release authorized: no
- Approval phrase:
  `I approve running the optional Meep micro-benchmark for optical-spec-agent using OSA_SOLVER_PYTHON=/opt/homebrew/Caskroom/miniforge/base/envs/osa-solvers/bin/python.`

## Expected Command

```bash
OSA_RUN_OPTIONAL_MEEP_VALIDATION=1 \
OSA_SOLVER_PYTHON=/opt/homebrew/Caskroom/miniforge/base/envs/osa-solvers/bin/python \
OSA_MEEP_VALIDATION_REPORT=/tmp/osa-meep-micro-benchmark-report.json \
OSA_MEEP_OUTPUT_DIR=/tmp/osa-meep-micro-benchmark-output \
./scripts/run_optional_solver_micro_benchmarks.sh
```

## Expected Artifacts

- `/tmp/osa-meep-micro-benchmark-output/meep_preview.py`
- `/tmp/osa-meep-micro-benchmark-output/meep_minimal_validation.py`
- `/tmp/osa-meep-micro-benchmark-output/meep_validation_result.json`
- `/tmp/osa-meep-micro-benchmark-output/meep_stdout.log`
- `/tmp/osa-meep-micro-benchmark-output/meep_stderr.log`
- `/tmp/osa-meep-micro-benchmark-report.json`

## Expected Report

The report should record:

- `meep_executed: true`
- `passed: true` if the run succeeds
- `production_grade_validation_claimed: false`
- `formal_convergence_proof_claimed: false`
- `proprietary_required: false`
- no PyPI/TestPyPI/tag/release actions
- MPB not executed

## Non-claims

- no production-grade physical validation
- no formal convergence proof
- no optical correctness claim
- no production-grade FDTD validation
- no release gate behavior
- no default solver dependency

## Cleanup Notes

Review the report and generated files, then remove
`/tmp/osa-meep-micro-benchmark-output/` and
`/tmp/osa-meep-micro-benchmark-report.json` unless the maintainer explicitly
requests preserving raw local artifacts. Commit only the Markdown evidence
summary and metadata updates unless raw artifacts are separately approved.
