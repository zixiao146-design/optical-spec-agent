# Draft Release Notes v0.9.0

> Release-candidate notes. `0.9.0rc1` is prepared in package metadata, but no
> GitHub release or git tag has been created.

## Summary

Draft v0.9 covers the accumulated main-branch release-candidate surface:

- v0.6 diagnostics
- v0.7 adapters
- v0.8 LLM parser foundation
- v0.9 workflow orchestration preview
- release engineering quality gates

v0.9 adds a synchronous, local workflow orchestration foundation that connects
the existing parser, validator, adapter, diagnostics, execution-planning, and
reporting capabilities into auditable runs.

## New

- `optical-spec diagnose` for post-hoc physical diagnostics.
- `optical-spec adapter-list` and `optical-spec adapter-generate` for
  solver-native scaffold generation.
- `optical-spec llm-eval` for deterministic mock LLM parser evaluation.
- `WorkflowRun`, `WorkflowStepResult`, `WorkflowArtifact`, and `WorkflowPlan` models.
- Workflow agents for intake, parsing, validation, adapter selection, generation,
  execution planning, optional Meep execution, diagnostics, evaluation, human
  review, and reporting.
- CLI:
  - `optical-spec workflow-plan`
  - `optical-spec workflow-run`
  - `optical-spec workflow-replay`
  - `optical-spec workflow-report`
- API:
  - `POST /workflow/plan`
  - `POST /workflow/run`
  - `POST /workflow/report`
- Standard artifact layout with `workflow_run.json` as source of truth.
- Human review checklist.
- Replay report.
- Workflow benchmark:
  - `benchmarks/workflow_cases.json`
  - `benchmarks/run_workflow_benchmark.py`
  - `make workflow-check`
- CI workflows for local quality gates, benchmarks, docs checks, and release
  dry-run builds.
- Release engineering scripts and contracts:
  - CLI surface check
  - docs consistency check
  - release readiness check
  - artifact contract check
  - CLI/API/benchmark/artifact contract docs

## Preserved

- Existing parse/validate/schema/example commands.
- Existing Meep commands.
- Existing diagnose command.
- Existing adapter commands.
- Existing LLM eval command.

## Verification Status

Most recent known local verification:

- `pip install -e ".[dev]"`: passed
- `pytest -q`: 329 passed, 4 warnings
- key_fields benchmark: 16/16 passed
- semantic benchmark: 27/27 passed
- LLM benchmark: 40/40 passed
- workflow benchmark: 12/12 passed
- `make check`: passed
- `docs-check`: ready
- `cli-check`: ready
- `release-check`: ready after the `0.9.0rc1` version bump
- `artifact-check`: ready
- `python -m build`: passed
- `twine check dist/*`: passed

## Limitations

- Synchronous/local only.
- No async queue or cloud execution.
- No external LLM provider required by default.
- Mock LLM provider is deterministic and not proof of real model quality.
- No automatic MPB/Gmsh/Elmer/Optiland execution.
- Meep execution remains optional/local.
- No production-grade physical validation.
- No formal convergence proof.
- Adapter outputs remain MVP scaffolds where applicable.
- Release/tag creation remains manual.

## Recommended Release Label

Use `0.9.0rc1` as the public candidate label for the current main-branch
surface if maintainers approve manual tag/release creation.

No GitHub release, git tag, PyPI publication, or final `0.9.0` release has been
created.
