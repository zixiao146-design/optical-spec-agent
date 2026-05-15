# v0.9.0rc5 Release Draft Readiness

## Baseline

- Current public prerelease: v0.9.0rc4
- v0.9.0rc4 release URL: https://github.com/zixiao146-design/optical-spec-agent/releases/tag/v0.9.0rc4
- v0.9.0rc4 target commit: 497acc37a021db1af24629a77abab16f1d0f62f8
- Current main release draft: v0.9.0rc5
- v0.9.0rc5 tag: not created
- GitHub release: not created
- PyPI/TestPyPI: not published / not uploaded
- TestPyPI upload approval: pending
- Upload command authorized: no
- PyPI publication approval: not granted

## Included Post-rc4 Hardening

- One-command quality gates in `scripts/run_quality_gates.sh`.
- v1.0 operations readiness docs for CI parity, release dry-runs, secrets hygiene, and maintainer operations.
- Python-aware solver preflight that detects CLI and Python-backed availability without solver execution.
- Adapter maturity model separating local artifact evidence, optional manual validation, and production-grade validation.
- Gmsh Level 3 optional manual validation evidence.
- Meep Level 3 optional manual validation evidence.
- MPB Level 3 optional manual validation evidence.
- Optiland Level 3 optional manual validation evidence.
- Elmer Level-3-ready documentation and install-deferred record:
  `validation/elmer/elmer_install_deferred_2026-05-15.md`.
- Open-source-solver-first strategy and proprietary-solver non-default policy.
- Public contract freeze candidate and manifest.
- Offline user journey and examples manifest.
- TestPyPI no-upload preflight.

## Adapter Validation Boundary

- Gmsh, Meep, MPB, and Optiland have narrow optional manual validation evidence.
- Elmer remains Level 2 + Level-3-ready, pending ElmerSolver availability and explicit opt-in validation.
- No external solver is required by default.
- No external LLM is required by default.
- No proprietary solver is required by default.
- No production-grade physical validation is claimed.
- No formal convergence proof is claimed.

## Required Checks Before Tag Creation

- `git status` clean.
- `project.version == 0.9.0rc5`.
- `optical_spec_agent.__version__ == 0.9.0rc5`.
- `v0.9.0rc5` tag absent locally and remotely.
- TestPyPI no-upload preflight passed.
- Quality gates passed.
- `scripts/smoke_release.sh` passed.
- Wheel smoke passed.
- `pytest` passed.
- `python -m build` passed.
- `make check` passed.
- CLI examples passed.
- E2E example passed.
- Dist filenames contain `0.9.0rc5`.
- Release draft notes exist.
- Release notes exist.
- No PyPI/TestPyPI upload.

## Current Verification

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

## Next Step

After maintainer approval:

- Create an annotated `v0.9.0rc5` tag.
- Push the tag.
- Create a GitHub prerelease.
- Verify `draft=false` and `prerelease=true`.
- Add `docs/post_release_status_v0.9.0rc5.md`.
- Do not publish PyPI or upload TestPyPI unless separately approved.

## Non-goals

- Do not publish PyPI now.
- Do not upload TestPyPI now.
- Do not create `v0.9.0rc5` tag now.
- Do not create a GitHub release now.
- Do not claim production-grade physical validation.
- Do not claim formal convergence proof.
- Do not require external solver or external LLM by default.
- Do not require proprietary solver by default.
