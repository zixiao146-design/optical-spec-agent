# Agent Command Center

## Purpose

Agent Command Center is the task-driven Agent Studio surface for local optical design work. It turns a natural language goal into a deterministic local task session:

```text
user goal -> optical intent -> design case -> materials -> adapters -> workflow -> artifacts -> evidence -> next actions
```

It is inspired by coding-agent style task sessions, but it is not a clone of any external product and does not copy external branding, wording, or assets.

## Current Status

- Current public prerelease: v0.9.0rc6
- Current main development version: 0.9.0rc7.dev0
- API contract version: 0.1
- PyPI: not published
- v0.9.0rc7 tag: not created
- v1.0.0 tag: not created

## API

The command center uses:

- `POST /api/agent-session`
- `GET /api/examples`
- `GET /api/materials`
- `POST /api/materials/suggest`
- `POST /api/workflow-plan`
- `POST /api/adapter-preview`
- `GET /api/validation-evidence`

`POST /api/agent-session` accepts a local goal, optional local example ID, and optional language hint. It returns an Agent Task Session with task plan steps, sub-agent trace, permission gates, local artifacts, evidence, and recommended next actions.

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
- `final_recommendation`
- `recommended_next_actions`

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

## Safety Boundaries

- No external solver execution by default.
- No external LLM call by default.
- No proprietary solver dependency by default.
- No PyPI/TestPyPI publication controls.
- No GitHub tag/release controls.
- No production-grade physical validation claim.
- No formal convergence proof claim.
- Material data remains preview/design-assist and must be independently verified.

