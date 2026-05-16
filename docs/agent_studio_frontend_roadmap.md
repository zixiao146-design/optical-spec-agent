# Agent Studio Frontend Roadmap

## Purpose

A future frontend should make the project feel like an agent by visualizing spec
parsing, validation, adapter selection, workflow planning, artifact preview, and
validation evidence.

## Current status

- Not part of v1.0.0 release criteria.
- Not required for v1.0.0.
- This is not a v1.0.0 release blocker.
- Local Agent API readiness is in progress through
  `docs/api_agent_contract.md` and `docs/cli_api_parity.md`.
- API response models exist in `src/optical_spec_agent/api/models.py`.
- Current `api_contract_version`: 0.1.
- API versioning and request validation are documented in
  `docs/api_versioning_policy.md` and `docs/api_request_validation_contract.md`.
- Frontend fixture examples exist under `examples/api/`.
- Frontend implementation is not started.
- Agent Studio frontend should call the local Agent API instead of shelling out
  directly to the CLI.
- Should follow API readiness and continued backend contract tests.
- Should remain local-first and no-default-solver.
- The API and future frontend must not run external solvers, call external
  LLMs, require proprietary tools, or access the network by default.

## Recommended phases

### Phase 1.5

- API readiness.
- FastAPI endpoints.
- API contract tests.
- No-solver/no-LLM default behavior.
- API endpoints for health/version, adapter registry, schema, parse, validate,
  workflow-plan, adapter-preview, validation evidence, and readiness/status.
- API response model and fixture coverage for frontend mock data.

### Phase 2

- Frontend MVP.
- Spec input.
- Adapter matrix.
- Workflow plan.
- Artifact preview.
- Validation evidence view.

### Phase 3

- Agent Studio.
- Session history.
- Approval gates.
- Optional solver panel.
- Report export.

## Non-goals for frontend MVP

- No cloud requirement.
- No login system.
- No default solver execution.
- No proprietary solver dependency.
- No production-grade claim.
