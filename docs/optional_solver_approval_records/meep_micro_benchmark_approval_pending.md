# Meep Micro-benchmark Approval Record

- Approval status: pending
- Execution authorized: no
- Solver execution performed: no
- Solver: Meep / PyMeep
- Required environment profile: `osa-solvers`
- Decision packet:
  `docs/optional_solver_approval_records/meep_micro_benchmark_decision_packet.md`
- Required approval phrase:
  `I approve running the optional Meep micro-benchmark for optical-spec-agent using OSA_SOLVER_PYTHON=<path>.`

## Readiness Profile

Meep readiness is environment-specific and requires `OSA_SOLVER_PYTHON`.
The maintainer-local `osa-solvers` profile can be checked without solver
execution:

```bash
OSA_SOLVER_PYTHON=/opt/homebrew/Caskroom/miniforge/base/envs/osa-solvers/bin/python \
OSA_SOLVER_READINESS_PROFILE=osa-solvers \
python scripts/check_optional_solver_readiness.py
```

Import-only readiness may detect both `meep` and `meep.mpb`. This pending Meep
record does not authorize MPB execution, Meep execution, uploads, tags, or releases.

## Command Template

DO NOT RUN WITHOUT APPROVAL:

```bash
OSA_SOLVER_PYTHON=<path> \
OSA_SOLVER_READINESS_PROFILE=osa-solvers \
OSA_MEEP_VALIDATION_REPORT=/tmp/osa-meep-micro-benchmark-report.json \
OSA_MEEP_OUTPUT_DIR=/tmp/osa-meep-micro-benchmark-output \
OSA_RUN_OPTIONAL_MEEP_VALIDATION=1 \
./scripts/run_optional_solver_micro_benchmarks.sh
```

## Expected Artifacts

- `/tmp/osa-meep-micro-benchmark-output/meep_preview.py`
- `/tmp/osa-meep-micro-benchmark-output/meep_validation_result.json`
- `/tmp/osa-meep-micro-benchmark-report.json`

## Cleanup Notes

Review the report, then remove `/tmp/osa-meep-micro-benchmark-output/` and
`/tmp/osa-meep-micro-benchmark-report.json` unless the maintainer explicitly
requests preserving the local evidence.

## Non-claims

- PyPI publication: not approved
- TestPyPI upload: not approved
- Tag or GitHub release creation: not approved
- `v1.0.0` release: not approved
- Production-grade physical validation: not claimed
- Formal convergence proof: not claimed
