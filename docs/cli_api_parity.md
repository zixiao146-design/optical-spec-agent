# CLI / API Parity

This document maps the documented CLI surface to the local Agent API readiness
surface for a future Agent Studio frontend. The API is local-first and does not
run external solvers, call external LLMs, require proprietary tools, or access
the network by default.

API response models are defined in `src/optical_spec_agent/api/models.py`, and
frontend fixture examples live under `examples/api/`. The current
`api_contract_version` is 0.1, and the API remains a
frontend-readiness / candidate API rather than a separately frozen v1.0 API
contract.

| CLI command | API endpoint | Parity status | Notes |
|---|---|---|---|
| `optical-spec --help` | `GET /api/health`, `GET /api/version` | Candidate-ready | API exposes service health and version/status metadata for frontend bootstrapping. |
| `optical-spec adapter-list --json` | `GET /api/adapters` | Candidate-ready | API returns adapter registry metadata, maturity summaries, and no-default-solver guarantees. |
| `optical-spec schema` | `GET /api/schema` | Candidate-ready | API returns the OpticalSpec JSON schema without network access. |
| `optical-spec parse ... --json` | `POST /api/parse` | Candidate-ready | API defaults to local heuristic/rule parsing and does not require an external LLM. |
| `optical-spec validate ...` | `POST /api/validate` | Candidate-ready | API validates inline specs or local repo paths with structured diagnostics. |
| `optical-spec workflow-plan ... --json` | `POST /api/workflow-plan` | Candidate-ready | API returns a local synchronous workflow preview and does not execute solvers. |
| `optical-spec adapter-generate ...` | `POST /api/adapter-preview` | Preview-ready | API returns preview content or artifact metadata only; it does not run the solver. |

## Shared boundaries

- External solvers are not run by default.
- External LLM access is not required by default.
- Proprietary solvers are not required by default.
- Production-grade physical validation is not claimed.
- Formal convergence proof is not claimed.
- The frontend implementation is not started; Agent Studio should use this API
  as the backend surface when that work begins.
- API versioning, request validation, and migration notes are documented in
  `docs/api_versioning_policy.md`, `docs/api_request_validation_contract.md`,
  and `docs/api_migration_notes.md`.
