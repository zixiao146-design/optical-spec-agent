# Frontend Handoff Spec

## Purpose

Defines what the Agent Studio Frontend MVP can rely on today.
Frontend MVP planning is documented in `docs/frontend_mvp_product_spec.md`,
`docs/frontend_information_architecture.md`, `docs/frontend_api_mapping.md`,
`docs/frontend_mvp_user_flows.md`,
`docs/frontend_mvp_acceptance_criteria.md`,
`docs/frontend_safety_policy.md`, and
`docs/frontend_mvp_implementation_plan.md`.
The implemented local MVP lives under `frontend/`, with run instructions in
`docs/frontend_mvp_runbook.md`.
The hardened MVP includes loading, empty, error, and API disconnected states.
When the API is unavailable, demo fixture mode keeps the UI navigable but is
explicitly marked as not live validation.
The interaction polish layer adds fixture loading buttons, API mode indicators,
diagnostics panels, recommended action panels, and collapsible JSON payloads.

## API base

- Local base URL: `http://127.0.0.1:8000`
- API contract version: 0.1
- Package version: 0.9.0rc7.dev0

## Frontend-ready endpoints

| Endpoint | Frontend use case | Request fixture | Response fixture | Safety notes |
|---|---|---|---|---|
| `GET /api/health` | Boot check and service availability. | none | `examples/api/health_response.json` | No solver, LLM, network, upload, tag, or release action. |
| `GET /api/version` | Show package/API/public-release status. | none | `examples/api/version_response.json` | Reports PyPI not published and TestPyPI verified only for 0.9.0rc6.dev0. |
| `GET /api/adapters` | Populate adapter matrix. | none | `examples/api/adapters_response.json` | Adapter discovery only; no solver execution. |
| `GET /api/schema` | Render schema-aware spec editor hints. | none | `examples/api/schema_response.json` | Local schema only; no network. |
| `POST /api/parse` | Convert text into a local preview spec. | `examples/api/parse_request_heuristic.json` | `examples/api/parse_response_heuristic.json` | Uses heuristic/rule parser by default; no external LLM. |
| `POST /api/validate` | Validate inline or local-path specs. | `examples/api/validate_request_minimal.json` | `examples/api/validate_response_minimal.json` | Local validation only; no production-grade physical validation claim. |
| `POST /api/workflow-plan` | Render local workflow plan. | `examples/api/workflow_plan_request.json` | `examples/api/workflow_plan_response.json` | Preview plan only; `external_solver_executed=false`. |
| `POST /api/adapter-preview` | Show generated artifact preview. | `examples/api/adapter_preview_gmsh_request.json` | `examples/api/adapter_preview_gmsh_response.json` | Generates preview content only; does not run the solver. |
| `GET /api/validation-evidence` | Render validation evidence summary. | none | `examples/api/validation_evidence_response.json` | Evidence summary only; no production-grade claim. |
| `GET /api/readiness` | Render release/readiness status and next steps. | none | `examples/api/readiness_response.json` | Reports PyPI not published and no v1.0.0 release. |

## Frontend screens mapped to endpoints

- Spec input screen -> `POST /api/parse` and `POST /api/validate`
- Adapter matrix -> `GET /api/adapters` and `GET /api/validation-evidence`
- Workflow plan -> `POST /api/workflow-plan`
- Artifact preview -> `POST /api/adapter-preview`
- Readiness/status -> `GET /api/readiness`
- Evidence view -> `GET /api/validation-evidence`

## Implemented MVP

- React + Vite + TypeScript frontend app exists under `frontend/`.
- It uses `VITE_API_BASE_URL` and defaults to `http://127.0.0.1:8000`.
- It calls the Local Agent API rather than shelling out to the CLI.
- It includes Dashboard, Spec Input, Adapter Matrix, Workflow Plan, Artifact
  Preview, Validation Evidence, and System Status views.
- It includes shared `LoadingState`, `EmptyState`, `ErrorState`,
  `SafetyNotice`, `ApiDisconnectedNotice`, `ApiModeIndicator`,
  `DiagnosticsPanel`, `RecommendedActions`, and `DemoModeBanner` components.
- It can fall back to demo fixtures for local walkthroughs without live API
  validation.
- It includes fixture loading buttons for Spec Input, Workflow Plan, and
  Artifact Preview. Loading fixtures fills local forms but does not call the
  API until submitted.
- Visual smoke planning is documented in `docs/frontend_visual_smoke_plan.md`.

## Not implemented beyond MVP

- No session history.
- No login.
- No cloud backend.
- No default solver execution.
- No default external LLM.
- No PyPI/TestPyPI upload controls.
- No tag/release controls.
