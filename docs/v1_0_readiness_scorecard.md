# v1.0 Readiness Scorecard

## Current Status

- Current public prerelease: v0.9.0rc6
- Current main development version: `0.9.0rc7.dev0`
- PyPI/TestPyPI: PyPI not published / TestPyPI uploaded for 0.9.0rc6.dev0
- TestPyPI upload approval for 0.9.0rc7.dev0: pending
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
- v0.9.0rc7 development readiness.
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
- v1.0.0 release criteria.
- v1.0.0 release plan.
- RC to v1.0.0 transition path.
- v1.0 PyPI decision gate.
- v1.0.0 post-release verification plan.
- Agent Studio frontend roadmap as future/Phase 2 planning, not a v1.0.0
  blocker.
- Local Agent API readiness surface for health/version, adapters, schema,
  parse, validate, workflow-plan, adapter-preview, validation evidence, and
  readiness/status.
- Local Agent API response models and stable error model.
- Local Agent API `api_contract_version` 0.1, request validation contract, and
  API migration notes.
- Frontend fixture examples under `examples/api/`.
- Local API launch guide, frontend handoff spec, and curl examples.
- Local API smoke script and fixture consistency script.
- Agent Studio frontend MVP planning docs.
- Agent Studio frontend MVP implementation under `frontend/`.
- Agent Studio frontend MVP runbook.
- CLI/API parity documentation for future Agent Studio integration.
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
- TestPyPI upload for 0.9.0rc7.dev0 is not performed and remains pending.
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
- v1.0.0 release criteria and release plan are documented, but no v1.0.0 tag
  or GitHub release has been created.
- API/frontend Agent Studio is local MVP work and not a v1.0.0 blocker.
- Local Agent API readiness is in progress; the frontend MVP is implemented
  locally, but API/frontend readiness is not a v1.0 blocker unless maintainers
  choose to gate on it.
- API fixture readiness is not a PyPI publication trigger and does not change
  the current package version or release status.
- The Local Agent API remains a frontend-readiness / candidate API and is not
  yet a separately frozen v1.0 API contract.
- No new GitHub Actions workflow was added during operations readiness because
  existing CI, docs, benchmark, prerelease, and release-dry-run workflows were
  reviewed and documented instead of duplicating automation.
- Material Library, Example Gallery, Optical Design Examples, and Agent Trace
  Timeline are preview-first Agent Studio capabilities. Scorecard status remains
  conservative: no production-grade physical validation claim, no formal
  convergence proof claim, Elmer Level 3 deferred, PyPI unpublished, and no
  tag/release action for `v0.9.0rc7` or `v1.0.0`.
- Backend evidence review decision is recorded in
  `docs/backend_evidence_review_decision.md`: backend evidence is sufficient to
  prepare a `v0.9.0rc7` release draft, but `v0.9.0rc7` tag creation, GitHub
  release creation, PyPI publication, TestPyPI upload, and `v1.0.0` release are
  not approved.

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
- Use `docs/v1_0_release_criteria.md`, `docs/v1_0_release_plan.md`,
  `docs/rc_to_v1_0_transition_path.md`, `docs/v1_0_pypi_decision_gate.md`,
  `docs/v1_0_post_release_verification_plan.md`, and
  `docs/agent_studio_frontend_roadmap.md` before any v1.0.0 release planning
  decision.
- Use `docs/api_agent_contract.md` and `docs/cli_api_parity.md` before any
  frontend MVP planning decision.
- Use `docs/api_error_model.md` and `examples/api/` before building frontend
  mock states.
- Use `docs/api_versioning_policy.md`,
  `docs/api_request_validation_contract.md`, and `docs/api_migration_notes.md`
  before changing API request or response shapes.
- Use `docs/api_local_launch_guide.md`, `docs/frontend_handoff_spec.md`,
  `docs/api_curl_examples.md`, `scripts/smoke_agent_api.sh`, and
  `scripts/check_api_fixtures.py` before starting frontend MVP planning.
- Use `docs/frontend_mvp_product_spec.md`,
  `docs/frontend_information_architecture.md`,
  `docs/frontend_api_mapping.md`, `docs/frontend_mvp_user_flows.md`,
  `docs/frontend_mvp_acceptance_criteria.md`,
  `docs/frontend_safety_policy.md`, and
  `docs/frontend_mvp_implementation_plan.md` to keep frontend MVP scope
  bounded.
- Use `docs/frontend_mvp_runbook.md` before running or hardening the frontend
  MVP.
- Use `docs/frontend_mvp_qa_checklist.md` and `scripts/smoke_frontend_mvp.sh`
  before demoing or extending the frontend MVP.
- Use `docs/frontend_visual_smoke_plan.md`,
  `docs/frontend_visual_smoke_runbook.md`, and
  `scripts/smoke_frontend_visual.sh` for optional/manual Playwright checks of
  Dashboard, Spec Input, Adapter Matrix, Workflow Plan, Artifact Preview,
  Validation Evidence, and System Status.
- Optionally evaluate TestPyPI upload with explicit approval.
- Do not publish PyPI yet.
- Prepare a `v0.9.0rc7` release draft from the backend evidence decision, while
  keeping tag/release/PyPI approval separate.
- Continue `v0.9.0rc7.dev0` development; create any future `v0.9.0rc7` tag and
  GitHub prerelease only after explicit maintainer approval and fresh verification.
