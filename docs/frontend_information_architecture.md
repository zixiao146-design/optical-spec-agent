# Agent Studio Frontend Information Architecture

The MVP should be a single-user, local-first interface backed by the Local Agent
API. It requires no authentication, no cloud dependency, and no solver
execution by default.
The implementation exists under `frontend/` and follows this information
architecture.

## 1. Agent Command Center

- Calls `POST /api/agent-session`.
- Shows natural language goal input, optical intent summary, selected design
  case, agent plan, sub-agent trace, permission gates, artifacts, evidence, and
  recommended next actions.
- Keeps blocked gates visible for external solver, external LLM, upload,
  publication, tag, and release actions.
- Does not run solvers, call external LLMs, upload packages, or create
  tags/releases.

## 2. Dashboard / Readiness

- Calls `GET /api/readiness`.
- Shows current public prerelease, main release draft, TestPyPI/PyPI
  status, and contract freeze status.
- Shows recommended next actions.
- Shows API mode indicator and API base URL.

## 3. Spec Input

- Calls `POST /api/parse`.
- Calls `POST /api/validate`.
- Shows parsed spec, validation status, and diagnostics.
- Includes fixture loading for local demos; fixture loading is not live
  validation until submitted.

## 4. Adapter Matrix

- Calls `GET /api/adapters`.
- Calls `GET /api/validation-evidence`.
- Shows Gmsh / Meep / MPB / Optiland Level 3 and Elmer deferred.

## 5. Example Gallery

- Calls `GET /api/examples`.
- Calls `GET /api/examples/{example_id}`.
- Calls `POST /api/examples/{example_id}/agent-trace`.
- Shows bundled optical design examples, material suggestions, adapter
  recommendations, workflow focus, maturity notes, and safety boundaries.
- Does not run solvers or call external LLMs.

## 6. Workflow Plan

- Calls `POST /api/workflow-plan`.
- Shows plan steps, diagnostics, and no solver execution.
- Includes a workflow fixture loader.

## 7. Artifact Preview

- Calls `POST /api/adapter-preview`.
- Shows preview content and artifact summary.
- Includes a minimal spec fixture loader and output language/extension summary.
- Never runs solver by default.

## 8. Validation Evidence

- Calls `GET /api/validation-evidence`.
- Shows evidence reports and limitations.

## 9. API / System Status

- Calls `GET /api/health`.
- Calls `GET /api/version`.
- Shows `api_contract_version`.
- Shows API mode indicator and API base URL.

## MVP boundaries

- Frontend should be single-user local-first.
- No authentication required for MVP.
- No cloud dependency.
- No solver execution by default.
- Optional Playwright visual smoke covers these seven pages manually and is not
  a default release gate.

## 10. Material Library

- Calls `GET /api/materials`.
- Calls `POST /api/materials/suggest`.
- Shows local preview materials and material suggestions.
- Shows related examples where applicable.
- States material data is not production-grade optical constants.

## 11. Agent Collaboration

- Calls `POST /api/agent-trace`.
- Calls `POST /api/examples/{example_id}/agent-trace`.
- Shows SpecAgent, MaterialAgent, GeometryAgent, AdapterAgent, WorkflowAgent,
  EvidenceAgent, SafetyAgent, and RecommendationAgent.
- Shows timeline step index, input summary, output summary, diagnostics,
  evidence refs, recommended next actions, final recommendation, and safety
  boundaries.
