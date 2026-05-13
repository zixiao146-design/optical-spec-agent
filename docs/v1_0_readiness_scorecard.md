# v1.0 Readiness Scorecard

## Current Status

- Current public prerelease: v0.9.0rc4
- Current main development version: 0.9.0rc5.dev0
- PyPI/TestPyPI: not published / not uploaded
- TestPyPI upload approval: pending
- v1.0.0 not released

## Ready / Strong Areas

- Release engineering.
- GitHub prerelease process.
- `smoke_release.sh`.
- TestPyPI no-upload preflight.
- Quality gates.
- Open-source-solver-first strategy.
- Proprietary solver non-default policy.
- CLI contract.
- Schema compatibility policy.
- Adapter support matrix.
- Offline examples.
- E2E user journey.
- Public contract freeze candidate.
- Examples manifest.
- Validation evidence manifest.
- Package build and wheel install.

## Still Not v1.0-ready

- No production-grade physical validation.
- No formal convergence proof.
- No solver-backed validation by default.
- TestPyPI upload not approved/exercised.
- PyPI publication not approved.
- Adapter outputs may still be MVP/scaffold.
- Workflow remains local/synchronous preview.
- v1.0 compatibility freeze not finalized.
- Optional no-upload GitHub Actions quality gate workflow was not added in this
  sprint because the repository already has multiple CI/release-dry-run
  workflows; keep that as a future consolidation task.

## Recommended Next Decisions

- Continue v1.0 readiness engineering.
- Optionally evaluate TestPyPI upload with explicit approval.
- Do not publish PyPI yet.
- Prepare a `v0.9.0rc5` release draft only when accumulated changes justify
  another public release candidate.
