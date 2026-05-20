# MPB Micro-benchmark Approval Record

- Approval status: pending
- Execution authorized: no
- Solver execution performed: no
- Solver: MPB through `meep.mpb`
- Required environment profile: `osa-solvers`
- Decision packet: `docs/optional_solver_approval_records/mpb_micro_benchmark_decision_packet.md`
- Requires `OSA_SOLVER_PYTHON`: yes
- Python import path: `from meep import mpb`
- MPB CLI required: no, if the `meep.mpb` Python path is available
- Required approval phrase:
  `I approve running the optional MPB micro-benchmark for optical-spec-agent using OSA_SOLVER_PYTHON=<path>.`

## Command Template

DO NOT RUN WITHOUT APPROVAL:

```bash
OSA_SOLVER_PYTHON=<path> \
OSA_SOLVER_READINESS_PROFILE=osa-solvers \
OSA_RUN_OPTIONAL_MPB_VALIDATION=1 \
OSA_MPB_VALIDATION_REPORT=/tmp/osa-mpb-micro-benchmark-report.json \
OSA_MPB_OUTPUT_DIR=/tmp/osa-mpb-micro-benchmark-output \
./scripts/run_optional_solver_micro_benchmarks.sh
```

## Expected Artifacts

- `/tmp/osa-mpb-micro-benchmark-output/mpb_preview.py`
- `/tmp/osa-mpb-micro-benchmark-output/mpb_validation_result.json`
- `/tmp/osa-mpb-micro-benchmark-output/mpb_band_summary.json` if generated
- `/tmp/osa-mpb-micro-benchmark-report.json`

## Cleanup Notes

Review the report, then remove `/tmp/osa-mpb-validation/` unless the
maintainer explicitly requests preserving the local evidence.

## Non-claims

- PyPI publication: not approved
- TestPyPI upload: not approved
- Tag or GitHub release creation: not approved
- `v1.0.0` release: not approved
- Production-grade MPB validation: not claimed
- Production-grade physical validation: not claimed
- Formal convergence proof: not claimed
- Optical correctness: not claimed
