# Local Agent API Contract

## Purpose

This API prepares a local-first Agent Studio backend. It exposes spec parsing,
validation, adapter discovery, workflow planning, artifact preview, validation
evidence, and readiness status without requiring network access, external
solvers, external LLMs, or proprietary tools by default.

## Current state

- Current public prerelease: v0.9.0rc6
- Current main development version: 0.9.0rc7.dev0
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
