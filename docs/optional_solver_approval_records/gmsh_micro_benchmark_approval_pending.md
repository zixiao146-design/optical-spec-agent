# Gmsh Micro-benchmark Approval Record

- Approval status: pending
- Execution authorized: no
- Solver execution performed: no
- Solver: Gmsh
- Required environment profile: `homebrew-cli` or current PATH with `gmsh`
- Required approval phrase:
  `I approve running the optional Gmsh micro-benchmark for optical-spec-agent.`

## Command Template

DO NOT RUN WITHOUT APPROVAL:

```bash
OSA_RUN_OPTIONAL_GMSH_VALIDATION=1 ./scripts/run_optional_solver_micro_benchmarks.sh
```

## Expected Artifacts

- `/tmp/osa-gmsh-validation/gmsh_preview.geo`
- `/tmp/osa-gmsh-validation/gmsh_preview.msh`
- `/tmp/osa-gmsh-validation/gmsh_validation_report.json`

## Cleanup Notes

Review the report, then remove `/tmp/osa-gmsh-validation/` unless the
maintainer explicitly requests preserving the local evidence.

## Non-claims

- PyPI publication: not approved
- TestPyPI upload: not approved
- Tag or GitHub release creation: not approved
- `v1.0.0` release: not approved
- Production-grade physical validation: not claimed
- Formal convergence proof: not claimed
