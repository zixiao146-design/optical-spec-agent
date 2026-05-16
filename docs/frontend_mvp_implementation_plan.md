# Agent Studio Frontend MVP Implementation Plan

This document is planning only. This task does not implement frontend code.
This task does not create the `frontend/` directory.

## Recommended technology stack

- React + Vite or equivalent lightweight frontend.
- TypeScript recommended.
- API base URL config.
- Local development only.

## Suggested directory layout

```text
frontend/
  package.json
  src/
    App.tsx
    api/
    components/
    pages/
    fixtures/
```

This task does not create the directory and does not implement frontend.

## Implementation phases

1. Scaffold frontend.
2. Connect health/version/readiness.
3. Adapter matrix.
4. Spec input / validate.
5. Workflow plan.
6. Adapter preview.
7. Evidence view.
8. Polish / docs.

## Guardrails for implementation task

- Do not add upload, publish, tag, or release controls.
- Do not run external solvers by default.
- Do not call external LLMs by default.
- Do not imply production-grade physical validation.
- Do not imply formal convergence proof.
- Do not commit `node_modules` or frontend build artifacts.
