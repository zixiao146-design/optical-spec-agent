# Agent Studio Frontend API Mapping

| Frontend screen | API endpoint | Method | Request fixture | Response fixture | Safety notes |
|---|---|---|---|---|---|
| Dashboard | `/api/readiness` | GET | none | `examples/api/readiness_response.json` | Shows PyPI not published, v1.0.0 not released, and recommended next actions. |
| Agent Command Center | `/api/agent-session` | POST | `examples/api/agent_session_request_nanoparticle.json` | `examples/api/agent_session_response_nanoparticle.json` | Converts a natural language goal into a deterministic local task session with plan, artifacts, permission gates, evidence, and next actions. |
| Spec Input | `/api/parse` | POST | `examples/api/parse_request_heuristic.json` | `examples/api/parse_response_heuristic.json` | Uses local heuristic/rule parser by default; no external LLM. |
| Spec Input | `/api/validate` | POST | `examples/api/validate_request_minimal.json` | `examples/api/validate_response_minimal.json` | Local spec validation only; no production-grade validation claim. |
| Adapter Matrix | `/api/adapters` | GET | none | `examples/api/adapters_response.json` | Registry summary only; no solver execution. |
| Adapter Matrix | `/api/validation-evidence` | GET | none | `examples/api/validation_evidence_response.json` | Shows evidence and limitations without expanding claims. |
| Example Gallery | `/api/examples` | GET | none | `examples/api/examples_response.json` | Lists local optical design examples only; no solver or network. |
| Example Gallery | `/api/examples/{example_id}` | GET | none | `examples/api/example_detail_nanoparticle_response.json` | Loads bundled spec and expected trace files from the repo. |
| Example Gallery / Agent Collaboration | `/api/examples/{example_id}/agent-trace` | POST | none | `examples/api/example_agent_trace_nanoparticle_response.json` | Builds deterministic local Agent Trace Timeline; no external LLM. |
| Workflow Plan | `/api/workflow-plan` | POST | `examples/api/workflow_plan_request.json` | `examples/api/workflow_plan_response.json` | Local synchronous preview only; `external_solver_executed=false`. |
| Artifact Preview | `/api/adapter-preview` | POST | `examples/api/adapter_preview_gmsh_request.json` | `examples/api/adapter_preview_gmsh_response.json` | Preview artifact only; does not run solver. |
| Evidence | `/api/validation-evidence` | GET | none | `examples/api/validation_evidence_response.json` | Gmsh/Meep/MPB/Optiland Level 3 evidence; Elmer deferred. |
| System Status | `/api/health` | GET | none | `examples/api/health_response.json` | Local service health only. |
| System Status | `/api/version` | GET | none | `examples/api/version_response.json` | Shows package version and `api_contract_version`. |
| Material Library | `/api/materials` | GET | none | `examples/api/materials_response.json` | Local preview material catalog only. |
| Material Library | `/api/materials/suggest` | POST | `examples/api/material_suggestion_request.json` | `examples/api/material_suggestion_response.json` | Application hints; no external material lookup. |
| Agent Collaboration | `/api/agent-trace` | POST | `examples/api/agent_trace_request_nanoparticle.json` | `examples/api/agent_trace_response_nanoparticle.json` | Deterministic local trace; no external LLM. |

All mapped endpoints are local-first, no-network fixtures for frontend planning.
They must not expose upload, publish, tag, release, solver-run, or external LLM
controls in the MVP.
The implemented frontend API client is `frontend/src/api/client.ts` and calls
only the configured local API base URL plus these `/api/*` paths.
