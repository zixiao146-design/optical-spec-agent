# Release Notes: v0.9.0rc3

Draft notes for the `v0.9.0rc3` release candidate. This file records the
candidate contents for release-readiness tracking; it does not mean the tag or
GitHub pre-release has been created.

## Summary

`v0.9.0rc3` is a hardening release candidate after the verified `v0.9.0rc2`
pre-release. It prepares the project for the next public RC by incorporating
v1.0 readiness contract work, validation and packaging gates, and wheel-install
smoke coverage.

## Changes Since v0.9.0rc2

- Added and stabilized v1.0 readiness contract docs and tests.
- Added CLI contract coverage.
- Added schema/API contract coverage.
- Added adapter support matrix coverage.
- Added workflow preview contract coverage.
- Added validation boundary documentation.
- Added packaging gate and validation gate documentation.
- Added PyPI/TestPyPI decision-gate documentation.
- Added optional external solver and external LLM policy docs.
- Added optional wheel install smoke verification to `scripts/smoke_release.sh`.
- Moved `main` from `0.9.0rc3.dev0` to `0.9.0rc3` release-draft state.

## Verification

- `scripts/smoke_release.sh`: passed.
- Wheel install smoke: passed.
- `pytest`: 357 passed, 4 warnings.
- `python -m build`: passed.
- `make check`: passed.
- Offline CLI examples passed.

## Known Limitations

- No PyPI publish.
- No TestPyPI upload.
- No production-grade physical validation.
- No formal convergence proof.
- External solvers are not run by default.
- External LLM providers are not required by default.
- Adapter outputs may still be MVP/scaffold unless explicitly validated.
- Workflow orchestration is a local/synchronous preview.
- This release candidate is not final `1.0` stability.

## Publication Status

- `v0.9.0rc3` tag: not created.
- GitHub pre-release: not created.
- PyPI/TestPyPI: not published / not uploaded.
