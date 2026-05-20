# Elmer Micro-benchmark Deferred Record

- Approval status: deferred
- Execution authorized: no
- Solver execution performed: no
- Solver: Elmer / ElmerSolver
- Required environment profile: `deferred-elmer`
- Required approval phrase:
  `I approve running the optional Elmer micro-benchmark for optical-spec-agent.`

## Deferred Status

ElmerSolver is unavailable in the default readiness profile and a maintainable install route
is still required before any optional Elmer execution can be considered. Elmer
remains Level 2 + Level-3-ready; it is not Level 3.

## Command Template

DO NOT RUN WITHOUT APPROVAL:

```bash
OSA_RUN_OPTIONAL_ELMER_VALIDATION=1 ./scripts/run_optional_solver_micro_benchmarks.sh
```

## Expected Artifacts If A Future Approval Exists

- `/tmp/osa-elmer-validation/case.sif`
- `/tmp/osa-elmer-validation/elmer_validation_report.json`

## Cleanup Notes

Deferred until the install route and explicit approval are both available.

## Non-claims

- PyPI publication: not approved
- TestPyPI upload: not approved
- Tag or GitHub release creation: not approved
- `v1.0.0` release: not approved
- Production-grade physical validation: not claimed
- Formal convergence proof: not claimed
- Elmer Level 3 validation: not claimed
