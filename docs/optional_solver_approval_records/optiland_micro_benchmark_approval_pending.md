# Optiland Micro-benchmark Approval Record

- Approval status: pending
- Execution authorized: no
- Solver execution performed: no
- Solver: Optiland
- Required environment profile: `current` or a Python profile where `optiland`
  is importable
- Required approval phrase:
  `I approve running the optional Optiland micro-benchmark for optical-spec-agent.`

## Command Template

DO NOT RUN WITHOUT APPROVAL:

```bash
OSA_RUN_OPTIONAL_OPTILAND_VALIDATION=1 ./scripts/run_optional_solver_micro_benchmarks.sh
```

## Expected Artifacts

- `/tmp/osa-optiland-validation/optiland_preview.py`
- `/tmp/osa-optiland-validation/optiland_validation_result.json`
- `/tmp/osa-optiland-validation/optiland_validation_report.json`

## Cleanup Notes

Review the report, then remove `/tmp/osa-optiland-validation/` unless the
maintainer explicitly requests preserving the local evidence.

## Non-claims

- PyPI publication: not approved
- TestPyPI upload: not approved
- Tag or GitHub release creation: not approved
- `v1.0.0` release: not approved
- Production-grade physical validation: not claimed
- Formal convergence proof: not claimed
