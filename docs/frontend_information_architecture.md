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

## 2. Spec Input

- Calls `POST /api/parse`.
- Calls `POST /api/validate`.
- Shows parsed spec, validation status, and diagnostics.

## 3. Adapter Matrix

- Calls `GET /api/adapters`.
- Calls `GET /api/validation-evidence`.
- Shows Gmsh / Meep / MPB / Optiland Level 3 and Elmer deferred.

## 4. Workflow Plan

- Calls `POST /api/workflow-plan`.
- Shows plan steps, diagnostics, and no solver execution.

## 5. Artifact Preview

- Calls `POST /api/adapter-preview`.
- Shows preview content and artifact summary.
- Never runs solver by default.

## 6. Validation Evidence

- Calls `GET /api/validation-evidence`.
- Shows evidence reports and limitations.

## 7. API / System Status

- Calls `GET /api/health`.
- Calls `GET /api/version`.
- Shows `api_contract_version`.

## MVP boundaries

- Frontend should be single-user local-first.
- No authentication required for MVP.
- No cloud dependency.
- No solver execution by default.
