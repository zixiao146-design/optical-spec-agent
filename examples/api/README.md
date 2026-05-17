# Local Agent API Examples

These fixtures document the current local Agent API response shapes for a
future Agent Studio frontend. They are example request/response JSON files, not
a frontend implementation.

Current `api_contract_version`: 0.1.

## Guarantees

- No network access is required.
- No external solver execution is performed.
- No external LLM call is required.
- No proprietary solver is required.
- No production-grade physical validation is claimed.
- No formal convergence proof is claimed.

## Fixture manifest

`frontend_fixture_manifest.json` lists each fixture with:

- fixture name
- endpoint
- method
- request file when applicable
- response file
- `no_network: true`
- `external_solver_executed: false`
- `external_llm_required: false`
- `proprietary_solver_required: false`
- `production_grade_validation_claimed: false`
- `formal_convergence_proof_claimed: false`

The manifest includes successful responses and stable error fixtures for
schema, heuristic parse, invalid specs, unsupported adapters, invalid workflow
requests, and disabled external LLM parsing. Future frontend work should use
these fixtures for local mock data and contract checks before any full UI
implementation begins.

The manifest also includes Material Library and Agent Collaboration fixtures:

- `materials_response.json`
- `material_detail_sio2_response.json`
- `material_suggestion_request.json`
- `material_suggestion_response.json`
- `agent_trace_request_nanoparticle.json`
- `agent_trace_response_nanoparticle.json`
- `examples_response.json`
- `example_detail_nanoparticle_response.json`
- `example_agent_trace_nanoparticle_response.json`
- `agent_session_request_nanoparticle.json`
- `agent_session_response_nanoparticle.json`
- `agent_session_error_empty_goal_response.json`

These fixtures are local preview/design-assist data only. They do not perform
external material database lookup, solver execution, external LLM calls,
uploads, tags, or releases.

The Agent Command Center fixtures exercise `POST /api/agent-session` and show
how a natural language goal becomes optical intent, a design case, local plan
steps, sub-agent trace, permission gates, local artifacts, evidence, and next
actions. They preserve the same no-solver, no-external-LLM, no-upload, no-tag,
and no-release boundaries.

`scripts/check_api_fixtures.py` compares these fixtures with live FastAPI
`TestClient` response top-level shapes. `scripts/smoke_agent_api.sh` exercises
all current `/api/*` endpoints without starting a background server. Both
scripts preserve the no-network, no-solver, no-external-LLM, no-upload,
no-tag, and no-release boundaries.
