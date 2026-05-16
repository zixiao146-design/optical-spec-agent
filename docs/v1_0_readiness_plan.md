# v1.0 Readiness Plan

## Current baseline

- Current public prerelease: `v0.9.0rc6`
- Current main development version: `0.9.0rc7.dev0`
- `v0.9.0rc7` GitHub release has not been created
- `v0.9.0rc7` tag has not been created
- Release URL: https://github.com/zixiao146-design/optical-spec-agent/releases/tag/v0.9.0rc6
- Release verified: yes
- Post-release status: `docs/post_release_status_v0.9.0rc6.md`
- Latest post-release status commit: `cf2fe72`
- PyPI published: no
- TestPyPI uploaded: yes, for `0.9.0rc6.dev0`
- Local Agent API readiness: in progress
- Local Agent API response models: available
- Local Agent API frontend fixtures: `examples/api/`
- Local Agent API handoff docs/scripts: available
- Agent Studio frontend MVP planning: available
- Frontend implementation: not started

## What v0.9.0rc2 already proves

- Clean install with the test extra passed: `python -m pip install -e ".[test]"`.
- Test suite passed at release time: `pytest: 331 passed, 4 warnings`.
- Current main hardening baseline after `40ed807`: `pytest: 332 passed, 4 warnings`.
- Build passed and produced wheel/sdist artifacts.
- `optical-spec --help` passed.
- Release smoke automation exists: `scripts/smoke_release.sh`.
- GitHub pre-release was verified with `draft=false` and `prerelease=true`.

These prove the release-candidate engineering path is reproducible enough for
early adopters. They do not prove physical correctness of generated simulations.

## Remaining limitations

- No PyPI publish has been performed.
- No production-grade physical validation is claimed.
- No formal convergence proof is provided.
- External solvers are not run by default.
- External LLM providers are not required by default.
- Project positioning is open-source-solver-first.
- Proprietary solvers are not default dependencies.
- No proprietary license is required for default tests, smoke, examples, or
  release validation.
- Adapter outputs remain MVP/scaffold unless separately validated.
- Workflow orchestration is a local/synchronous preview.
- The RC is not final `1.0` stability.

## Recommended path through the v0.9.0rc7 development cycle

`v0.9.0rc6` is the current public prerelease. `main` now builds as the
`0.9.0rc7.dev0` development version. The `v0.9.0rc7` tag has not been created,
no GitHub release exists for rc7, and PyPI remains unpublished.
Recommended goals:

- Use `docs/v1_0_gap_audit.md` to classify hard blockers,
  soft blockers, deferred items, and future work.
- Use `docs/release_readiness_v0.9.0rc7.md` to keep rc7 development checks
  explicit.
- Use `docs/v1_0_decision_matrix.md` for TestPyPI, PyPI, Elmer,
  production-validation, and public-contract-freeze decisions.
- Use `docs/v1_0_public_contract_freeze_checklist.md` to make the freeze
  candidate actionable.
- Use `docs/v1_0_public_contract_freeze_confirmation.md`,
  `docs/v1_0_contract_frozen_surface.md`,
  `docs/v1_0_contract_non_goals.md`, and
  `docs/v1_0_breaking_change_policy.md` as the maintainer-facing freeze
  confirmation package. Maintainer confirmation is approved and recorded in
  `docs/v1_0_public_contract_freeze_status.md`.
- Use `docs/publication_decision_record.md` to keep TestPyPI authorization
  explicit, record the successful 0.9.0rc6.dev0 Trusted Publishing upload, and
  keep PyPI not granted.
- Use `docs/pypi_publication_readiness_checklist.md` to keep PyPI publication
  preconditions explicit.
- Use `docs/pypi_post_publication_verification_plan.md` to define the clean
  install, CLI, example, status-doc, and yank/rollback checks required after a
  separately approved PyPI publication.
- Use `docs/v1_0_release_criteria.md`, `docs/v1_0_release_plan.md`,
  `docs/rc_to_v1_0_transition_path.md`, `docs/v1_0_pypi_decision_gate.md`, and
  `docs/v1_0_post_release_verification_plan.md` as the v1.0.0 planning and
  release criteria package.
- Treat `docs/agent_studio_frontend_roadmap.md` as future/Phase 2 planning,
  not as a v1.0.0 release blocker.
- Use `docs/api_agent_contract.md` and `docs/cli_api_parity.md` to keep the
  local Agent API aligned with the CLI and ready for a future Agent Studio
  frontend.
- Use `docs/api_error_model.md` and `examples/api/frontend_fixture_manifest.json`
  to keep API error behavior and frontend fixtures stable.
- Use `docs/api_versioning_policy.md`,
  `docs/api_request_validation_contract.md`, and `docs/api_migration_notes.md`
  to keep API schema versioning and request validation explicit.
- Use `docs/api_local_launch_guide.md`, `docs/frontend_handoff_spec.md`, and
  `docs/api_curl_examples.md` for future frontend developer handoff.
- Use `scripts/smoke_agent_api.sh` and `scripts/check_api_fixtures.py` to keep
  the local API smoke path and frontend fixtures aligned with live TestClient
  responses.
- Use `docs/frontend_mvp_product_spec.md`,
  `docs/frontend_information_architecture.md`,
  `docs/frontend_api_mapping.md`, `docs/frontend_mvp_user_flows.md`,
  `docs/frontend_mvp_acceptance_criteria.md`,
  `docs/frontend_safety_policy.md`, and
  `docs/frontend_mvp_implementation_plan.md` before starting a frontend
  implementation task.
- Keep API defaults local/synchronous/preview-first: no external solver
  execution, no external LLM call, no proprietary solver requirement, and no
  network dependency for documented examples.
- Keep TestPyPI/PyPI gated by explicit approval.
- Keep packaging metadata and wheel install smoke reliable.
- Keep the v1.0 stability gate current.
- Keep one-command quality gates reproducible.
- Stronger adapter golden-output regression tests.
- Better workflow replay and dry-run smoke coverage.
- Clearer CLI quickstart examples for local/no-network usage.
- Stronger release engineering playbook coverage.
- Optional external solver validation path documented, but not made default.
- Open-source solver availability preflight documented and safe by default:
  `scripts/open_solver_validation_preflight.sh`.
- Manual solver validation reports use
  `docs/manual_solver_validation_report_template.md`.
- Optional solver tests follow `docs/pytest_marker_policy.md` and remain
  skipped/manual by default.
- Physical validation status clarified without overclaiming.
- PyPI remains unpublished unless explicitly approved.
- TestPyPI upload and clean-install verification are complete for
  `0.9.0rc6.dev0`; do not re-upload the same version.
- TestPyPI upload for `0.9.0rc6` is not performed and requires separate
  approval.

## Recommended path to v1.0.0

Before `v1.0.0`, maintainers should decide and document:

- Stable public API and CLI contract: `docs/cli_contract.md` and
  `docs/schema_contract.md`.
- Offline examples and fixtures: `examples/README.md`,
  `examples/specs/minimal_nanoparticle.json`,
  `examples/workflows/local_preview_request.json`, and `examples/e2e/`.
- Offline user journey: `docs/offline_user_journey.md` documents the
  validate -> parse -> adapter-list -> workflow-plan path with no network, no
  external solver, no external LLM, and no proprietary solver requirement.
- Adapter family evidence has been expanded with offline golden/evidence
  fixtures for Gmsh, Elmer, MPB, and Optiland. This evidence covers local
  artifact/scaffold generation only; it does not imply production-grade
  physical validation.
- Schema compatibility policy: `docs/schema_compatibility_policy.md`.
- Supported adapters and their stability levels:
  `docs/adapter_support_matrix.md`.
- Open-source-solver-first strategy:
  `docs/open_source_solver_strategy.md`.
- Proprietary solver boundary:
  `docs/proprietary_solver_policy.md`.
- v1.0 compatibility policy:
  `docs/v1_0_compatibility_policy.md`.
- v1.0 readiness gap audit:
  `docs/v1_0_gap_audit.md`.
- v0.9.0rc7 development readiness:
  `docs/release_readiness_v0.9.0rc7.md`.
- v1.0 decision matrix:
  `docs/v1_0_decision_matrix.md`.
- v1.0 public contract freeze:
  `docs/v1_0_public_contract_freeze.md`.
- v1.0 public contract freeze checklist:
  `docs/v1_0_public_contract_freeze_checklist.md`.
- v1.0 public contract freeze confirmation:
  `docs/v1_0_public_contract_freeze_confirmation.md`.
- v1.0 public contract freeze status:
  `docs/v1_0_public_contract_freeze_status.md`.
- v1.0 contract frozen surface candidate:
  `docs/v1_0_contract_frozen_surface.md`.
- v1.0 contract non-goals:
  `docs/v1_0_contract_non_goals.md`.
- v1.0 breaking change policy:
  `docs/v1_0_breaking_change_policy.md`.
- Publication decision record:
  `docs/publication_decision_record.md`.
- PyPI publication readiness checklist:
  `docs/pypi_publication_readiness_checklist.md`.
- PyPI post-publication verification plan:
  `docs/pypi_post_publication_verification_plan.md`.
- v1.0.0 release criteria:
  `docs/v1_0_release_criteria.md`.
- v1.0.0 release plan:
  `docs/v1_0_release_plan.md`.
- RC to v1.0.0 transition path:
  `docs/rc_to_v1_0_transition_path.md`.
- v1.0 PyPI decision gate:
  `docs/v1_0_pypi_decision_gate.md`.
- v1.0.0 post-release verification plan:
  `docs/v1_0_post_release_verification_plan.md`.
- Agent Studio frontend roadmap:
  `docs/agent_studio_frontend_roadmap.md`; this is future/Phase 2 planning
  and not a v1.0.0 blocker.
- Public contract manifest and change checklist:
  `docs/public_contract_manifest.json` and
  `docs/public_contract_change_checklist.md`.
- Validation evidence manifest:
  `docs/validation_evidence_manifest.md`.
- Optional open-source solver validation plan:
  `docs/open_source_solver_validation_plan.md`.
- Optional open-source solver validation harness:
  `docs/open_solver_validation_harness.md`.
- Adapter maturity model:
  `docs/adapter_maturity_model.md`.
- Gmsh optional validation pilot:
  `docs/gmsh_optional_validation_pilot.md`; it is guarded by
  `OSA_RUN_OPTIONAL_GMSH_VALIDATION=1` and is not enabled by default.
- Gmsh Level 3 readiness:
  `docs/gmsh_level3_readiness.md` and
  `validation/gmsh/gmsh_validation_pilot_2026-05-14.md` record a narrow
  optional manual validation of the project/adapter `.geo` artifact path. This
  does not make Gmsh a default dependency and does not support
  production-grade physical validation or a formal convergence proof.
- Meep optional validation pilot:
  `docs/meep_optional_validation_pilot.md`; it is guarded by
  `OSA_RUN_OPTIONAL_MEEP_VALIDATION=1` and is not enabled by default.
- Meep Level 3 readiness:
  `docs/meep_level3_readiness.md` and
  `validation/meep/meep_validation_pilot_2026-05-14.md` record a narrow
  optional manual validation of a tiny project-owned PyMeep path generated from
  an adapter preview artifact. This does not make Meep a default dependency and
  does not support production-grade physical validation or a formal convergence
  proof.
- MPB optional validation pilot:
  `docs/mpb_optional_validation_pilot.md`; it is guarded by
  `OSA_RUN_OPTIONAL_MPB_VALIDATION=1` and is not enabled by default.
- MPB Level 3 readiness:
  `docs/mpb_level3_readiness.md` and
  `validation/mpb/mpb_validation_pilot_2026-05-14.md` record a narrow optional
  manual validation of a tiny project-owned MPB/PyMeep path generated from an
  adapter preview artifact. This does not make MPB a default dependency, does
  not require MPB CLI, and does not support production-grade physical validation
  or a formal convergence proof.
- Optiland optional validation pilot:
  `docs/optiland_optional_validation_pilot.md`; it is guarded by
  `OSA_RUN_OPTIONAL_OPTILAND_VALIDATION=1` and is not enabled by default.
- Optiland Level 3 readiness:
  `docs/optiland_level3_readiness.md` and
  `validation/optiland/optiland_validation_pilot_2026-05-14.md` record a narrow
  optional manual validation of a tiny project-owned Optiland backend path
  generated from an adapter preview artifact. This does not make Optiland a
  default dependency and does not support production-grade optical validation or
  a formal convergence proof.
- Elmer optional validation pilot:
  `docs/elmer_optional_validation_pilot.md`; it is guarded by
  `OSA_RUN_OPTIONAL_ELMER_VALIDATION=1` and is not enabled by default.
- Elmer Level 3 readiness:
  `docs/elmer_level3_readiness.md` and
  `scripts/run_optional_elmer_validation.sh` prepare a default no-execution
  availability check. Elmer remains Level 2 until ElmerSolver is installed and
  an explicit opt-in manual validation report is recorded. The 2026-05-15
  conda-forge/Homebrew install attempt is recorded as deferred in
  `validation/elmer/elmer_install_deferred_2026-05-15.md`.
- Manual solver validation report template:
  `docs/manual_solver_validation_report_template.md`.
- Pytest marker policy for optional solver validation:
  `docs/pytest_marker_policy.md`.
- Examples manifest:
  `examples/examples_manifest.json`.
- Error model:
  `docs/error_model.md`.
- Pre-v1 migration notes:
  `docs/migration_notes_pre_v1.md`.
- Compatibility evidence tests for CLI, schema, adapter registry, workflow
  preview, documented examples, and failure modes.
- Public contract manifest tests to prevent CLI/schema/adapter/workflow/examples
  drift before v1.0.
- Offline user journey regression tests for documented e2e commands.
- Workflow preview boundaries: `docs/workflow_preview_contract.md`.
- Unsupported assumptions, validation limits, and non-goals:
  `docs/validation_boundary.md`.
- Reproducible release procedure and rollback policy.
- Production-grade validation plan, or an explicit non-production disclaimer.
- Versioning policy for previews, RCs, and final releases.
- PyPI publication decision: `docs/pypi_publication_decision.md`.
- PyPI publication readiness checklist:
  `docs/pypi_publication_readiness_checklist.md`.
- PyPI post-publication verification plan:
  `docs/pypi_post_publication_verification_plan.md`.
- Packaging publication gate: `docs/packaging_gate.md`.
- Validation gate for RC/v1.0 readiness: `docs/validation_gate.md`.
- Optional external solver policy: `docs/external_solver_policy.md`.
- Optional external LLM policy: `docs/external_llm_policy.md`.
- Security and token-handling guidance for release operations.

## Immediate engineering priorities

### P0

- Release closure verification. Completed for `v0.9.0rc2`.
- Tag sync verification. Completed locally for `v0.9.0rc2`; repeat before any new tag.
- Release status visibility. Completed through post-release status docs.
- Smoke script reliability. Strengthened after `40ed807`.
- Public contract docs and regression tests. Added in current main.
- Packaging and validation gates. Added in current main.
- Optional external solver/LLM policy docs. Added in current main.
- Continue v1.0 readiness engineering from the verified `v0.9.0rc5`
  public prerelease.

### P1

- Additional CLI examples around failure/strict modes.
- Adapter golden-output tests for non-Meep scaffold adapters.
- Workflow replay smoke tests for Meep/no-execute diagnostics.
- Release rollback playbook.
- Expand evidence fixtures across all adapter families.
- Optional/manual external solver validation remains a separate future gate.

### P2

- TestPyPI evaluation only with explicit approval.
- Optional external solver gate.
- Expanded physical validation examples.

## Explicit non-goals

- Do not publish PyPI yet.
- Do not re-upload the existing `0.9.0rc6.dev0` TestPyPI artifacts.
- Do not upload `0.9.0rc7.dev0` to TestPyPI without explicit approval.
- Do not move `v0.9.0rc1`, `v0.9.0rc2`, `v0.9.0rc3`, `v0.9.0rc4`,
  `v0.9.0rc5`, or `v0.9.0rc6` tags.
- Do not create the `v0.9.0rc7` tag until future release-draft checks and
  maintainer approval.
- Do not treat `0.9.0rc7.dev0` as a public release; a future `v0.9.0rc7`
  release candidate requires tag and
  GitHub prerelease creation are explicitly approved and completed.
- Do not claim production-grade physical validation.
- Do not claim formal convergence proof.
- Do not require external solver or external LLM by default.
