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
Local launch, frontend handoff, and curl examples are documented in
`docs/api_local_launch_guide.md`, `docs/frontend_handoff_spec.md`, and
`docs/api_curl_examples.md`.
Frontend MVP planning is documented in `docs/frontend_mvp_product_spec.md`,
`docs/frontend_information_architecture.md`, `docs/frontend_api_mapping.md`,
`docs/frontend_mvp_user_flows.md`,
`docs/frontend_mvp_acceptance_criteria.md`,
`docs/frontend_safety_policy.md`, and
`docs/frontend_mvp_implementation_plan.md`.
The implemented local MVP lives under `frontend/`, with run instructions in
`docs/frontend_mvp_runbook.md`.
Hardened frontend demo checks are documented in
`docs/frontend_mvp_qa_checklist.md` and exercised by
`scripts/smoke_frontend_mvp.sh`. Demo fixture mode is not live validation.

| CLI command | API endpoint | Parity status | Notes |
|---|---|---|---|
| `optical-spec --help` | `GET /api/health`, `GET /api/version` | Candidate-ready | API exposes service health and version/status metadata for frontend bootstrapping. |
| `optical-spec adapter-list --json` | `GET /api/adapters` | Candidate-ready | API returns adapter registry metadata, maturity summaries, and no-default-solver guarantees. |
| `optical-spec schema` | `GET /api/schema` | Candidate-ready | API returns the OpticalSpec JSON schema without network access. |
| `optical-spec parse ... --json` | `POST /api/parse` | Candidate-ready | API defaults to local heuristic/rule parsing and does not require an external LLM. |
| `optical-spec validate ...` | `POST /api/validate` | Candidate-ready | API validates inline specs or local repo paths with structured diagnostics. |
| `optical-spec workflow-plan ... --json` | `POST /api/workflow-plan` | Candidate-ready | API returns a local synchronous workflow preview and does not execute solvers. |
| `optical-spec adapter-generate ...` | `POST /api/adapter-preview` | Preview-ready | API returns preview content or artifact metadata only; it does not run the solver. |
| material catalog | `GET /api/materials`, `GET /api/materials/{material_id}` | API-first | Local preview material catalog; no production-grade optical constants claim. |
| material suggest | `POST /api/materials/suggest` | API-first | Local application-to-material hints; no network lookup. |
| optical design examples | `GET /api/examples`, `GET /api/examples/{example_id}` | API-first | Local bundled Example Gallery; examples load from `examples/optical_design/`. |
| agent collaboration | `POST /api/agent-trace` | API-first | Deterministic local sub-agent trace; no external LLM or solver call. |
| example collaboration | `POST /api/examples/{example_id}/agent-trace` | API-first | Builds an Agent Trace Timeline for a bundled example. |
| command-center task session | `POST /api/agent-session` | API-first | Natural language goal to optical intent, design case, plan, artifacts, permission gates, evidence, and next actions. |

## Shared boundaries

- External solvers are not run by default.
- External LLM access is not required by default.
- Proprietary solvers are not required by default.
- Production-grade physical validation is not claimed.
- Formal convergence proof is not claimed.
- The frontend MVP uses this API as its backend surface and does not shell out
  directly to CLI commands.
- API versioning, request validation, and migration notes are documented in
  `docs/api_versioning_policy.md`, `docs/api_request_validation_contract.md`,
  and `docs/api_migration_notes.md`.
- `scripts/smoke_agent_api.sh` and `scripts/check_api_fixtures.py` provide
  local API smoke and fixture consistency checks without uploading, publishing,
  creating tags, or creating releases.
