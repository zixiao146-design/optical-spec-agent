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
- CI and quality gate parity.
- Release dry-run operations.
- Secrets and token hygiene.
- Maintainer operations checklist.
- Optional open-source solver availability preflight.
- Python-backed solver availability detection for Meep, MPB, and Optiland.
- Adapter maturity model.
- Gmsh optional validation pilot, now with Level 3 optional manual validation
  evidence for one project/adapter `.geo` artifact path.
- Gmsh Level 3 optional manual validation evidence is recorded but remains
  narrow and non-default.
- Meep optional validation pilot, now with Level 3 optional manual validation
  evidence for one tiny project-owned PyMeep validation path.
- Meep Level 3 optional manual validation evidence is recorded but remains
  narrow and non-default.
- MPB optional validation pilot, now with Level 3 optional manual validation
  evidence for one tiny project-owned MPB/PyMeep validation path.
- MPB Level 3 optional manual validation evidence is recorded but remains
  narrow and non-default. MPB CLI is not required.
- Manual solver validation report template.
- Pytest marker policy for optional/manual validation.
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
- Gmsh Level 3 evidence is narrow and optional; it is not production-grade
  physical validation, not a formal convergence proof, and not a default gate.
- The Gmsh report is not production-grade physical validation.
- Meep Level 3 evidence is narrow and optional; it is not production-grade
  physical validation, not a formal convergence proof, and not a default gate.
- The Meep report is not production-grade physical validation.
- MPB Level 3 evidence is narrow and optional; it is not production-grade
  physical validation, not a formal convergence proof, and not a default gate.
- The MPB report is not production-grade physical validation and does not
  require MPB CLI.
- Open-source solver preflight detects availability only and does not execute
  solvers.
- MPB CLI absence is acceptable when `meep.mpb` imports successfully; ElmerSolver
  remains optional/manual.
- TestPyPI upload not approved/exercised.
- PyPI publication not approved.
- Adapter outputs may still be MVP/scaffold.
- Workflow remains local/synchronous preview.
- v1.0 compatibility freeze not finalized.
- No new GitHub Actions workflow was added during operations readiness because
  existing CI, docs, benchmark, prerelease, and release-dry-run workflows were
  reviewed and documented instead of duplicating automation.

## Recommended Next Decisions

- Continue v1.0 readiness engineering.
- Optionally evaluate TestPyPI upload with explicit approval.
- Do not publish PyPI yet.
- Prepare a `v0.9.0rc5` release draft only when accumulated changes justify
  another public release candidate.
