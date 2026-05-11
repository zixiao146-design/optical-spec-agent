"""Synchronous local workflow runner for v0.9 orchestration."""

from __future__ import annotations

from time import perf_counter

from optical_spec_agent.workflows.agents import (
    AdapterSelectionAgent,
    DiagnosticsAgent,
    EvaluationAgent,
    ExecutionPlanAgent,
    GenerationAgent,
    HumanReviewAgent,
    IntakeAgent,
    OptionalMeepExecutionAgent,
    ParseAgent,
    ReportAgent,
    ValidateAgent,
    WorkflowAgent,
    WorkflowContext,
)
from optical_spec_agent.workflows.artifacts import (
    artifact_from_path,
    ensure_workflow_dirs,
    write_json,
)
from optical_spec_agent.workflows.models import (
    AgentResult,
    WorkflowPlan,
    WorkflowRun,
    WorkflowRunnerConfig,
    WorkflowStepResult,
    make_workflow_run_id,
    utc_now_iso,
)


class WorkflowRunner:
    """Run a deterministic, synchronous local workflow."""

    def __init__(
        self,
        config: WorkflowRunnerConfig,
        *,
        agents: list[WorkflowAgent] | None = None,
    ) -> None:
        self.config = config
        self.agents = agents or [
            IntakeAgent(),
            ParseAgent(),
            ValidateAgent(),
            AdapterSelectionAgent(),
            GenerationAgent(),
            ExecutionPlanAgent(),
            OptionalMeepExecutionAgent(),
            DiagnosticsAgent(),
            EvaluationAgent(),
            HumanReviewAgent(),
            ReportAgent(),
        ]

    def run(self, input_text: str) -> WorkflowRun:
        """Execute the configured workflow and write workflow_run.json."""
        output_dir = self.config.output_dir
        dirs = ensure_workflow_dirs(output_dir)
        run_id = make_workflow_run_id()
        context = WorkflowContext(
            input_text=input_text,
            output_dir=output_dir,
            config=self.config,
            run_id=run_id,
            dirs=dirs,
            selected_tool=self.config.tool,
        )
        plan_path = output_dir / "workflow_plan.json"
        write_json(
            plan_path,
            WorkflowPlan(
                input_text=input_text,
                planned_steps=[agent.name for agent in self.agents],
                parser_mode=self.config.parser,
                selected_tool=self.config.tool,
                execute_policy="execute_meep" if self.config.allow_execute else "no_execute",
                expected_artifacts=[
                    "input.txt",
                    "workflow_run.json",
                    "workflow_summary.md",
                    "workflow_summary.json",
                    "human_review_checklist.md",
                    "artifacts/spec.json",
                    "artifacts/generated_input.*",
                    "artifacts/workflow_evaluation.json",
                ],
                risk_flags=["human_review_required"],
                limitations=["Workflow v0.9 is synchronous/local orchestration only."],
            ),
        )
        context.workflow_artifacts["workflow_plan.json"] = artifact_from_path(
            name="workflow_plan.json",
            path=plan_path,
            output_dir=output_dir,
            artifact_type="workflow_plan",
            producer_step="runner",
            description="Planned workflow steps for this run.",
            required=True,
        )

        steps: list[WorkflowStepResult] = []
        for index, agent in enumerate(self.agents, start=1):
            step_id = f"{index:02d}_{agent.name}"
            step = self._run_agent(agent, context=context, step_id=step_id)
            steps.append(step)
            context.workflow_artifacts.update(step.artifacts)
            context.warnings.extend(step.warnings)
            context.errors.extend(step.errors)
            if step.status == "error" and self.config.strict:
                break
            if step.status == "warning" and not self.config.continue_on_warning:
                break

        final_status = _final_status(steps)
        workflow = WorkflowRun(
            run_id=run_id,
            created_at=utc_now_iso(),
            input_text=input_text,
            parser_mode=self.config.parser,
            llm_provider=self.config.llm_provider,
            selected_tool=context.selected_tool,
            output_dir=str(output_dir),
            status=final_status,
            steps=steps,
            artifacts=context.workflow_artifacts,
            warnings=list(dict.fromkeys(context.warnings)),
            errors=list(dict.fromkeys(context.errors)),
            assumptions=list(dict.fromkeys(context.assumptions)),
            limitations=list(dict.fromkeys(context.limitations)),
        )
        workflow_path = output_dir / "workflow_run.json"
        write_json(workflow_path, workflow)
        workflow.artifacts["workflow_run.json"] = artifact_from_path(
            name="workflow_run.json",
            path=workflow_path,
            output_dir=output_dir,
            artifact_type="workflow_run",
            producer_step="runner",
            description="Top-level v0.9 workflow source-of-truth artifact.",
            required=True,
        )
        write_json(workflow_path, workflow)
        return workflow

    def _run_agent(
        self,
        agent: WorkflowAgent,
        *,
        context: WorkflowContext,
        step_id: str,
    ) -> WorkflowStepResult:
        started_at = utc_now_iso()
        start = perf_counter()
        try:
            result = agent.run(context)
        except Exception as exc:  # noqa: BLE001 - agents should convert unexpected errors.
            result = AgentResult(status="error", errors=[f"{type(exc).__name__}: {exc}"])
        finished_at = utc_now_iso()
        duration_ms = round((perf_counter() - start) * 1000, 3)
        step = WorkflowStepResult(
            step_id=step_id,
            agent_name=agent.name,
            status=result.status,
            started_at=started_at,
            finished_at=finished_at,
            duration_ms=duration_ms,
            inputs_summary={
                "parser": context.config.parser,
                "tool": context.config.tool,
                "selected_tool": context.selected_tool,
            },
            outputs_summary=result.payload,
            artifacts=result.artifacts,
            warnings=result.warnings,
            errors=result.errors,
            notes=result.notes,
        )
        write_json(context.dirs["steps"] / f"{step_id}.json", step)
        return step


def _final_status(steps: list[WorkflowStepResult]) -> str:
    if any(step.status == "error" for step in steps):
        return "error"
    if any(step.status == "warning" for step in steps):
        return "warning"
    return "success"
