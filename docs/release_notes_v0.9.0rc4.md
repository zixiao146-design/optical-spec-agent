# v0.9.0rc4 Release Notes

## Summary

`v0.9.0rc4` is a release draft for the fourth `v0.9.0` release candidate. It
packages post-`v0.9.0rc3` v1.0 readiness hardening while keeping PyPI and
TestPyPI unpublished.

Current public prerelease remains `v0.9.0rc3` until `v0.9.0rc4` is tagged and a
GitHub prerelease is created. The `v0.9.0rc4` tag has not been created.

## Highlights

- Open-source-solver-first product strategy.
- Proprietary solvers documented as non-default/export-only future targets.
- Expanded adapter evidence for Meep, Gmsh, Elmer, MPB, and Optiland.
- Offline examples and examples manifest.
- Offline end-to-end user journey.
- Error model and pre-v1 migration notes.
- Validation evidence manifest.
- Optional open-source solver validation plan.
- Public contract freeze candidate and public contract manifest.
- TestPyPI no-upload preflight.
- Packaging and validation gates.
- Wheel install smoke.

## Verification

- `scripts/testpypi_preflight.sh`: passed
- `scripts/smoke_release.sh`: passed
- Wheel install smoke: passed
- `pytest`: 429 passed, 4 warnings
- `python -m build`: passed
- `make check`: passed
- CLI examples: passed
- E2E examples: passed
- Dist files:
  - `optical_spec_agent-0.9.0rc4-py3-none-any.whl`
  - `optical_spec_agent-0.9.0rc4.tar.gz`

## Scope limitations

- No production-grade physical validation.
- No formal convergence proof.
- External solvers are not run by default.
- External LLM is not required by default.
- Proprietary solvers are not required by default.
- Adapter outputs may still be MVP/scaffold unless explicitly validated.
- Workflow is local/synchronous preview.
- RC is not final 1.0 stability.

## PyPI/TestPyPI status

- PyPI: not published
- TestPyPI: not uploaded
- TestPyPI upload approval: pending
- Upload command authorized: no
- PyPI publication approval: not granted

## Tag/release note

- `v0.9.0rc4` tag: not created yet
- GitHub release: not created yet
- This draft does not create tags or releases.
