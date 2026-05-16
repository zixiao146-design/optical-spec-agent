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
- Frontend implementation: not started
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
- Preserve the no-default-solver and no-default-LLM policy.

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
