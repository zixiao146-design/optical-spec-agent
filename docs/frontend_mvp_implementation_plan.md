# Agent Studio Frontend MVP Implementation Plan

This document records the implementation plan used for the first local Agent
Studio Frontend MVP. The MVP scaffold now exists under `frontend/`, while
production deployment, solver execution, upload/release controls, login, cloud
backend, optimization dashboards, and complex 3D visualization remain outside
scope.

## Recommended technology stack

- React + Vite or equivalent lightweight frontend.
- TypeScript recommended.
- API base URL config.
- Local development only.

## Implemented directory layout

```text
frontend/
  package.json
  index.html
  vite.config.ts
  src/
    App.tsx
    api/
    components/
    pages/
    fixtures/
```

The implementation uses the existing Local Agent API and defaults to
`http://127.0.0.1:8000` through `VITE_API_BASE_URL`.

## Implementation phases

1. Scaffold frontend. Completed.
2. Connect health/version/readiness. Completed.
3. Adapter matrix. Completed.
4. Spec input / validate. Completed.
5. Workflow plan. Completed.
6. Adapter preview. Completed.
7. Evidence view. Completed.
8. Polish / docs. Initial MVP completed.
9. Loading / empty / error / API disconnected state hardening. Completed.
10. Demo fixture mode for local walkthroughs when API is unavailable. Completed.
11. Frontend smoke script and QA checklist. Completed.

## Guardrails for implementation task

- Do not add upload, publish, tag, or release controls.
- Do not run external solvers by default.
- Do not call external LLMs by default.
- Do not imply production-grade physical validation.
- Do not imply formal convergence proof.
- Do not commit `node_modules` or frontend build artifacts.
- Keep `VITE_API_BASE_URL` local by default.
- Demo fixture mode must be visibly labeled as not live validation.
- Loading, error, and disconnected states must preserve safety boundaries.
