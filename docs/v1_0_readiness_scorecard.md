# v1.0 Readiness Scorecard

## Current Status

- Current public prerelease: v0.9.0rc5
- Current main release draft: `0.9.0rc6`
- PyPI/TestPyPI: PyPI not published / TestPyPI uploaded for 0.9.0rc6.dev0
- TestPyPI upload approval for 0.9.0rc6: pending
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
- Optiland optional validation pilot, now with Level 3 optional manual
  validation evidence for one tiny project-owned Optiland backend path.
- Optiland Level 3 optional manual validation evidence is recorded but remains
  narrow and non-default.
- Elmer Level-3-ready optional validation path documented with a default
  no-execution script.
- Manual solver validation report template.
- Pytest marker policy for optional/manual validation.
- Open-source-solver-first strategy.
- Proprietary solver non-default policy.
- CLI contract.
- Schema compatibility policy.
- Adapter support matrix.
- Offline examples.
- E2E user journey.
- Public contract freeze approved for the documented surface.
- v1.0 readiness gap audit.
- v0.9.0rc6 development plan.
- v1.0 decision matrix.
- v1.0 public contract freeze checklist.
- v1.0 public contract freeze confirmation package.
- v1.0 public contract freeze status.
- v1.0 contract frozen surface.
- v1.0 contract non-goals.
- v1.0 breaking change policy.
- Publication decision record.
- PyPI publication readiness checklist.
- PyPI post-publication verification plan.
- TestPyPI upload attempt record for 0.9.0rc6.dev0: first local token attempt
  failed with HTTP 403 Forbidden and did not publish PyPI.
- TestPyPI status record for 0.9.0rc6.dev0: Trusted Publishing upload
  completed, clean install from TestPyPI passed, and PyPI remains unpublished.
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
- Optiland Level 3 evidence is narrow and optional; it is not production-grade
  optical validation, not a formal convergence proof, and not a default gate.
- The Optiland report is not production-grade optical validation.
- Open-source solver preflight detects availability only and does not execute
  solvers.
- MPB CLI absence is acceptable when `meep.mpb` imports successfully; ElmerSolver
  remains optional/manual.
- Elmer remains Level 2 pending ElmerSolver installation and explicit opt-in
  manual validation; missing ElmerSolver is non-blocking for default gates, and
  the 2026-05-15 package-manager install attempt is recorded as deferred.
- TestPyPI upload exercised for 0.9.0rc6.dev0 through manual Trusted
  Publishing.
- TestPyPI upload for 0.9.0rc6 is not performed and remains pending.
- PyPI publication not approved.
- PyPI publication readiness checklist records required approval, final version,
  CI, quality gates, build, twine check, metadata review, validation-claim
  review, yanking policy, and post-publication verification before PyPI.
- Publication decision record keeps PyPI publication not granted and prevents
  tag/release creation from being implied by TestPyPI success.
- Adapter outputs may still be MVP/scaffold.
- Workflow remains local/synchronous preview.
- v1.0 public contract freeze is approved for the documented surface.
- PyPI publication remains a hard strategic decision.
- `v1.0.0` final release remains separately gated.
- No new GitHub Actions workflow was added during operations readiness because
  existing CI, docs, benchmark, prerelease, and release-dry-run workflows were
  reviewed and documented instead of duplicating automation.

## Recommended Next Decisions

- Continue v1.0 readiness engineering.
- Use `docs/v1_0_gap_audit.md` to classify blockers and deferred work.
- Use `docs/rc6_development_plan.md` to keep rc6 development scoped.
- Use `docs/v1_0_decision_matrix.md` before TestPyPI, PyPI, Elmer, production
  validation, or public-contract-freeze decisions.
- Use `docs/v1_0_public_contract_freeze_checklist.md` and
  `docs/v1_0_public_contract_freeze_status.md` before changing the frozen
  surface.
- Use `docs/v1_0_public_contract_freeze_confirmation.md`,
  `docs/v1_0_contract_frozen_surface.md`,
  `docs/v1_0_contract_non_goals.md`, and
  `docs/v1_0_breaking_change_policy.md`, and
  `docs/v1_0_public_contract_freeze_status.md` as the approved freeze package.
- Use `docs/publication_decision_record.md` before any TestPyPI/PyPI action.
- Use `docs/pypi_publication_readiness_checklist.md` and
  `docs/pypi_post_publication_verification_plan.md` before any PyPI approval.
- Optionally evaluate TestPyPI upload with explicit approval.
- Do not publish PyPI yet.
- Continue release-draft review for `v0.9.0rc6`; create the tag and GitHub
  prerelease only after explicit maintainer approval and fresh verification.
