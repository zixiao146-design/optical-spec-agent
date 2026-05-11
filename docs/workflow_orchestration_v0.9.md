# v0.9 Workflow Orchestration Foundation

> Scope: synchronous, local, deterministic orchestration of existing
> `optical-spec-agent` capabilities.
>
> Non-goal: background workers, cloud execution, autonomous solver runs, or
> production-grade physical validation.

## Architecture

v0.9 adds a workflow layer around existing modules:

```text
natural language task
→ IntakeAgent
→ ParseAgent
→ ValidateAgent
→ AdapterSelectionAgent
→ GenerationAgent
→ ExecutionPlanAgent
→ OptionalMeepExecutionAgent
→ DiagnosticsAgent
→ EvaluationAgent
→ HumanReviewAgent
→ ReportAgent
→ workflow_run.json
```

All steps are synchronous. There is no queue, no background worker, and no cloud
execution.

## Agents

- `IntakeAgent`: checks input and writes `input.txt`.
- `ParseAgent`: calls `SpecService` using `rule`, `llm`, or `hybrid`.
- `ValidateAgent`: calls `SpecValidator`.
- `AdapterSelectionAgent`: selects Meep/MPB/Gmsh/Elmer/Optiland through the adapter registry.
- `GenerationAgent`: writes solver-native input scaffold.
- `ExecutionPlanAgent`: records execution policy. Default is no execution.
- `OptionalMeepExecutionAgent`: only runs Meep when explicitly enabled.
- `DiagnosticsAgent`: runs post-hoc Meep diagnostics or writes a not-applicable artifact.
- `EvaluationAgent`: checks workflow completeness, not physics correctness.
- `HumanReviewAgent`: writes a human review checklist.
- `ReportAgent`: writes Markdown and JSON summaries.

## Artifact Layout

```text
outputs/workflows/<run>/
  input.txt
  workflow_run.json
  workflow_summary.md
  workflow_summary.json
  human_review_checklist.md
  steps/
    01_intake.json
    ...
  artifacts/
    spec.json
    parser_report.json
    validation_report.json
    adapter_selection.json
    generated_input.py|.geo|.sif
    execution_plan.json
    execution_skip.json
    mesh_report.csv
    flux_report.csv
    execution_diagnostics.json
    diagnostic_preview.png
    workflow_evaluation.json
  replay/
    replay_report.json
```

`workflow_run.json` is the source of truth for the run.

## CLI

```bash
optical-spec workflow-plan "用 Meep FDTD 仿真金纳米球-金膜 gap plasmon..."

optical-spec workflow-run "用 MPB 计算二维光子晶体 band diagram，输出前 8 条能带。" \
  --parser hybrid \
  --llm-provider mock \
  --tool mpb \
  --output-dir outputs/workflows/mpb_demo \
  --no-execute

optical-spec workflow-replay outputs/workflows/mpb_demo/workflow_run.json \
  --output-dir outputs/workflows/mpb_demo_replay

optical-spec workflow-report outputs/workflows/mpb_demo/workflow_run.json \
  --output outputs/workflows/mpb_demo/report.md
```

## API

- `POST /workflow/plan`
- `POST /workflow/run`
- `POST /workflow/report`

The API defaults to no solver execution.

## SDK

```python
from pathlib import Path

from optical_spec_agent.workflows import WorkflowRunner, WorkflowRunnerConfig

runner = WorkflowRunner(
    WorkflowRunnerConfig(
        parser="hybrid",
        llm_provider="mock",
        tool="auto",
        output_dir=Path("outputs/workflows/sdk_demo"),
        allow_execute=False,
    )
)

result = runner.run("用 MPB 计算二维光子晶体 band diagram，输出前 8 条能带。")
print(result.model_dump())
```

## Replay

`workflow-replay` reads an existing `workflow_run.json`, reruns with deterministic
local settings, and writes `replay/replay_report.json`. Replay does not execute
solvers by default.

## Human Review

Every run writes `human_review_checklist.md` with missing fields, inferred
fields, adapter limitations, generated files to inspect, and recommended human
decisions before manual solver execution.

## Limitations

- Workflow orchestration is synchronous and local.
- No async background worker or cloud execution.
- No external LLM provider is required by default.
- MPB/Gmsh/Elmer/Optiland are not executed.
- Meep execution remains optional/local.
- Workflow evaluation checks engineering completeness, not physical correctness.
- No production-grade physical validation or formal convergence proof.
