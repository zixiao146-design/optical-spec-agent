# Current Release Readiness

This document describes the current `main` branch. It is not a release tag.

## Current State

- `pyproject.toml` package version on `main`: `0.9.0rc7.dev0`
- Current public prerelease: `v0.9.0rc6`
- Current main development version: `0.9.0rc7.dev0`
- Main branch state: post-v0.9.0rc6 development toward `v0.9.0rc7`
- Product positioning: open-source-solver-first
- `v0.9.0rc6` GitHub prerelease has been created and verified
- `v0.9.0rc7` GitHub release has not been created
- `v0.9.0rc7` tag has not been created
- GitHub release for `v0.9.0rc7`: not created
- Current public GitHub prerelease created: yes (`v0.9.0rc6`)
- Current public prerelease verified: yes
- Post-release status doc: `docs/post_release_status_v0.9.0rc6.md`
- Latest release-status commit: `cf2fe72`
- PyPI published: no
- TestPyPI uploaded: yes, for `0.9.0rc6.dev0`
- TestPyPI upload for `0.9.0rc7.dev0`: not performed
- TestPyPI upload approval record:
  `docs/testpypi_upload_approval_v0.9.0rc6.dev0.md`
- TestPyPI upload approval record for rc7.dev0:
  `docs/testpypi_upload_approval_v0.9.0rc7.dev0.md`
- Latest TestPyPI upload attempt:
  `docs/testpypi_upload_attempt_v0.9.0rc6.dev0.md`
- TestPyPI status:
  `docs/testpypi_status_v0.9.0rc6.dev0.md`
- TestPyPI Trusted Publishing doc:
  `docs/testpypi_trusted_publishing.md`
- TestPyPI Trusted Publishing workflow:
  `.github/workflows/testpypi-trusted-publish.yml` (manual, passed for
  `0.9.0rc6.dev0`)
- TestPyPI upload approval status for 0.9.0rc7.dev0: pending
- TestPyPI upload authorized for rc7.dev0: no
- Upload command authorized for 0.9.0rc7.dev0: no
- Latest TestPyPI upload attempt result: failed with HTTP 403 Forbidden
- TestPyPI Trusted Publishing result: completed
- TestPyPI clean install verification: passed
- PyPI publication approval: not granted
- PyPI publication readiness checklist:
  `docs/pypi_publication_readiness_checklist.md`
- PyPI post-publication verification plan:
  `docs/pypi_post_publication_verification_plan.md`
- v1.0.0 release criteria:
  `docs/v1_0_release_criteria.md`
- v1.0.0 release plan:
  `docs/v1_0_release_plan.md`
- RC to v1.0.0 transition path:
  `docs/rc_to_v1_0_transition_path.md`
- v1.0 PyPI decision gate:
  `docs/v1_0_pypi_decision_gate.md`
- v1.0.0 post-release verification plan:
  `docs/v1_0_post_release_verification_plan.md`
- Agent Studio frontend roadmap:
  `docs/agent_studio_frontend_roadmap.md` (future/Phase 2, not a v1.0.0
  blocker)
- Local Agent API readiness:
  `docs/api_agent_contract.md` and `docs/cli_api_parity.md` (in progress;
  frontend implementation not started)
- Local Agent API error model:
  `docs/api_error_model.md`
- Local Agent API versioning and request validation:
  `docs/api_versioning_policy.md`, `docs/api_request_validation_contract.md`,
  and `docs/api_migration_notes.md`
- Local Agent API frontend fixtures:
  `examples/api/`
- Proprietary solvers are not default dependencies.
- No proprietary license is required for default tests, smoke, examples, or
  release validation.
- v1.0 compatibility policy exists: `docs/v1_0_compatibility_policy.md`
- v1.0 public contract freeze approved:
  `docs/v1_0_public_contract_freeze_status.md`
- Validation evidence manifest exists: `docs/validation_evidence_manifest.md`
- Optional open-source solver validation plan exists:
  `docs/open_source_solver_validation_plan.md`
- Open-source solver validation harness exists:
  `docs/open_solver_validation_harness.md`
- Open-source solver preflight script:
  `scripts/open_solver_validation_preflight.sh`
- Gmsh Level 3 optional manual validation evidence:
  `validation/gmsh/gmsh_validation_pilot_2026-05-14.md`
- Meep Level 3 optional manual validation evidence:
  `validation/meep/meep_validation_pilot_2026-05-14.md`
- MPB Level 3 optional manual validation evidence:
  `validation/mpb/mpb_validation_pilot_2026-05-14.md`
- Optiland Level 3 optional manual validation evidence:
  `validation/optiland/optiland_validation_pilot_2026-05-14.md`
- Elmer Level-3-ready optional validation path:
  `docs/elmer_level3_readiness.md` and `scripts/run_optional_elmer_validation.sh`;
  the 2026-05-15 conda-forge/Homebrew install attempt is deferred.
- Manual solver validation report template:
  `docs/manual_solver_validation_report_template.md`
- Pytest marker policy:
  `docs/pytest_marker_policy.md`
- Examples manifest exists: `examples/examples_manifest.json`
- Main branch capabilities:
  - v0.6 local/manual post-hoc diagnostics
  - v0.7 multi-solver adapter MVP scaffolds
  - v0.8 LLM parser foundation with deterministic mock provider
  - v0.9 synchronous local workflow orchestration foundation

## Capability Matrix

| Area | Main branch status | Release note |
|---|---|---|
| Rule parser | Stable baseline | Default parser |
| Diagnostics | RC preview | Does not run Meep |
| Meep execution harness | Optional local/manual | Meep not required in CI |
| MPB/Gmsh/Elmer/Optiland adapters | RC MVP scaffold generation plus narrow MPB/Gmsh/Optiland Level 3 optional evidence; Elmer Level-3-ready pending actual validation | Do not run external solvers by default |
| LLM parser foundation | RC preview | Mock provider is deterministic |
| Workflow orchestration | RC preview | Local and synchronous |
| Local Agent API | API readiness in progress | Local/synchronous preview only; no solver, LLM, proprietary, or network default |
| API contract version | 0.1 candidate API | Frontend-readiness surface; not separately frozen as v1.0 API |
| Frontend fixtures | API examples ready | `examples/api/`; frontend implementation not started |
| Bilingual README | RC ready | `README.md` links to `README.zh-CN.md`; Chinese README is complete |
| Public contracts | v1.0-readiness foundation | CLI, schema/API, adapter, workflow, validation, and PyPI boundaries documented |

## Quality Gates

Run these before proposing a release:

```bash
pip install -e ".[dev]"
./scripts/run_quality_gates.sh
OSA_SMOKE_VENV=/tmp/osa-smoke-current ./scripts/smoke_release.sh
python -m pytest
python benchmarks/run_benchmark.py --mode key_fields
python benchmarks/run_semantic_benchmark.py
python benchmarks/run_semantic_benchmark.py --report outputs/semantic_benchmark_report.json
python benchmarks/run_llm_benchmark.py --cases benchmarks/llm_cases.json --parser hybrid --llm-provider mock --report outputs/llm_eval_report.json
python benchmarks/run_workflow_benchmark.py --cases benchmarks/workflow_cases.json --output-dir outputs/workflow_benchmark --report outputs/workflow_benchmark_report.json
python scripts/check_cli_surface.py
python scripts/check_docs_consistency.py
python scripts/check_release_readiness.py --report outputs/release_readiness_report.json
python scripts/check_artifact_contracts.py
make check
python -m build
python -m twine check dist/*
```

## Recommended Version Action

Current recommendation: treat `v0.9.0rc6` as the active verified public
prerelease while `main` moves to post-v0.9.0rc6 development toward
`v0.9.0rc7`. The `v0.9.0rc7` tag has not been created, no GitHub release
exists for rc7, and publication remains separately gated. TestPyPI contains
the `0.9.0rc6.dev0` development package via manual Trusted Publishing, but
TestPyPI upload for `0.9.0rc7.dev0` has not been performed; PyPI remains
unpublished.

Current main contract artifacts:

- `docs/cli_contract.md`
- `docs/schema_contract.md`
- `docs/adapter_support_matrix.md`
- `docs/workflow_preview_contract.md`
- `docs/validation_boundary.md`
- `docs/open_source_solver_strategy.md`
- `docs/proprietary_solver_policy.md`
- `docs/v1_0_compatibility_policy.md`
- `docs/v1_0_public_contract_freeze.md`
- `docs/v1_0_public_contract_freeze_confirmation.md`
- `docs/v1_0_public_contract_freeze_status.md`
- `docs/v1_0_contract_frozen_surface.md`
- `docs/v1_0_contract_non_goals.md`
- `docs/v1_0_breaking_change_policy.md`
- `docs/public_contract_manifest.json`
- `docs/public_contract_change_checklist.md`
- `docs/validation_evidence_manifest.md`
- `docs/open_source_solver_validation_plan.md`
- `docs/offline_user_journey.md`
- `docs/error_model.md`
- `docs/migration_notes_pre_v1.md`
- `docs/pypi_publication_decision.md`
- `docs/packaging_gate.md`
- `docs/validation_gate.md`
- `docs/external_solver_policy.md`
- `docs/external_llm_policy.md`
- `docs/release_engineering_playbook.md`
- `docs/v1_0_readiness_plan.md`
- `docs/v1_0_gap_audit.md`
- `docs/release_readiness_v0.9.0rc7.md`
- `docs/rc6_development_plan.md`
- `docs/v1_0_decision_matrix.md`
- `docs/v1_0_public_contract_freeze_checklist.md`
- `docs/publication_decision_record.md`
- `docs/pypi_publication_readiness_checklist.md`
- `docs/pypi_post_publication_verification_plan.md`
- `docs/v1_0_release_criteria.md`
- `docs/v1_0_release_plan.md`
- `docs/rc_to_v1_0_transition_path.md`
- `docs/v1_0_pypi_decision_gate.md`
- `docs/v1_0_post_release_verification_plan.md`
- `docs/agent_studio_frontend_roadmap.md`
- `docs/quality_gates.md`
- `docs/ci_quality_gate_parity.md`
- `docs/release_dry_run_operations.md`
- `docs/secrets_and_token_hygiene.md`
- `docs/v1_0_readiness_scorecard.md`
- `docs/maintainer_decision_log.md`
- `docs/maintainer_operations_checklist.md`
- `docs/README.md`
- `docs/release_readiness_v0.9.0rc6.md`
- `docs/testpypi_dry_run_gate.md`
- `docs/testpypi_status_v0.9.0rc6.dev0.md`
- `docs/v1_0_stability_gate.md`
- `docs/schema_compatibility_policy.md`
- `examples/README.md`
- `examples/e2e/README.md`

Current v1.0 evidence artifacts:

- Offline examples: `examples/specs/minimal_nanoparticle.json`,
  `examples/specs/missing_wavelength_meep_preview.json`, and
  `examples/workflows/local_preview_request.json`.
- Adapter evidence fixtures:
  `tests/fixtures/adapter_golden/meep_missing_wavelength_expected_fragments.txt`.
- Expanded adapter family evidence fixtures:
  `tests/fixtures/adapter_golden/gmsh/`, `tests/fixtures/adapter_golden/elmer/`,
  `tests/fixtures/adapter_golden/mpb/`, and
  `tests/fixtures/adapter_golden/optiland/`.
- Workflow evidence fixtures:
  `tests/fixtures/workflow_preview/local_preview_expected_keys.json`.
- Failure-mode regression: `tests/test_failure_mode_regression.py`.
- Schema compatibility evidence: `docs/schema_compatibility_policy.md` and
  `tests/test_schema_compatibility_policy.py`.
- Workflow-to-adapter planning evidence:
  `tests/test_workflow_adapter_evidence.py`.
- Offline user journey evidence:
  `examples/e2e/`, `docs/offline_user_journey.md`, and
  `tests/test_offline_user_journey.py`.
- Error model and pre-v1 migration evidence:
  `docs/error_model.md`, `docs/migration_notes_pre_v1.md`, and
  `tests/test_error_model.py`.
- Public contract freeze approved evidence:
  `docs/v1_0_public_contract_freeze.md`,
  `docs/public_contract_manifest.json`,
  `docs/public_contract_change_checklist.md`, and
  `tests/test_public_contract_manifest.py`.
- v1.0 gap audit and rc6 planning evidence:
  `docs/v1_0_gap_audit.md`, `docs/rc6_development_plan.md`,
  `docs/v1_0_decision_matrix.md`,
  `docs/v1_0_public_contract_freeze_checklist.md`, and
  `docs/publication_decision_record.md`.
- Optional open-source solver validation harness:
  `scripts/open_solver_validation_preflight.sh`,
  `docs/open_solver_validation_harness.md`,
  `docs/manual_solver_validation_report_template.md`, and
  `docs/pytest_marker_policy.md`.
- Adapter maturity model:
  `docs/adapter_maturity_model.md`.
- Gmsh optional validation pilot:
  `docs/gmsh_optional_validation_pilot.md` and
  `scripts/run_optional_gmsh_validation.sh`; default tests, smoke, quality
  gates, and release validation do not run Gmsh.
- MPB optional validation pilot:
  `docs/mpb_optional_validation_pilot.md` and
  `scripts/run_optional_mpb_validation.sh`; default tests, smoke, quality
  gates, and release validation do not run MPB or require MPB CLI.
- Optiland optional validation pilot:
  `docs/optiland_optional_validation_pilot.md` and
  `scripts/run_optional_optiland_validation.sh`; default tests, smoke, quality
  gates, and release validation do not run Optiland.

## Release Blockers

- No hard release blocker is currently recorded for the post-`v0.9.0rc6`
  `0.9.0rc7.dev0` development state.
- v1.0 hard blockers remain: explicit PyPI publication decision and final
  `v1.0.0` release criteria.
- The public contract freeze is approved for the documented surface.
- Do not move `v0.9.0rc1`, `v0.9.0rc2`, `v0.9.0rc3`, `v0.9.0rc4`,
  `v0.9.0rc5`, or `v0.9.0rc6`.
- Do not publish PyPI yet.
- Do not re-upload the existing `0.9.0rc6.dev0` TestPyPI artifacts.
- Do not upload `0.9.0rc7.dev0` to TestPyPI unless separately approved.
- Keep generated adapter scaffolds presented as MVP inputs.
- Keep default CI free of external solver and external LLM requirements.
- Next blocker class: any future `v0.9.0rc7` candidate must pass the release smoke
  script, full tests, build, docs checks, and release readiness checks before a
  new tag is considered.

## Known Limitations

- No production-grade physical validation.
- No formal convergence proof.
- No full solver automation.
- No external solver execution in default CI.
- No external LLM provider required by default.
- Mock LLM evaluation is deterministic and not a real model-quality proof.
- Adapter outputs remain scaffold/MVP unless separately validated.
- Meep execution remains optional/local.

## Manual Release Checklist

1. Use `docs/post_release_status_v0.9.0rc6.md` as the rc6 source of truth.
2. Use `docs/v1_0_readiness_plan.md` for the next hardening priorities.
3. Use `docs/release_engineering_playbook.md` for repeatable RC procedure.
4. Review the public contract docs before changing CLI, schema, adapter, or
   workflow behavior.
5. Run the packaging and validation gates before any future RC.
6. Confirm any future `v0.9.0rc7` tag is absent locally and remotely before tag creation.
7. Create an annotated `v0.9.0rc7` tag only after final maintainer approval.
8. Keep PyPI unpublished and do not re-upload TestPyPI unless explicitly
   approved for a new version.
