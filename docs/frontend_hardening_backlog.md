# Frontend Hardening Backlog

## Current Status

- Current public prerelease: v0.9.0rc6
- Current main development version: 0.9.0rc7.dev0
- Agent Studio demo package: exists
- Demo was run locally: yes
- PyPI published: no
- v0.9.0rc7 tag: not created
- v1.0.0 tag: not created

## P0 Must Fix Before Public Demo

- Capture concrete maintainer demo observations in
  `docs/agent_studio_demo_feedback.md` before announcing a public demo.
- Run the demo package from a clean checkout and confirm
  `./scripts/demo_agent_studio.sh` starts the API and frontend without leaving
  generated artifacts.
- Confirm API disconnected/demo fixture mode is visibly labeled as not live
  validation on every relevant page.
- Confirm all seven MVP pages keep safety copy visible:
  Dashboard / Readiness, Spec Input, Adapter Matrix, Workflow Plan, Artifact
  Preview, Validation Evidence, and System Status.
- Confirm no PyPI/TestPyPI upload controls, tag controls, release controls,
  solver-run controls, or external LLM controls are visible.
- Confirm frontend smoke, API smoke, fixture consistency, and optional
  Playwright visual smoke remain passing on the demo machine.

## P1 Important Polish

- Improve keyboard focus visibility and tab order across navigation, forms,
  JSON panels, and action buttons.
- Add clearer "live API" versus "demo fixture" page-level labels in screenshots
  and walkthrough moments.
- Improve diagnostics grouping for warnings, assumptions, missing fields, and
  recommended next actions.
- Add copy-to-clipboard affordances for selected JSON panels without requiring
  browser permissions.
- Add responsive layout checks for narrow laptop and tablet-width local demos.
- Add a guided demo mode that highlights the next page/action without adding
  cloud, login, upload, tag, release, solver, or external LLM controls.

## P2 Future Enhancement

- Add optional Playwright screenshot capture that writes only to ignored output
  directories.
- Add a generated local demo report summarizing API status, frontend status,
  fixtures used, and safety boundaries.
- Add persisted local UI preferences for API base URL and selected adapter.
- Add deeper fixture scenarios for MPB, Meep, Gmsh, Optiland, and Elmer
  deferred evidence.
- Add non-blocking visual theme polish after core workflow clarity is stable.

## Deferred / Non-goals

- PyPI/TestPyPI upload controls are deferred/non-goals.
- Tag/release controls are deferred/non-goals.
- Default solver execution is a non-goal.
- Default external LLM calls are a non-goal.
- Production-grade physical validation claims are a non-goal.
- Formal convergence proof claims are a non-goal.
- Cloud backend, login, and multi-user collaboration are deferred.
- Elmer Level 3 validation remains deferred; do not mark Elmer as Level 3.

## Safety Boundaries

- No upload controls.
- No tag/release controls.
- No default solver execution.
- No default external LLM.
- No production-grade validation claim.
- No formal convergence proof claim.
