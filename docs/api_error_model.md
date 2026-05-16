# Local Agent API Error Model

## Purpose

Defines stable local API error behavior for a future Agent Studio frontend.
Errors should be renderable as diagnostics without implying solver execution,
external LLM use, network access, or expanded validation claims.

## Error response shape

Agent API errors use JSON with:

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

## Error categories

- `invalid_json`
- `invalid_spec`
- `unsupported_adapter`
- `invalid_workflow_request`
- `preview_generation_error`
- `solver_execution_not_enabled`
- `external_llm_not_enabled`

## Default behavior

- API does not execute solvers by default.
- API does not call external LLM by default.
- API does not require proprietary solvers.
- API does not claim production-grade physical validation.
- API does not claim a formal convergence proof.
