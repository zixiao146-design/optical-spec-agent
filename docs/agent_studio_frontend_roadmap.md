# Agent Studio Frontend Roadmap

## Purpose

A future frontend should make the project feel like an agent by visualizing spec
parsing, validation, adapter selection, workflow planning, artifact preview, and
validation evidence.

## Current status

- Not part of v1.0.0 release criteria.
- Not required for v1.0.0.
- This is not a v1.0.0 release blocker.
- Local Agent API readiness is in progress through
  `docs/api_agent_contract.md` and `docs/cli_api_parity.md`.
- API response models exist in `src/optical_spec_agent/api/models.py`.
- Current `api_contract_version`: 0.1.
- API versioning and request validation are documented in
  `docs/api_versioning_policy.md` and `docs/api_request_validation_contract.md`.
- Local API launch guidance is documented in `docs/api_local_launch_guide.md`.
- Frontend handoff details are documented in `docs/frontend_handoff_spec.md`.
- Copyable local curl examples are documented in `docs/api_curl_examples.md`.
- Frontend MVP planning exists in `docs/frontend_mvp_product_spec.md`,
  `docs/frontend_information_architecture.md`,
  `docs/frontend_api_mapping.md`, `docs/frontend_mvp_user_flows.md`,
  `docs/frontend_mvp_acceptance_criteria.md`,
  `docs/frontend_safety_policy.md`, and
  `docs/frontend_mvp_implementation_plan.md`.
- Frontend MVP implementation exists under `frontend/`.
- Frontend MVP runbook: `docs/frontend_mvp_runbook.md`.
- Frontend MVP QA checklist: `docs/frontend_mvp_qa_checklist.md`.
- Frontend fixture examples exist under `examples/api/`.
- Fixture consistency is checked by `scripts/check_api_fixtures.py`.
- API smoke coverage is checked by `scripts/smoke_agent_api.sh`.
- Frontend smoke coverage is checked by `scripts/smoke_frontend_mvp.sh`.
- React + Vite + TypeScript MVP scaffold exists and remains local-first.
- Loading, empty, error, API disconnected, and demo fixture states exist for
  local demos and continued development.
- Fixture loading buttons, API mode indicator, diagnostics panels, recommended
  action panels, and collapsible JSON payloads improve live API ergonomics.
- Optional Playwright visual smoke is documented in
  `docs/frontend_visual_smoke_plan.md` and
  `docs/frontend_visual_smoke_runbook.md`; it remains manual and outside the
  default release gate.
- Maintainer-facing local demo package exists through
  `scripts/demo_agent_studio.sh`, `docs/agent_studio_demo_runbook.md`,
  `docs/agent_studio_demo_checklist.md`,
  `docs/agent_studio_demo_storyboard.md`, and
  `docs/agent_studio_demo_troubleshooting.md`.
- Demo review capture and hardening backlog are tracked in
  `docs/agent_studio_demo_feedback.md` and
  `docs/frontend_hardening_backlog.md`.
- Quickstart onboarding is documented in `docs/quickstart.md` and
  `docs/quickstart.zh-CN.md`, with setup/run scripts
  `scripts/bootstrap_demo_env.sh` and `scripts/run_quickstart_demo.sh`.
- English / 中文 frontend localization is documented in
  `docs/frontend_i18n_zh_CN.md`; UI copy, guided demo, and safety boundaries
  are localized while API JSON field names, adapter tool names, and
  `api_contract_version` remain stable.
- Material Library and Agent Collaboration trace are available as preview-first
  optical-design domain expansion.
- No full production frontend, cloud backend, login system, solver-run control,
  external LLM control, upload control, or tag/release control is included.
- Agent Studio frontend should call the local Agent API instead of shelling out
  directly to the CLI.
- Should follow API readiness and continued backend contract tests.
- Should remain local-first and no-default-solver.
- The API and future frontend must not run external solvers, call external
  LLMs, require proprietary tools, or access the network by default.

## Recommended phases

### Phase 1.5

- API readiness.
- FastAPI endpoints.
- API contract tests.
- No-solver/no-LLM default behavior.
- API endpoints for health/version, adapter registry, schema, parse, validate,
  workflow-plan, adapter-preview, validation evidence, and readiness/status.
- API response model and fixture coverage for frontend mock data.
- Local launch guide, curl examples, and live fixture consistency checks.
- Frontend MVP product spec, information architecture, API mapping, user
  flows, acceptance criteria, safety policy, and implementation plan.
- Frontend QA checklist and smoke script.

### Phase 2

- Frontend MVP.
- Spec input.
- Adapter matrix.
- Workflow plan.
- Artifact preview.
- Validation evidence view.
- Dashboard/readiness and system status views.
- Local API base URL configuration with `VITE_API_BASE_URL`.
- Loading, empty, error, and API disconnected states.
- Demo fixture mode that is explicitly not live validation.
- Fixture-backed form defaults and live API/demo mode clarity.
- Diagnostics and recommended next actions.
- Optional/manual Playwright visual smoke for major local pages and safety copy.
- Local maintainer demo package that ties API launch, frontend launch, smoke
  checks, optional visual smoke, and a guided walkthrough together.
- Demo feedback review loop and prioritized hardening backlog.
- Guided quickstart panel and quickstart completion checklist for first-time
  local users.
- English / 中文 language switcher and Chinese guided demo copy.
- Example Gallery for bundled optical design examples.
- Material Library connections to examples and applications.
- Agent Trace Timeline showing sub-agent input/output, diagnostics, evidence,
  safety notes, and recommended next actions.

### Phase 3

- Agent Studio.
- Session history.
- Approval gates.
- Optional solver panel.
- Report export.

## Non-goals for frontend MVP

- No cloud requirement.
- No login system.
- No default solver execution.
- No proprietary solver dependency.
- No production-grade claim.
- No formal convergence proof claim.
