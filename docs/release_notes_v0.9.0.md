# Draft Release Notes v0.9.0

> Draft only. No GitHub release or tag has been created.

## Summary

v0.9 adds a synchronous, local workflow orchestration foundation that connects
the existing parser, validator, adapter, diagnostics, execution-planning, and
reporting capabilities into auditable runs.

## New

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

## Preserved

- Existing parse/validate/schema/example commands.
- Existing Meep commands.
- Existing diagnose command.
- Existing adapter commands.
- Existing LLM eval command.

## Limitations

- Synchronous/local only.
- No async queue or cloud execution.
- No external LLM provider required by default.
- No automatic MPB/Gmsh/Elmer/Optiland execution.
- Meep execution remains optional/local.
- No production-grade physical validation.
- No formal convergence proof.
- Adapter outputs remain MVP scaffolds where applicable.
