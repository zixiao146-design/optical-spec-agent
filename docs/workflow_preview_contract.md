# Workflow Preview Contract

Version scope: current public prerelease `v0.9.0rc4`; current `main`
development version `0.9.0rc5.dev0`. `v0.9.0rc5.dev0` is not a release, the
`v0.9.0rc5` tag has not been created, and PyPI/TestPyPI remain unpublished.
Continue v1.0 readiness engineering and prepare a `v0.9.0rc5.dev0` development version
only when accumulated changes should be published as another RC.

Workflow orchestration is a local, synchronous preview layer. It coordinates
existing parser, validator, adapter, diagnostics, review, replay, and report
steps. It is not a background worker, cloud execution system, or autonomous
solver platform.

## Supported operations

- `workflow-plan`: create a lightweight plan and expected artifact list.
- `workflow-run`: execute local workflow agents and write `workflow_run.json`.
- `workflow-replay`: replay an existing workflow run with deterministic local
  settings.
- `workflow-report`: render workflow artifacts as Markdown or JSON.

## Dry-run and replay behavior

- Solver execution is disabled by default.
- `allow_execute=False` produces an `execution_skip.json` artifact.
- Non-Meep tools produce `diagnostics_not_applicable.json` instead of attempting
  external solver diagnostics.
- Replay compares deterministic key fields: input text, parser mode, LLM
  provider, selected tool, and status.

## Artifact expectations

Workflow runs should write:

- `workflow_plan.json`
- `workflow_run.json`
- `workflow_summary.md`
- `workflow_summary.json`
- `human_review_checklist.md`
- `steps/*.json`
- `artifacts/spec.json`
- `artifacts/validation_report.json`
- `artifacts/adapter_selection.json`
- `artifacts/generated_input.*` when generation succeeds
- `artifacts/execution_plan.json`
- `artifacts/workflow_evaluation.json`

Artifact metadata records relative path, producer step, type, existence, and
size where available.

## Default offline behavior

- No external solver is run by default.
- No external LLM provider is required by default.
- `hybrid` workflows may use the deterministic mock provider.
- Workflow output is an auditable engineering artifact, not a scientific proof.
- `examples/workflows/local_preview_request.json` is the canonical offline
  workflow-plan fixture.
- `tests/fixtures/workflow_preview/local_preview_expected_keys.json` records the
  stable top-level evidence keys for plan/run/replay checks.
- `tests/test_workflow_adapter_evidence.py` verifies that workflow planning
  includes adapter generation artifacts while remaining preview/no-execute by
  default.

## Non-goals

- No async/background orchestration.
- No cloud execution.
- No production-grade physical validation.
- No formal convergence proof.
- No automatic MPB/Gmsh/Elmer/Optiland execution.
