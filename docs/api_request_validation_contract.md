# Local Agent API Request Validation Contract

## Purpose

Defines how future Agent Studio requests are validated by the local
preview-first API.

## Request validation defaults

- Unknown request fields should be rejected where request models are explicit.
- Required fields should produce a stable error response.
- Invalid adapter/tool names should produce `unsupported_adapter`.
- Invalid spec payloads should produce `invalid_spec`.
- Invalid workflow requests should produce `invalid_workflow_request`.
- Solver execution requests are not enabled by default.

## Endpoint request expectations

- `POST /api/parse` expects local text and a local parser mode such as
  `heuristic` or `rule`.
- `POST /api/validate` expects an inline `spec` object or repo-local JSON
  `path`.
- `POST /api/workflow-plan` expects `text`, inline `spec`, or a repo-local
  workflow/spec `path`.
- `POST /api/adapter-preview` expects an inline `spec` object or repo-local JSON
  `path`, plus an optional adapter `tool`.

## Error response behavior

API error responses must include:

- `api_contract_version: "0.1"`
- `status: error`
- `error_code`
- `message`
- `diagnostics`
- `recommended_next_actions`
- `external_solver_executed: false`
- `external_llm_required: false`
- `proprietary_solver_required: false`
- `production_grade_validation_claimed: false`
- `formal_convergence_proof_claimed: false`

## Fixture and curl coverage

Request fixtures under `examples/api/` are suitable for frontend handoff and
for the curl examples in `docs/api_curl_examples.md`. The live consistency
script `scripts/check_api_fixtures.py` verifies that request files exist,
response files exist, and live API responses keep the same top-level shape and
safety flags as the fixture responses.
