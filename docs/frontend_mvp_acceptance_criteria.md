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

## 2. Safety criteria

- UI must show no-default-solver boundary.
- UI must show no-default-LLM boundary.
- UI must not expose PyPI/TestPyPI upload button.
- UI must not expose tag/release button.
- UI must not imply production-grade validation.
- UI must not imply formal convergence proof.

## 3. Technical criteria

- Local-first.
- No cloud backend.
- No login system.
- API base configurable.
- Uses API contract version 0.1.
- Uses `examples/api` fixtures for initial development.
- No generated build artifacts committed.

## 4. Not required for MVP

- Solver execution.
- External LLM.
- Multi-user accounts.
- 3D visualization.
- Optimization UI.
- PyPI/release operations.

## Implementation evidence

- Frontend source exists under `frontend/`.
- API base URL is configurable with `VITE_API_BASE_URL`.
- The MVP uses Local Agent API endpoints only.
- Build outputs, `node_modules`, and generated artifacts must not be committed.
