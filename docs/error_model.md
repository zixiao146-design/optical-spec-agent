# Error Model

## Purpose

The error model documents how users should interpret common local/offline
failures.

## Scope

- Invalid JSON.
- Invalid spec or missing required field.
- Unsupported adapter.
- Invalid workflow request.
- Optional external solver not installed.
- Optional external LLM not configured.
- Proprietary solver unavailable.

## Principles

- The default offline path should fail deterministically.
- Errors should be actionable.
- Failures should not require network diagnosis unless explicitly using an
  external service.
- Missing optional solvers should not break default examples.
- Missing external LLM should not break the deterministic parser path.
- Proprietary tools are not default requirements.

## Non-goals

- Not a guarantee of production-grade physical validation.
- Not a formal convergence proof.
- Not a solver-backed correctness proof.
