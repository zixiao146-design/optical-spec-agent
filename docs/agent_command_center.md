# Agent Command Center

## Purpose

Agent Command Center is the task-driven Agent Studio surface for local optical design work. It turns a natural language goal into a deterministic local task session:

```text
user goal -> requirement template -> optical language -> design case -> materials -> adapters/calculators -> workflow -> artifacts -> evidence -> next actions
```

Compatibility summary: user goal -> optical intent -> design case.

The requirement-template layer is documented in
`docs/design_requirement_templates.md`; the optical language mapping is
documented in `docs/natural_language_to_optical_language.md`.

It is inspired by coding-agent style task sessions, but it is not a clone of any external product and does not copy external branding, wording, or assets.

## Current Status

- Current public prerelease: v0.9.0rc7
- Current main development version: 0.9.0rc8.dev0
- API contract version: 0.1
- PyPI: not published
- v0.9.0rc8 tag: not created
- v1.0.0 tag: not created

## API

The command center uses:

- `POST /api/agent-session`
- `GET /api/design-requirements`
- `POST /api/design-requirements/match`
- `GET /api/examples`
- `GET /api/materials`
- `POST /api/materials/suggest`
- `GET /api/tool-capabilities`
- `POST /api/optics/thin-film`
- `POST /api/optics/thin-film-spectrum`
- `POST /api/optics/quarter-wave-ar`
- `POST /api/optics/paraxial-lens`
- `POST /api/optics/paraxial-system`
- `POST /api/optics/two-lens-relay`
- `POST /api/optics/gaussian-beam`
- `POST /api/optics/gaussian-beam-series`
- `POST /api/optics/gaussian-beam-focus`
- `POST /api/optics/waveguide-estimate`
- `POST /api/optics/waveguide-sweep`
- `POST /api/optics/waveguide-single-mode-range`
- `POST /api/workflow-plan`
- `POST /api/adapter-preview`
- `GET /api/validation-evidence`

`POST /api/agent-session` accepts a local goal, optional local example ID, and optional language hint. It returns an Agent Task Session with task plan steps, sub-agent trace, permission gates, a tool-call ledger, local artifacts, evidence, and recommended next actions.

## Task Session Shape

An Agent Task Session includes:

- `session_id`
- `user_goal`
- `optical_intent_summary`
- `selected_example_id`
- `design_case_summary`
- `plan_steps`
- `agent_trace`
- `artifacts`
- `permission_gates`
- `tool_call_ledger`
- `final_recommendation`
- `recommended_next_actions`

The tool-call ledger records actual local Python calls such as
`material_catalog.suggest`, `example_registry.load`, `agent_trace.build`,
`workflow_plan.preview`, `adapter_preview.generate`, and applicable
`optics.*` preview calculators. It also records blocked external solver, LLM,
upload, tag, and release actions.

Case-level calculator integration now records richer design-assist calls:
thin-film coating sessions include spectrum and quarter-wave AR helpers,
waveguide sessions include V-number sweep and single-mode range helpers,
lens sessions include a two-lens relay helper, and Gaussian beam goals include
series/focus helpers. These are internal Python previews only.

## Permission Gates

Allowed by default:

- Local spec parsing
- Local material catalog lookup
- Local workflow planning
- Local adapter preview generation

Blocked or requiring explicit approval outside Agent Studio:

- External solver execution
- External LLM calls
- TestPyPI upload
- PyPI publication
- Git tag creation
- GitHub release creation

## Source / Monitor Diagnostics

Agent sessions include `source_model`, `monitor_model`, and
`optical_language_diagnostics`. The plan explicitly records:

- infer source and monitor
- check missing source/monitor inputs
- diagnose observables
- map source/monitor intent into adapter-native preview semantics
- record default assumptions
- keep `safe_to_run_solver=false`

For nanoparticle/FDTD previews, the default is a plane-wave-like source,
400-900 nm band, `linear_x` polarization, and scattering/extinction spectrum
monitor metadata. The backend can explain how this maps to Meep flux/DFT
preview metadata or Gmsh mesh-region annotations, but no external solver
monitor is executed.

## Safety Boundaries

- No external solver execution by default.
- No external LLM call by default.
- No proprietary solver dependency by default.
- No PyPI/TestPyPI publication controls.
- No GitHub tag/release controls.
- No production-grade physical validation claim.
- No formal convergence proof claim.
- Material data remains preview/design-assist and must be independently verified.
