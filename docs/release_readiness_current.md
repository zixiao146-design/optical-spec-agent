# Current Release Readiness

This document describes the current `main` branch. It is not a release tag.

## Current State

- `pyproject.toml` package version on `main`: `0.9.0rc8.dev0`
- Current public prerelease: `v0.9.0rc7`
- Current main development version: `0.9.0rc8.dev0`
- Main branch state: post-v0.9.0rc7 development toward `v0.9.0rc8`
- Product positioning: open-source-solver-first
- `v0.9.0rc7` GitHub prerelease has been created and verified
- `v0.9.0rc8.dev0` is not a public release
- GitHub release for `v0.9.0rc8`: not created
- `v0.9.0rc8` tag has not been created
- `v1.0.0` tag has not been created
- Current public GitHub prerelease created: yes (`v0.9.0rc7`)
- Current public prerelease verified: yes
- Post-release status doc: `docs/post_release_status_v0.9.0rc7.md`
- Latest release-status commit: `37923d4`
- PyPI published: no
- TestPyPI uploaded: yes, for `0.9.0rc6.dev0`
- TestPyPI upload for `0.9.0rc8.dev0`: not performed
- TestPyPI upload approval record:
  `docs/testpypi_upload_approval_v0.9.0rc6.dev0.md`
- TestPyPI upload approval record for rc7:
  `docs/testpypi_upload_approval_v0.9.0rc7.md`
- TestPyPI upload approval record for rc8 development:
  `docs/testpypi_upload_approval_v0.9.0rc8.dev0.md`
- Latest TestPyPI upload attempt:
  `docs/testpypi_upload_attempt_v0.9.0rc6.dev0.md`
- TestPyPI status:
  `docs/testpypi_status_v0.9.0rc6.dev0.md`
- TestPyPI Trusted Publishing doc:
  `docs/testpypi_trusted_publishing.md`
- TestPyPI Trusted Publishing workflow:
  `.github/workflows/testpypi-trusted-publish.yml` (manual, passed for
  `0.9.0rc6.dev0`)
- TestPyPI upload approval status for 0.9.0rc8.dev0: pending
- TestPyPI upload authorized for rc8.dev0: no
- Upload command authorized for 0.9.0rc8.dev0: no
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
  `docs/agent_studio_frontend_roadmap.md` (local MVP implemented; production
  frontend remains future/Phase 2 and not a v1.0.0 blocker)
- Local Agent API readiness:
  `docs/api_agent_contract.md` and `docs/cli_api_parity.md` (in progress;
  frontend MVP implemented)
- Local Agent API error model:
  `docs/api_error_model.md`
- Local Agent API versioning and request validation:
  `docs/api_versioning_policy.md`, `docs/api_request_validation_contract.md`,
  and `docs/api_migration_notes.md`
- Local Agent API frontend fixtures:
  `examples/api/`
- Local Agent API local launch guide:
  `docs/api_local_launch_guide.md`
- Frontend handoff spec:
  `docs/frontend_handoff_spec.md`
- API curl examples:
  `docs/api_curl_examples.md`
- API smoke script:
  `scripts/smoke_agent_api.sh`
- API fixture consistency script:
  `scripts/check_api_fixtures.py`
- Agent Studio frontend MVP planning:
  `docs/frontend_mvp_product_spec.md`,
  `docs/frontend_information_architecture.md`,
  `docs/frontend_api_mapping.md`, `docs/frontend_mvp_user_flows.md`,
  `docs/frontend_mvp_acceptance_criteria.md`,
  `docs/frontend_safety_policy.md`, and
  `docs/frontend_mvp_implementation_plan.md`
- Agent Studio frontend MVP implementation:
  `frontend/`, `docs/frontend_mvp_runbook.md`, and
  `docs/frontend_mvp_qa_checklist.md`
- Agent Studio frontend English / 中文 localization:
  `docs/frontend_i18n_zh_CN.md` and `frontend/src/i18n/`; UI copy, guided
  demo, and safety copy are localized, while API JSON field names, adapter tool
  names, and `api_contract_version` remain unchanged.
- Optical design domain expansion:
  local preview material catalog, `examples/optical_design/`, and
  deterministic sub-agent collaboration trace for Agent Studio. These are
  preview-first development capabilities and do not authorize PyPI/TestPyPI
  upload, create tags/releases, run external solvers by default, call external
  LLMs by default, claim production-grade physical validation, or claim formal
  convergence proof.
- Agent Command Center:
  `POST /api/agent-session`, `docs/agent_command_center.md`, and
  `docs/agent_command_center.zh-CN.md` provide a local deterministic task
  session surface from natural language goal to optical intent, design case,
  plan steps, sub-agent trace, artifacts, permission gates, evidence, and next
  actions. This is not a release, PyPI, TestPyPI, tag, or GitHub release action.
- Backend evidence review decision:
  `docs/backend_evidence_review_decision.md` records that backend evidence is
  sufficient for the v0.9.0rc7 release draft that has now been published as a
  GitHub prerelease. It does not approve PyPI publication, TestPyPI upload for
  0.9.0rc8.dev0, creating a v0.9.0rc8 tag, creating a v1.0.0 tag/release, or
  claiming production-grade physical validation.
- rc8 backend roadmap:
  `docs/rc8_backend_roadmap.md` classifies post-rc7 backend work as done /
  stable enough, needs backend hardening, deferred / non-blocker, future /
  Phase 2, and not a goal.
- rc8 capability gap audit:
  `docs/rc8_capability_gap_audit.md` records remaining backend hardening gaps
  before any future rc8, PyPI, or v1.0.0 decision.
- rc8 to v1.0 decision path:
  `docs/rc8_to_v1_0_decision_path.md` keeps rc8.dev0 engineering separate from
  future rc8 release draft, PyPI publication, and v1.0.0 decisions.
- Application-domain benchmarks:
  `docs/application_domain_benchmarks.md`,
  `docs/domain_benchmark_results_policy.md`, and
  `examples/application_domain_benchmarks/` evaluate positive, ambiguous,
  underconstrained, unsupported, and unsafe/blocked optical-design requests
  without running solvers or calling external LLMs.
- Optional solver micro-benchmark readiness/approval:
  `docs/optional_solver_micro_benchmark_approval_matrix.md`,
  `docs/optional_solver_micro_benchmark_approval_record_template.md`,
  `docs/optional_solver_micro_benchmark_readiness_status.md`, and
  `docs/optional_solver_environment_profiles.md`,
  `docs/optional_solver_micro_benchmark_execution_packet.md`,
  `docs/optional_solver_execution_sequence.md`, and
  `docs/optional_solver_approval_records/`, plus
  `scripts/check_optional_solver_readiness.py` make candidate solver execution
  reviewable before any opt-in run. Readiness is environment-aware:
  `OSA_SOLVER_PYTHON` can probe a dedicated solver Python such as
  `osa-solvers`, while CLI tools such as Gmsh are detected from the current
  `PATH`. Default behavior remains no solver
  execution, Elmer remains deferred, and these records do not authorize
  PyPI/TestPyPI upload, tag creation, or GitHub release creation.
- Approved Gmsh-only optional micro-benchmark evidence:
  `validation/gmsh/gmsh_micro_benchmark_2026-05-20.md`. This is mesh
  generation smoke evidence only; Meep, MPB, Optiland, and Elmer were not run.
- Gmsh micro-benchmark review decision:
  `docs/optional_solver_approval_records/gmsh_micro_benchmark_review_2026-05-20.md`.
  The evidence is accepted only as optional manual mesh-generation smoke
  evidence. Optiland is the next candidate only and is not approved; Meep/MPB
  require `OSA_SOLVER_PYTHON` and separate approval; Elmer remains deferred.
- Fiber coupling and polarization warning closure:
  `POST /api/optics/fiber-coupling`,
  `POST /api/optics/polarization-jones`,
  `docs/fiber_coupling_preview_calculator.md`, and
  `docs/polarization_preview_calculator.md` provide deterministic preview
  calculators for the two former warning-level application domains. They are
  preview/design-assist only and do not prove real coupling efficiency, vector
  EM polarization behavior, or production-grade validation.
- Frontend MVP smoke:
  `scripts/smoke_frontend_mvp.sh`
- Frontend visual smoke plan:
  `docs/frontend_visual_smoke_plan.md`
- Frontend visual smoke runbook:
  `docs/frontend_visual_smoke_runbook.md` (manual/optional, not part of the
  default release gate)
- Frontend visual smoke script:
  `scripts/smoke_frontend_visual.sh`
- Agent Studio local demo package:
  `scripts/demo_agent_studio.sh`, `docs/agent_studio_demo_runbook.md`,
  `docs/agent_studio_demo_checklist.md`,
  `docs/agent_studio_demo_storyboard.md`, and
  `docs/agent_studio_demo_troubleshooting.md` (local-only, not a release or
  publication action)
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
| Frontend fixtures | API examples ready | `examples/api/`; frontend MVP implemented |
| Frontend handoff | API handoff docs/scripts ready | Launch guide, handoff spec, curl examples, smoke script, fixture consistency script, frontend runbook |
| Frontend MVP | Local MVP implemented and hardened | React + Vite + TypeScript under `frontend/`; fixture loading, API mode indicator, diagnostics, recommended actions, loading/empty/error/API-disconnected/demo states; optional Playwright visual smoke; local demo package; no upload/release/solver/LLM controls |
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

Current recommendation: treat `v0.9.0rc7` as the active verified public
prerelease while `main` moves to post-v0.9.0rc7 development toward
`v0.9.0rc8`. The `v0.9.0rc8` tag has not been created, no GitHub release
exists for rc8, and publication remains separately gated. TestPyPI contains
the `0.9.0rc6.dev0` development package via manual Trusted Publishing, but
TestPyPI upload for `0.9.0rc8.dev0` has not been performed; PyPI remains
unpublished.

Use `docs/rc8_backend_roadmap.md`, `docs/rc8_capability_gap_audit.md`, and
`docs/rc8_to_v1_0_decision_path.md` for post-rc7 backend engineering. These
documents do not prepare a `v0.9.0rc8` release draft, do not create tags or
GitHub releases, do not approve PyPI/TestPyPI publication, and do not claim
production-grade physical validation or a formal convergence proof.

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
- `docs/quickstart.md`
- `docs/quickstart.zh-CN.md`
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
- `examples/quickstart/README.md`

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
- Agent Studio domain workflow evidence:
  `docs/example_gallery.md`, `docs/agent_trace_timeline.md`,
  `docs/material_library.md`, `examples/optical_design/`, and
  `tests/test_example_registry.py`; Example Gallery and Agent Trace Timeline
  are preview-first local UI/API surfaces and do not run solvers or call
  external LLMs.
- Backend tool-call reality evidence:
  `docs/tool_call_reality_matrix.md`, `docs/backend_functionality_status.md`,
  `docs/backend_capability_report.md`, `docs/design_case_cross_checks.md`,
  `docs/design_requirement_templates.md`, `docs/natural_language_to_optical_language.md`,
  `scripts/audit_sub_agents.py`, `scripts/smoke_backend_capabilities.sh`, and
  `scripts/smoke_backend_report.sh`;
  these document installed/callable/executed status, task-session tool-call
  ledgers, blocked solver/LLM/upload/tag/release actions, and local optical
  preview calculators. The generated report also cross-checks bundled design
  cases against expected calculator or adapter-trace behavior. rc8.dev0 adds
  material provenance coverage, material suitability diagnostics, ambiguous
  requirement matching, and critical/optional missing-input diagnostics without
  changing publication or release boundaries.
- Maintainer backend evidence review pack:
  `docs/backend_evidence_review_pack.md`,
  `docs/backend_evidence_review_pack.zh-CN.md`,
  `scripts/generate_backend_evidence_pack.py`, and
  `scripts/smoke_backend_evidence_pack.sh`; this bundles sub-agent reality,
  tool-call reality, calculator evidence, design-case cross-checks,
  source/monitor diagnostics, adapter-native golden coverage, blocked external
  actions, and maintainer review questions. It is preview/design-assist
  evidence only and does not authorize PyPI/TestPyPI upload, tags, or releases.
- Optical calculator evidence:
  `docs/optical_calculators.md`, `docs/optical_calculators.zh-CN.md`,
  `docs/optical_calculator_case_integration.md`,
  `docs/optical_calculator_case_integration.zh-CN.md`,
  `examples/optics_calculators/`, and `/api/optics/*`; calculators now cover
  thin-film spectra, quarter-wave AR, Gaussian beam series/focus, paraxial
  systems/two-lens relays, and waveguide sweeps/single-mode ranges. They are
  preview/design-assist only and do not claim production-grade physical
  validation. Reference sanity cases and quality fields are documented in
  `docs/optical_calculator_reference_cases.md` and
  `docs/optical_calculator_reference_cases.zh-CN.md`.

## Release Blockers

- No hard release blocker is currently recorded for the post-`v0.9.0rc7`
  `0.9.0rc8.dev0` development state.
- v1.0 hard blockers remain: explicit PyPI publication decision and final
  `v1.0.0` release criteria.
- The public contract freeze is approved for the documented surface.
- Do not move `v0.9.0rc1`, `v0.9.0rc2`, `v0.9.0rc3`, `v0.9.0rc4`,
  `v0.9.0rc5`, `v0.9.0rc6`, or `v0.9.0rc7`.
- Do not publish PyPI yet.
- Do not re-upload the existing `0.9.0rc6.dev0` TestPyPI artifacts.
- Do not upload `0.9.0rc8.dev0` to TestPyPI unless separately approved.
- Keep generated adapter scaffolds presented as MVP inputs.
- Keep default CI free of external solver and external LLM requirements.
- Next blocker class: any future `v0.9.0rc8` candidate must pass the release smoke
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
- Source/monitor inference, missing-input diagnostics, observable diagnostics,
  and adapter-native source/monitor mapping are backend preview metadata only;
  they do not represent executed solver monitor results.
- Adapter-native golden preview cases and coverage matrices are local fixture
  and metadata-diff checks only; they do not represent executed solver monitor
  results or production-grade validation.

## Manual Release Checklist

1. Use `docs/post_release_status_v0.9.0rc7.md` as the rc7 source of truth.
2. Use `docs/v1_0_readiness_plan.md` for the next hardening priorities.
3. Use `docs/release_engineering_playbook.md` for repeatable RC procedure.
4. Review the public contract docs before changing CLI, schema, adapter, or
   workflow behavior.
5. Run the packaging and validation gates before any future RC.
6. Confirm any future `v0.9.0rc8` tag is absent locally and remotely before tag creation.
7. Create an annotated `v0.9.0rc8` tag only after final maintainer approval.
8. Keep PyPI unpublished and do not re-upload TestPyPI unless explicitly
   approved for a new version.

## Application Domain Coverage

The rc8.dev0 backend now includes `GET /api/application-domains`,
`POST /api/application-domains/match`, and `GET /api/application-domain-cross-checks`.
These local-only endpoints connect ten preview domains to material suitability,
requirement templates, expected calculators/adapters, missing-input questions,
and deferred capability notes. They do not execute solvers, call external LLMs,
or claim production-grade physical validation.

Application-domain benchmark endpoints and fixtures now cover positive,
ambiguous, underconstrained, unsupported, and unsafe/blocked scenarios. The
benchmark evaluator keeps warnings for intentionally partial domains and blocks
commercial solver or production-grade validation requests by default.

## Validation Maturity and Preview Boundary

Current readiness now includes a conservative validation maturity layer:

- [`backend_validation_maturity_matrix.md`](backend_validation_maturity_matrix.md)
  classifies materials, calculators, application domains, adapter metadata,
  sub-agent sessions, tool-call ledger evidence, and frontend UI/demo surface.
- [`preview_boundary_policy.md`](preview_boundary_policy.md) states what users
  can rely on and what they must independently verify.
- `GET /api/backend-validation-maturity` exposes the same summary through the
  local API.
- `scripts/audit_validation_claims.py` scans repo text for unsafe validation
  overclaims before future release-draft work.
- Optional solver-backed micro-benchmark planning is documented in
  [`solver_validation_micro_benchmarks.md`](solver_validation_micro_benchmarks.md)
  and `validation/solver_validation_micro_benchmarks.json`. The wrapper
  `scripts/run_optional_solver_micro_benchmarks.sh` is default no-execute and
  requires explicit `OSA_RUN_OPTIONAL_*_VALIDATION=1` before any solver-backed
  run.
