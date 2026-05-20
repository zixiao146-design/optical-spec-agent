# MPB Optional Micro-benchmark Decision Packet

## Current status

- MPB micro-benchmark approval: approved for the 2026-05-20 MPB-only run
- MPB execution authorized: yes for the completed 2026-05-20 MPB-only run; no future rerun authorized
- MPB executed: yes, MPB / `meep.mpb` only, on 2026-05-20
- Meep executed in this task: no
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

- MPB may be available through Python import:
  `from meep import mpb`
- MPB CLI is not required if the `meep.mpb` Python path is available.
- Readiness checks are import/path probes only and do not execute MPB.

## Approval phrase

Required explicit phrase:

`I approve running the optional MPB micro-benchmark for optical-spec-agent using OSA_SOLVER_PYTHON=<path>.`

## Opt-in Command Used For Approved Run

DO NOT RUN WITHOUT NEW APPROVAL FOR FUTURE RERUNS:

```bash
OSA_RUN_OPTIONAL_MPB_VALIDATION=1 \
OSA_SOLVER_PYTHON=/opt/homebrew/Caskroom/miniforge/base/envs/osa-solvers/bin/python \
OSA_MPB_VALIDATION_REPORT=/tmp/osa-mpb-micro-benchmark-report.json \
OSA_MPB_OUTPUT_DIR=/tmp/osa-mpb-micro-benchmark-output \
./scripts/run_optional_solver_micro_benchmarks.sh
```

## Expected artifacts

- generated MPB preview script
- MPB result JSON or band summary JSON
- optional manual validation report
- no committed raw generated artifacts unless explicitly approved

## Recorded Evidence

- approval record: `docs/optional_solver_approval_records/mpb_micro_benchmark_approval_2026-05-20.md`
- evidence record: `validation/mpb/mpb_micro_benchmark_2026-05-20.md`
- report path: `/tmp/osa-mpb-micro-benchmark-report.json`
- status: passed
- future MPB rerun authorization: no

## Non-claims

- no production-grade MPB validation
- no production-grade physical validation
- no formal convergence proof
- no optical correctness claim
- no default solver dependency
- no release gate behavior

## Separation from publication/release

- PyPI publication: not approved
- TestPyPI upload: not approved
- tag/release creation: not approved
- `v1.0.0` release: not approved
