# Meep Optional Micro-benchmark Decision Packet

## Current status

- Meep micro-benchmark approval: approved for the 2026-05-20 Meep-only run
- Meep execution authorized: yes, for the 2026-05-20 Meep-only run only
- Meep executed: yes, passed on 2026-05-20
- Meep review status: accepted as optional manual PyMeep/FDTD smoke evidence
- MPB executed: no
- Gmsh executed in this task: no
- Optiland executed in this task: no
- Elmer executed: no
- PyPI/TestPyPI upload authorized: no
- Tag/release authorized: no

## Required environment profile

- `OSA_SOLVER_PYTHON` is required.
- Recommended local profile:
  `/opt/homebrew/Caskroom/miniforge/base/envs/osa-solvers/bin/python`
- Readiness check command:

```bash
OSA_SOLVER_PYTHON=/opt/homebrew/Caskroom/miniforge/base/envs/osa-solvers/bin/python \
OSA_SOLVER_READINESS_PROFILE=osa-solvers \
python scripts/check_optional_solver_readiness.py
```

The 2026-05-20 import-only profile check detected the `meep` module through the
`osa-solvers` Python profile. It may also detect `meep.mpb`, but MPB remains a
separate solver decision and is not authorized by this Meep packet. Readiness
checks perform import/path detection only. The later approved Meep-only run is
recorded in `validation/meep/meep_micro_benchmark_2026-05-20.md` and reviewed
in `docs/optional_solver_approval_records/meep_micro_benchmark_review_2026-05-20.md`.

## Approval phrase

Required explicit phrase:

`I approve running the optional Meep micro-benchmark for optical-spec-agent using OSA_SOLVER_PYTHON=<path>.`

## Approved opt-in command

The following command was approved only for the 2026-05-20 Meep-only run.
Do not rerun without fresh approval:

```bash
OSA_RUN_OPTIONAL_MEEP_VALIDATION=1 \
OSA_SOLVER_PYTHON=<path> \
OSA_MEEP_VALIDATION_REPORT=/tmp/osa-meep-micro-benchmark-report.json \
OSA_MEEP_OUTPUT_DIR=/tmp/osa-meep-micro-benchmark-output \
./scripts/run_optional_solver_micro_benchmarks.sh
```

## Expected artifacts

- Meep generated preview script
- Meep result JSON
- optional manual validation report
- no committed raw generated artifacts unless explicitly approved

## Non-claims

- no production-grade FDTD validation
- no formal convergence proof
- no optical correctness claim
- no default solver dependency
- no release gate behavior

## Separation from publication/release

- PyPI publication: not approved
- TestPyPI upload: not approved
- tag/release creation: not approved
- `v1.0.0` release: not approved
