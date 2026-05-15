# v0.9.0rc5 Release Notes

## Summary

v0.9.0rc5 is a release draft for the fifth v0.9.0 release candidate. It
packages post-v0.9.0rc4 v1.0 readiness hardening around operations, quality
gates, adapter maturity, optional open-source solver validation, and release
governance.

## Highlights

- Added repeatable local quality gates.
- Added v1.0 operations readiness docs for CI parity, release dry-runs, secrets
  hygiene, and maintainer operations.
- Improved open-source solver preflight to detect CLI and Python-backed solver
  availability without executing solvers.
- Added adapter maturity model and evidence tracking.
- Added offline user journey and public contract evidence.
- Kept PyPI/TestPyPI publication gated by explicit approval.

## Adapter Maturity Changes

- Gmsh: Level 3 optional manual validation evidence recorded.
- Meep: Level 3 optional manual validation evidence recorded.
- MPB: Level 3 optional manual validation evidence recorded; MPB CLI is not
  required.
- Optiland: Level 3 optional manual backend validation evidence recorded.
- Elmer: Level 2 + Level-3-ready; Elmer install is deferred because ElmerSolver
  is not currently available through the checked local package-manager routes.

## Optional Validation Evidence

- `validation/gmsh/gmsh_validation_pilot_2026-05-14.md`
- `validation/meep/meep_validation_pilot_2026-05-14.md`
- `validation/mpb/mpb_validation_pilot_2026-05-14.md`
- `validation/optiland/optiland_validation_pilot_2026-05-14.md`

These reports are narrow optional manual validation evidence only. They do not
make external solvers default dependencies and do not support production-grade
physical validation or a formal convergence proof.

## Elmer Deferred Status

Elmer remains Level 2 + Level-3-ready. The readiness path and default
no-execution script exist, but no completed Elmer manual validation report is
recorded. The deferred install record is:

- `validation/elmer/elmer_install_deferred_2026-05-15.md`

## Verification

- Quality gates: passed.
- TestPyPI no-upload preflight: passed.
- Normal smoke: passed.
- Wheel smoke: passed.
- `pytest`: 475 passed, 4 warnings.
- `python -m build`: passed.
- `make check`: passed.
- CLI examples: passed.
- E2E example: passed.
- Dist files:
  - `optical_spec_agent-0.9.0rc5-py3-none-any.whl`
  - `optical_spec_agent-0.9.0rc5.tar.gz`

## Scope Limitations

- No PyPI publish.
- No TestPyPI upload.
- No production-grade physical validation.
- No formal convergence proof.
- External solvers are not run by default.
- External LLM is not required by default.
- Proprietary solvers are not required by default.
- Elmer Level 3 validation is deferred.
- Workflow remains a local/synchronous preview.
- This release candidate is not final 1.0 stability.

## PyPI/TestPyPI Status

- PyPI: not published.
- TestPyPI: not uploaded.
- TestPyPI upload approval: pending.
- Upload command authorized: no.
- PyPI publication approval: not granted.

## Tag/Release Note

The `v0.9.0rc5` tag and GitHub prerelease have not been created yet. They should
be created only after explicit maintainer approval.
