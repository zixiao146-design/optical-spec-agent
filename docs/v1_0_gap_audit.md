# v1.0 Readiness Gap Audit

## Current baseline

- Current public prerelease: v0.9.0rc8
- Current main development version: 0.9.0rc9.dev0
- v0.9.0rc9 tag: not created
- PyPI: not published
- TestPyPI: uploaded for 0.9.0rc6.dev0
- TestPyPI upload for 0.9.0rc9.dev0: not performed
- TestPyPI upload approval for 0.9.0rc9.dev0: pending
- PyPI publication approval: not granted

## Strong areas

- Release engineering.
- Annotated tag / GitHub prerelease process.
- Post-release status process.
- Quality gates.
- TestPyPI no-upload preflight.
- TestPyPI Trusted Publishing upload and clean install verification for
  0.9.0rc6.dev0, plus rc6 release draft preparation.
- Wheel install smoke.
- CLI examples.
- Offline user journey.
- Examples manifest.
- Public contract manifest.
- v1.0 public contract freeze checklist.
- v1.0 public contract freeze confirmation package, now maintainer-approved.
- v1.0 public contract freeze status record.
- v1.0 contract frozen surface.
- v1.0 contract non-goals.
- v1.0 breaking change policy.
- Publication decision record.
- v1.0.0 release criteria.
- v1.0.0 release plan.
- RC to v1.0.0 transition path.
- v1.0 PyPI decision gate.
- v1.0.0 post-release verification plan.
- Agent Studio frontend roadmap as future/Phase 2 planning.
- Open-source-solver-first strategy.
- Proprietary solver non-default policy.
- Adapter maturity evidence for Gmsh / Meep / MPB / Optiland.
- Python-aware solver preflight.

## Remaining gaps

- Elmer Level 3 validation deferred.
- TestPyPI upload completed for 0.9.0rc6.dev0 via Trusted Publishing and is
  recorded in `docs/testpypi_status_v0.9.0rc6.dev0.md`.
- The earlier local token-based TestPyPI upload attempt failed with HTTP 403
  Forbidden and remains recorded in
  `docs/testpypi_upload_attempt_v0.9.0rc6.dev0.md`.
- PyPI publication not approved.
- v1.0 public contract freeze is approved and recorded in
  `docs/v1_0_public_contract_freeze_status.md`.
- `docs/publication_decision_record.md` records that TestPyPI is completed for
  `0.9.0rc6.dev0`; the `0.9.0rc8` upload is not performed and PyPI remains not
  granted.
- `docs/pypi_publication_readiness_checklist.md` exists and keeps PyPI
  publication blocked until explicit maintainer approval, final version choice,
  quality gates, CI, build, twine check, metadata review, validation-claim
  review, yanking-policy review, and post-publication verification planning are
  complete.
- `docs/pypi_post_publication_verification_plan.md` exists for clean PyPI
  install, version, CLI, example, status-doc, and yank/rollback checks after a
  separately approved publication.
- Production-grade physical validation not claimed.
- Formal convergence proof not claimed.
- Workflow remains local/synchronous preview.
- Adapter outputs may still be MVP/scaffold unless explicitly validated.
- API/frontend Agent Studio planning is documented as future/Phase 2 work, not
  a v1.0 blocker.

## Blocker classification

| Item | Classification | Rationale | Next action |
|---|---|---|---|
| PyPI decision | Hard blocker for v1.0 | v1.0 distribution must have an explicit publication decision, whether PyPI, GitHub-only, or delayed. | Record an explicit maintainer decision before v1.0. |
| TestPyPI upload | Satisfied for 0.9.0rc6.dev0; future decision for any new version | TestPyPI is not required for GitHub-only prereleases, but it becomes a release confidence gate if PyPI publication is planned. The 0.9.0rc6.dev0 upload and clean install verification are complete. | Do not re-upload the same version; decide future uploads per candidate. |
| Elmer Level 3 | Deferred/non-blocker | Elmer remains Level 2 + Level-3-ready; missing ElmerSolver is documented and non-blocking for default gates. | Revisit only when a maintainable install route exists. |
| Production-grade physical validation | Deferred/non-blocker unless v1.0 claims production-grade validation | The project does not claim production-grade physical validation. | Keep claims conservative or define a separate validation program. |
| Formal convergence proof | Deferred/non-blocker unless explicitly claimed | The project does not claim a formal convergence proof. | Keep as a non-goal unless requirements change. |
| Public contract freeze | Satisfied for documented surface | CLI, schema, adapter, workflow, validation, and publication boundaries are frozen or explicitly scoped. | Keep `docs/v1_0_public_contract_freeze_status.md` and manifest checks current. |
| v1.0.0 release approval | Hard blocker | v1.0.0 requires a separate explicit maintainer approval. | Use `docs/v1_0_release_criteria.md` and `docs/v1_0_release_plan.md`. |
| Quality gates | Already satisfied, must remain passing | Local quality gates, smoke, build, docs, and CLI checks are established. | Re-run before each RC or v1.0 transition. |
| Workflow preview | Future work unless final v1.0 claims expand | Workflow orchestration remains local/synchronous preview. | Keep scope clear or define future automation. |
| API/frontend Agent Studio | Future work | Roadmap exists, but frontend/API Studio is not part of v1.0.0 release criteria. | Revisit after backend/API contract readiness. |

## Recommended v1.0 path

- Keep the approved public contract freeze current.
- Use `docs/v1_0_public_contract_freeze_checklist.md` as the executable
  freeze checklist.
- Use `docs/v1_0_public_contract_freeze_confirmation.md`,
  `docs/v1_0_contract_frozen_surface.md`,
  `docs/v1_0_contract_non_goals.md`, and
  `docs/v1_0_breaking_change_policy.md`, and
  `docs/v1_0_public_contract_freeze_status.md` as the approved freeze package.
- Keep production claims conservative.
- Use `docs/testpypi_status_v0.9.0rc6.dev0.md` as the current TestPyPI
  verification record.
- Decide PyPI publication explicitly through `docs/publication_decision_record.md`.
- Use `docs/pypi_publication_readiness_checklist.md` and
  `docs/pypi_post_publication_verification_plan.md` before any PyPI approval.
- Use `docs/v1_0_release_criteria.md`, `docs/v1_0_release_plan.md`,
  `docs/rc_to_v1_0_transition_path.md`, `docs/v1_0_pypi_decision_gate.md`, and
  `docs/v1_0_post_release_verification_plan.md` before any v1.0.0 release
  decision.
- Keep `docs/agent_studio_frontend_roadmap.md` as a future/Phase 2 roadmap,
  not a release blocker.
- Keep Elmer deferred unless a maintainable install route appears.
- Prepare v0.9.0rc6 only if new hardening justifies another release candidate.
