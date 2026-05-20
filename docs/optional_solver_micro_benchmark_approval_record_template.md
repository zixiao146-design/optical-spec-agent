# Optional Solver Micro-benchmark Approval Record Template

Use this template before any optional solver-backed micro-benchmark is run.
Filling it out does not approve PyPI/TestPyPI publication, tag creation, GitHub
release creation, or `v1.0.0` release.

## Solver Selected

- Solver:
- Adapter:
- Local environment / version notes:
- Availability check reviewed:

## Required Approval Phrase

The maintainer approval phrase must be:

> I approve running the optional <solver> micro-benchmark for optical-spec-agent.

The phrase must name the selected solver in the actual approval record.

## Explicitly Not Approved

- PyPI publication: not approved.
- TestPyPI upload: not approved.
- Tag or GitHub release creation: not approved.
- `v1.0.0` release: not approved.
- Production-grade physical validation claim: not approved.
- Formal convergence proof claim: not approved.

## Expected Command

Set only the selected solver env var after approval, for example:

```bash
OSA_RUN_OPTIONAL_<SOLVER>_VALIDATION=1 ./scripts/run_optional_solver_micro_benchmarks.sh
```

Do not set unrelated opt-in env vars.

## Expected Output

- A solver-specific report JSON under `/tmp/osa-*-validation/`.
- Any generated solver input/output artifact listed in
  `validation/solver_validation_micro_benchmarks.json`.
- Safety markers showing no upload, no tag, and no release actions.

## Cleanup Notes

- Review and remove temporary `/tmp/osa-*-validation/` files when no longer
  needed.
- Do not commit solver output artifacts by default.
- Missing solver installs are non-blocking for default development.
