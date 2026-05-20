# Agent Studio Demo Feedback

## Current Status

- Current public prerelease: v0.9.0rc8
- Current main development version: 0.9.0rc9.dev0
- Latest localized frontend commit reviewed: 212b880
- Agent Studio frontend localization: English / 中文
- Demo was run locally: yes
- PyPI published: no
- PyPI publication approval: not granted
- v0.9.0rc9 tag: not created
- v1.0.0 tag: not created
- GitHub release action approved: no

## Maintainer Feedback Source

- Demo date: 五月十七日
- Maintainer: MilesLee
- Overall impression: 还是很粗糙简陋
- P0: 公开演示前必须增加中文手把手教程
- P1: 待进一步 demo 反馈确认
- P2: 待进一步 demo 反馈确认

## Recorded Observations

- Demo was run locally.
- The maintainer confirmed the current Agent Studio still feels rough and
  minimal for a public-facing demo.
- The immediate P0 fix is a Chinese step-by-step guided tutorial that lets a
  Chinese user complete one full local agent workflow without maintainer
  narration.
- Page-by-page feedback has not been provided yet. Do not invent detailed page feedback;
  collect it during the next guided tutorial demo.
- Follow-up work is tracked in `docs/frontend_hardening_backlog.md`.

## Priority Summary

### P0 Must Fix Before Public Demo

- Add a Chinese step-by-step tutorial entry in the frontend.
- Document the Chinese guided tutorial in
  `docs/agent_studio_chinese_guided_tutorial.md`.
- Include per-step operation, expected result, API endpoint, and safety
  boundary.
- Add a one-click Chinese nanoparticle example load path.
- Show tutorial completion / next action guidance.

### P1 Important Polish

- Pending further demo feedback.

### P2 Future Enhancement

- Pending further demo feedback.

## Safety Boundaries Preserved

- No upload controls.
- No tag/release controls.
- No default solver execution.
- No default external LLM.
- No production-grade validation claim.
- No production-grade physical validation claim.
- No formal convergence proof claim.
- No PyPI/TestPyPI publication action.
- No GitHub release action.

## Follow-up

- Run the Chinese guided tutorial demo again after the P0 tutorial is merged.
- Record page-by-page feedback only when it is actually provided.
- Keep the Agent Studio demo package local-only until a maintainer explicitly
  approves a different scope.
