# Local Agent API Contract

## Purpose

This API prepares a local-first Agent Studio backend. It exposes spec parsing,
validation, adapter discovery, workflow planning, artifact preview, validation
evidence, and readiness status without requiring network access, external
solvers, external LLMs, or proprietary tools by default.

## Current state

- Current public prerelease: v0.9.0rc7
- Current main development version: 0.9.0rc8.dev0
- v1.0 public contract freeze: approved
- API readiness: in progress
- API status: frontend-readiness / candidate API
- `api_contract_version`: 0.1
- API response models: available in `src/optical_spec_agent/api/models.py`
- API examples and frontend fixtures: `examples/api/`
- API versioning policy: `docs/api_versioning_policy.md`
- API request validation contract: `docs/api_request_validation_contract.md`
- API migration notes: `docs/api_migration_notes.md`
- Local launch guide: `docs/api_local_launch_guide.md`
- Frontend handoff spec: `docs/frontend_handoff_spec.md`
- Curl examples: `docs/api_curl_examples.md`
- Frontend MVP planning:
  `docs/frontend_mvp_product_spec.md`,
  `docs/frontend_information_architecture.md`,
  `docs/frontend_api_mapping.md`, `docs/frontend_mvp_user_flows.md`,
  `docs/frontend_mvp_acceptance_criteria.md`,
  `docs/frontend_safety_policy.md`, and
  `docs/frontend_mvp_implementation_plan.md`
- Live fixture consistency check: `scripts/check_api_fixtures.py`
- API smoke script: `scripts/smoke_agent_api.sh`
- Frontend MVP implementation: available under `frontend/`
- Frontend MVP runbook: `docs/frontend_mvp_runbook.md`
- Frontend MVP QA checklist: `docs/frontend_mvp_qa_checklist.md`
- Frontend MVP smoke script: `scripts/smoke_frontend_mvp.sh`
- Optional Playwright visual smoke:
  `docs/frontend_visual_smoke_runbook.md` and
  `scripts/smoke_frontend_visual.sh`
- PyPI: not published

The Local Agent API is not yet a separately frozen v1.0 API contract unless a
maintainer explicitly approves freezing it.

## Default guarantees

- No external solver execution by default.
- No external LLM call by default.
- No proprietary solver dependency.
- No network dependency for documented local examples.
- No production-grade physical validation claim.
- No formal convergence proof claim.
- Local synchronous preview only unless explicitly extended.

## Candidate API endpoints

- `GET /api/health`
- `GET /api/version`
- `GET /api/adapters`
- `GET /api/schema`
- `POST /api/parse`
- `POST /api/validate`
- `POST /api/workflow-plan`
- `POST /api/adapter-preview`
- `GET /api/validation-evidence`
- `GET /api/readiness`
- `GET /api/examples`
- `GET /api/examples/{example_id}`
- `POST /api/examples/{example_id}/agent-trace`
- `GET /api/design-requirements`
- `GET /api/design-requirements/{template_id}`
- `POST /api/design-requirements/match`
- `GET /api/materials`
- `GET /api/materials/{material_id}`
- `POST /api/materials/suggest`
- `POST /api/agent-trace`
- `POST /api/agent-session`

The design requirements endpoints expose deterministic natural-language goal
matching for seven optical design templates. They make the natural language ->
optical language -> design case -> expected tool calls path explicit without
calling an external LLM.

## Response shape principles

- JSON only.
- Include `api_contract_version`.
- Include `status`.
- Include diagnostics and warnings where relevant.
- Include `external_solver_executed=false` by default.
- Include `external_llm_required=false` by default.
- Include `proprietary_solver_required=false` by default.
- Include `production_grade_validation_claimed=false`.
- Include `formal_convergence_proof_claimed=false`.
- Include `recommended_next_actions` where appropriate.
- Use documented response models for health, version, adapters, schema, parse,
  validate, workflow-plan, adapter-preview, validation evidence, readiness, and
  error responses.

## Error behavior

Stable API error behavior is documented in `docs/api_error_model.md`. Error
responses include `api_contract_version`, `status: error`, `error_code`,
`message`, diagnostics, recommended next actions, and the same conservative
safety flags. Request validation behavior is documented in
`docs/api_request_validation_contract.md`.

## Frontend readiness

Frontend Agent Studio calls this API rather than shelling out to the CLI
directly. The first local MVP is implemented under `frontend/` and uses the
`examples/api/` fixtures for local mock data and contract checks.

## Handoff readiness

The local launch guide, frontend handoff spec, curl examples, API smoke script,
and live fixture consistency script are now part of the API readiness package.
They help a future frontend developer run the backend locally, copy documented
curl calls, and check that `examples/api/` fixtures still match the live API
top-level response shape. These checks do not run solvers, call external LLMs,
upload packages, create tags, or create releases.

Frontend MVP implementation now exists under `frontend/`. It is local-first,
uses `VITE_API_BASE_URL`, and does not include solver execution, external LLM,
upload, publish, tag, release, login, cloud, or production deployment controls.
The hardened MVP includes loading, empty, error, API disconnected, and demo
fixture states. Demo fixture mode is explicitly not live validation.
Optional Playwright visual smoke is manual-only and verifies local rendering
and safety copy without changing the API contract or release gate.

## Optical Design Domain Expansion

API contract version `0.1` now includes local preview endpoints for optical
design domain assistance:

- `GET /api/materials`
- `GET /api/materials/{material_id}`
- `POST /api/materials/suggest`
- `GET /api/examples`
- `GET /api/examples/{example_id}`
- `POST /api/examples/{example_id}/agent-trace`
- `POST /api/agent-trace`

These endpoints are frontend-readiness / candidate API surfaces. They do not
run external solvers, do not call external LLMs, do not access external material
databases, do not upload packages, and do not create tags/releases. Material
records are local preview/design-assist hints, not production-grade optical
constants. Example Gallery responses load only local `examples/optical_design`
files. The Agent Trace Timeline is deterministic local collaboration
visibility, not autonomous external agent execution.

## Agent Command Center

API contract version `0.1` also includes the task-driven command-center
endpoint:

- `POST /api/agent-session`
- `GET /api/tool-capabilities`
- `POST /api/optics/thin-film`
- `POST /api/optics/thin-film-spectrum`
- `POST /api/optics/quarter-wave-ar`
- `POST /api/optics/paraxial-lens`
- `POST /api/optics/paraxial-system`
- `POST /api/optics/two-lens-relay`
- `POST /api/optics/gaussian-beam`
- `POST /api/optics/gaussian-beam-series`
- `POST /api/optics/gaussian-beam-focus`
- `POST /api/optics/waveguide-estimate`
- `POST /api/optics/waveguide-sweep`
- `POST /api/optics/waveguide-single-mode-range`
- `GET /api/backend-capability-report`
- `GET /api/backend-evidence-summary`
- `GET /api/design-case-cross-checks`
- `GET /api/adapter-native-golden-coverage`

This endpoint turns a natural language optical design goal into a
deterministic local Agent Task Session: optical intent, selected design case, material
suggestions, adapter recommendation, workflow plan steps, artifacts, evidence,
permission gates, a tool-call ledger, and recommended next actions. It reuses
the local material catalog, local example registry, deterministic sub-agent
trace, and preview optical calculators when applicable. Calculator-backed cases
now include thin-film spectrum and quarter-wave AR previews, Gaussian beam
series/focus previews, paraxial system and two-lens relay previews, and
waveguide sweep/single-mode range previews. `/api/tool-capabilities` reports
internal tools, external solver availability detection, and disabled
publication/release controls without executing external tools. The optics
endpoints provide preview/design-assist calculations only. These endpoints do
not call an external LLM, do not execute a solver, do not access the network,
do not upload packages, and do not create tags/releases.

Calculator responses expose explicit `quality`, `warnings`, `assumptions`, and
`limitations` fields. The current quality level is
`sanity_checked_preview`; reference-case formulas are documented in
`docs/optical_calculator_reference_cases.md`. These fields improve numeric
sanity evidence without changing the no-production-validation boundary.

The backend-readiness report endpoints add maintainer-facing proof of backend
reality. `GET /api/backend-capability-report` returns package status,
sub-agent execution status, internal tool import/call/execution status,
calculator quality/reference-case status, design-case cross-check summaries,
and blocked external actions. `GET /api/backend-evidence-summary` returns a
maintainer review summary that bundles sub-agent reality, tool-call reality,
calculator evidence, design-case cross-checks, source/monitor diagnostics,
adapter-native golden coverage, and blocked/deferred capabilities.
`GET /api/design-case-cross-checks` verifies
bundled optical design examples against expected calculator or adapter-trace
behavior. These endpoints do not run external solvers, call external LLMs,
upload packages, create tags/releases, or claim production-grade physical
validation.

`POST /api/optical-language/infer`,
`POST /api/optical-language/diagnose`,
`POST /api/optical-language/observables/diagnose`, and
`POST /api/optical-language/adapter-mapping` expose source/monitor/observable
metadata, missing-input diagnostics, observable taxonomy, and adapter-native
preview semantics. `POST /api/agent-session` includes the same `source_model`,
`monitor_model`, `optical_language_diagnostics`, `observable_diagnostics`, and
`adapter_source_monitor_mapping` fields plus ledger entries for
`optical_language.infer_source_monitor`,
`optical_language.diagnose_missing_inputs`,
`optical_language.diagnose_observable`, and
`optical_language.map_source_monitor_to_adapter`. Monitor definitions are
preview-only metadata, not external solver monitor results.
Adapter-native golden fixtures under `examples/adapter_native_golden/` and
`examples/api/adapter_native_golden_*_response.json` lock expected preview
semantics for Meep, MPB, Gmsh, Elmer, and Optiland without running solvers.
`GET /api/adapter-native-golden-coverage` exposes a machine-readable coverage
matrix, and the backend capability report includes the same
`adapter_native_golden_coverage` section. The matrix records strict metadata
diff status, native mapping terms, preview-only flags, and the fact that real
solver results still require explicit solver execution.
