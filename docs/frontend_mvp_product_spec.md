# Agent Studio Frontend MVP Product Spec

## Purpose

Agent Studio Frontend MVP is a local-first web interface that visualizes the
existing Local Agent API workflow: spec input, parsing, validation, adapter
selection, workflow planning, artifact preview, validation evidence, and
readiness status.

## Current status

- Current public prerelease: v0.9.0rc6
- Current main development version: 0.9.0rc7.dev0
- API contract version: 0.1
- Frontend implementation: MVP implemented under `frontend/`
- PyPI: not published
- v1.0.0: not released

## MVP goals

- Make the project feel like an agent by guiding the user through local spec
  interpretation, validation, planning, and review.
- Expose spec parsing and validation visually.
- Show adapter maturity and validation evidence.
- Show workflow plan steps.
- Show generated preview artifacts.
- Show validation boundaries.
- Show recommended next actions.
- Provide a polished guided quickstart demo for first-time local users.
- Show a quickstart success / next-action experience.
- Preserve the no-default-solver and no-default-LLM policy.
- Support English / 中文 UI switching for local demos while preserving stable
  English API JSON field names, adapter tool names, package metadata, and
  `api_contract_version`.

## MVP non-goals

- No cloud backend.
- No login system.
- No production deployment.
- No external solver execution by default.
- No external LLM call by default.
- No proprietary solver dependency.
- No production-grade validation claim.
- No formal convergence proof.
- No complex 3D visualization.
- No optimization dashboard.
- No multi-user session system.

## Primary users

- Optical researcher evaluating local workflow preview.
- Developer testing adapters.
- Maintainer reviewing validation evidence.
- Future frontend user needing guided workflow.

## Success criteria

- User can input or paste spec text or JSON.
- User can validate spec.
- User can see adapter matrix.
- User can generate workflow plan.
- User can preview adapter artifact.
- User can see validation evidence.
- User can see readiness and publication status.
- All views preserve safety boundary language.

## Implementation status

- React + Vite + TypeScript scaffold exists in `frontend/`.
- Frontend API client calls only the configured local API base URL and `/api/*`
  endpoints.
- The MVP includes dashboard/readiness, spec input, adapter matrix, workflow
  plan, artifact preview, validation evidence, and system status views.
- No PyPI/TestPyPI upload controls, tag/release controls, solver-run controls,
  external LLM controls, login, cloud backend, or production deployment are
  included.
- Loading, empty, error, API disconnected, and demo fixture states are included
  for local demos and continued development.
- Demo fixture mode is labeled as not live validation.
- Fixture loading buttons exist for spec input, workflow plan, and adapter
  preview forms; loading a fixture does not call the API until submitted.
- API mode indicators, diagnostics panels, recommended action panels, and
  collapsible JSON panels are included for live API ergonomics.
- A guided quickstart panel and completion checklist are included on the
  dashboard to make the first-run experience feel agent-like.
- `docs/quickstart.md`, `docs/quickstart.zh-CN.md`,
  `scripts/bootstrap_demo_env.sh`, and `scripts/run_quickstart_demo.sh` provide
  the user-facing onboarding path.
- Optional Playwright visual smoke is documented in
  `docs/frontend_visual_smoke_plan.md` and
  `docs/frontend_visual_smoke_runbook.md`.
- Playwright visual smoke is manual/optional and is not part of the default
  release gate.
- Run instructions are documented in `docs/frontend_mvp_runbook.md`.

## Optical Design Domain Expansion

The MVP now includes an Example Gallery page, a Material Library page, and an
Agent Collaboration / Agent Trace Timeline page.
The Example Gallery loads bundled examples from `examples/optical_design/` and
connects each case to material suggestions, adapter recommendations, workflow
plans, previews, evidence, and next actions.
The Material Library presents a local preview catalog and application-oriented
suggestions. The Agent Collaboration page renders SpecAgent, MaterialAgent,
GeometryAgent, AdapterAgent, WorkflowAgent, EvidenceAgent, SafetyAgent, and
RecommendationAgent as a visible timeline with input/output/diagnostics/evidence/recommendations.
These features preserve no
default solver execution, no external LLM calls, no production-grade physical
validation claim, and no formal convergence proof claim.
