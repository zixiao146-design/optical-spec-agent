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
- API response models: available in `src/optical_spec_agent/api/models.py`
- API examples and frontend fixtures: `examples/api/`
- Frontend implementation: not started
- PyPI: not published

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
responses include `status: error`, `error_code`, `message`, diagnostics,
recommended next actions, and the same conservative safety flags.

## Frontend readiness

Frontend Agent Studio should call this API later rather than shelling out to
the CLI directly. The API is a backend readiness surface only; no full frontend
implementation is included in this task. Future frontend work should use the
`examples/api/` fixtures for local mock data and contract checks.
