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
invalid specs, unsupported adapters, invalid workflow requests, and disabled
external LLM parsing. Future frontend work should use these fixtures for local
mock data and contract checks before any full UI implementation begins.
