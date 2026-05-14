# v1.0 Readiness Plan

## Current baseline

- Current public prerelease: `v0.9.0rc4`
- Current main development version: `0.9.0rc5.dev0`
- `v0.9.0rc5` GitHub release has not been created
- `v0.9.0rc5` tag has not been created
- Release URL: https://github.com/zixiao146-design/optical-spec-agent/releases/tag/v0.9.0rc4
- Release verified: yes
- Post-release status: `docs/post_release_status_v0.9.0rc4.md`
- Latest post-release status commit: `d26df1b`
- PyPI published: no
- TestPyPI uploaded: no

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

## Recommended path through 0.9.0rc5.dev0

`0.9.0rc5.dev0` is the current post-rc4 development state. A future
`v0.9.0rc5` release draft should be prepared only when accumulated post-rc4
hardening changes justify another public RC. Recommended goals:

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
- TestPyPI remains not uploaded unless explicitly approved.

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
- v1.0 public contract freeze candidate:
  `docs/v1_0_public_contract_freeze.md`.
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
- Continue v1.0 readiness engineering from `0.9.0rc5.dev0`.

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
- Do not upload TestPyPI yet.
- Do not move `v0.9.0rc1`, `v0.9.0rc2`, `v0.9.0rc3`, or `v0.9.0rc4` tags.
- Do not create the `v0.9.0rc5` tag until final readiness checks and maintainer approval.
- Do not treat `v0.9.0rc5.dev0` as a published release.
- Do not claim production-grade physical validation.
- Do not claim formal convergence proof.
- Do not require external solver or external LLM by default.
