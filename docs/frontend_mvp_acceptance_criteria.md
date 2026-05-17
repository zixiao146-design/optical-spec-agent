# Agent Studio Frontend MVP Acceptance Criteria

## 1. Functional criteria

- Can launch against local API.
- Can call all frontend-ready endpoints.
- Can render readiness state.
- Can render adapter matrix.
- Can submit parse and validate requests.
- Can render workflow plan.
- Can render adapter preview.
- Can render validation evidence.
- Can show loading, empty, error, and API disconnected states.
- Can show demo fixture mode when the local API is unavailable.
- Can load example/fixture requests into Spec Input, Workflow Plan, and Artifact
  Preview without calling the API until submitted.
- Can show API connected, API disconnected, and demo fixture mode with the API
  base URL.
- Can render diagnostics and recommended next actions consistently.

## 2. Safety criteria

- UI must show no-default-solver boundary.
- UI must show no-default-LLM boundary.
- UI must not expose PyPI/TestPyPI upload button.
- UI must not expose tag/release button.
- UI must not imply production-grade validation.
- UI must not imply formal convergence proof.
- Demo fixture mode must state that it is not live validation.
- UI must show that it does not control PyPI/TestPyPI publication or GitHub
  releases.

## 3. Technical criteria

- Local-first.
- No cloud backend.
- No login system.
- API base configurable.
- Uses API contract version 0.1.
- Uses `examples/api` fixtures for initial development.
- No generated build artifacts committed.
- Uses shared `LoadingState`, `EmptyState`, `ErrorState`, `SafetyNotice`, and
  `ApiDisconnectedNotice` components.
- Buttons are disabled while the matching local API action is loading.
- Status and error regions use `aria-live`.
- JSON panels are labeled, scrollable, and can be collapsed for scan-friendly
  local demos.
- Playwright visual smoke is documented in `docs/frontend_visual_smoke_plan.md`
  and `docs/frontend_visual_smoke_runbook.md`.
- Optional Playwright visual smoke can be run with
  `./scripts/smoke_frontend_visual.sh`.
- Playwright visual smoke remains manual and outside the default release gate.

## 4. Not required for MVP

- Solver execution.
- External LLM.
- Multi-user accounts.
- 3D visualization.
- Optimization UI.
- PyPI/release operations.
- Required Playwright screenshot automation in the default quality gates.

## Implementation evidence

- Frontend source exists under `frontend/`.
- API base URL is configurable with `VITE_API_BASE_URL`.
- The MVP uses Local Agent API endpoints only.
- The MVP has demo fixture fallback for API disconnected local demos.
- `./scripts/smoke_frontend_mvp.sh` verifies typecheck/build without committing
  generated frontend artifacts.
- `./scripts/smoke_frontend_visual.sh` verifies major pages and safety copy
  manually without committing Playwright reports.
- Build outputs, `node_modules`, and generated artifacts must not be committed.
