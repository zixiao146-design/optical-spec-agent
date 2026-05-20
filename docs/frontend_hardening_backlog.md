# Frontend Hardening Backlog

## Current Status

- Current public prerelease: v0.9.0rc8
- Current main development version: 0.9.0rc9.dev0
- Agent Studio demo package: exists
- Demo was run locally: yes
- PyPI published: no
- v0.9.0rc9 tag: not created
- v1.0.0 tag: not created

## P0 Must Fix Before Public Demo

- Chinese step-by-step tutorial before any public demo:
  `docs/agent_studio_chinese_guided_tutorial.md`.
- Chinese tutorial entry in the frontend.
- Tutorial stepper with the full local agent workflow.
- Per-step operation instructions.
- Per-step expected results.
- Per-step API endpoint reference.
- Per-step safety boundary.
- One-click Chinese nanoparticle example loading.
- Tutorial completion state / next-step suggestions.
- Confirm no PyPI/TestPyPI upload controls, tag controls, release controls,
  solver-run controls, or external LLM controls are visible.

## P1 Important Polish

- 待进一步 demo 反馈确认.

## P2 Future Enhancement

- 待进一步 demo 反馈确认.

## Feedback Discipline

- Do not invent page-by-page issues that were not provided.
- Current real feedback is limited to: "还是很粗糙简陋" and the P0 need for a
  Chinese step-by-step tutorial before public demo.
- Add page-specific P1/P2 items only after the next demo produces concrete
  observations.

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
