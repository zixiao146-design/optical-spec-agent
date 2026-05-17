# Agent Studio Frontend Information Architecture

The MVP should be a single-user, local-first interface backed by the Local Agent
API. It requires no authentication, no cloud dependency, and no solver
execution by default.
The implementation exists under `frontend/` and follows this information
architecture.

## 1. Dashboard / Readiness

- Calls `GET /api/readiness`.
- Shows current public prerelease, main development version, TestPyPI/PyPI
  status, and contract freeze status.
- Shows recommended next actions.
- Shows API mode indicator and API base URL.

## 2. Spec Input

- Calls `POST /api/parse`.
- Calls `POST /api/validate`.
- Shows parsed spec, validation status, and diagnostics.
- Includes fixture loading for local demos; fixture loading is not live
  validation until submitted.

## 3. Adapter Matrix

- Calls `GET /api/adapters`.
- Calls `GET /api/validation-evidence`.
- Shows Gmsh / Meep / MPB / Optiland Level 3 and Elmer deferred.

## 4. Workflow Plan

- Calls `POST /api/workflow-plan`.
- Shows plan steps, diagnostics, and no solver execution.
- Includes a workflow fixture loader.

## 5. Artifact Preview

- Calls `POST /api/adapter-preview`.
- Shows preview content and artifact summary.
- Includes a minimal spec fixture loader and output language/extension summary.
- Never runs solver by default.

## 6. Validation Evidence

- Calls `GET /api/validation-evidence`.
- Shows evidence reports and limitations.

## 7. API / System Status

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
