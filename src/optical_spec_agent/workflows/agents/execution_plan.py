"""Workflow execution-plan and optional Meep execution agents."""

from __future__ import annotations

from pathlib import Path

from optical_spec_agent.execution import run_meep_script
from optical_spec_agent.workflows.agents.base import WorkflowAgent, WorkflowContext
from optical_spec_agent.workflows.artifacts import artifact_from_path, write_json
from optical_spec_agent.workflows.models import AgentResult


class ExecutionPlanAgent(WorkflowAgent):
    """Write an execution plan without running external solvers."""

    name = "execution_plan"

    def run(self, context: WorkflowContext) -> AgentResult:
        tool = context.selected_tool or context.config.tool
        unsupported = tool in {"mpb", "gmsh", "elmer", "optiland"}
        plan = {
            "allow_execute": context.config.allow_execute,
            "selected_tool": tool,
            "execution_supported": tool == "meep",
            "default_policy": "no external solver execution by default",
            "will_execute": bool(context.config.allow_execute and tool == "meep"),
            "warnings": [],
            "limitations": [
                "Workflow v0.9 is synchronous/local orchestration, not solver automation.",
                "External solver execution is not supported for MPB/Gmsh/Elmer/Optiland.",
            ],
        }
        if unsupported:
            plan["warnings"].append(
                f"{tool} execution is unsupported in workflow v0.9; scaffold generation only."
            )
        if not context.config.allow_execute:
            plan["warnings"].append("Solver execution disabled by default (--no-execute).")
        path = context.dirs["artifacts"] / "execution_plan.json"
        write_json(path, plan)
        artifacts = {
            "execution_plan.json": artifact_from_path(
                name="execution_plan.json",
                path=path,
                output_dir=context.output_dir,
                artifact_type="execution_plan",
                producer_step=self.name,
                description="Explicit solver execution policy for this workflow.",
                required=True,
            )
        }
        return AgentResult(
            status="warning" if plan["warnings"] else "success",
            payload=plan,
            artifacts=artifacts,
            warnings=plan["warnings"],
            limitations=plan["limitations"],
        )


class OptionalMeepExecutionAgent(WorkflowAgent):
    """Optionally run generated Meep scripts through the existing execution harness."""

    name = "execution"

    def run(self, context: WorkflowContext) -> AgentResult:
        if not context.config.allow_execute:
            return self._write_skip(context, reason="Execution disabled by workflow configuration.")
        if context.selected_tool != "meep":
            return self._write_skip(
                context,
                reason=f"Execution unsupported for selected tool '{context.selected_tool}'.",
            )

        generated = context.generated_files.get("primary")
        if not generated:
            return AgentResult(status="error", errors=["No generated Meep script available."])

        result = run_meep_script(
            script_path=Path(generated),
            workdir=context.output_dir / "execution",
            timeout=300,
            expected_mode="preview",
            save_artifacts=True,
            run_id=f"{context.run_id}-meep",
        )
        path = context.output_dir / "execution" / "execution_result.json"
        artifacts = {
            "execution_result.json": artifact_from_path(
                name="execution_result.json",
                path=path,
                output_dir=context.output_dir,
                artifact_type="execution_result",
                producer_step=self.name,
                description="Optional Meep execution result.",
            )
        }
        status = "success" if result.success else "warning"
        if context.config.strict_execution and not result.success:
            status = "error"
        return AgentResult(
            status=status,
            payload=result.to_dict(),
            artifacts=artifacts,
            warnings=result.warnings,
            errors=result.errors if status == "error" else [],
            notes=["Meep execution is optional/local and not production solver automation."],
        )

    def _write_skip(self, context: WorkflowContext, *, reason: str) -> AgentResult:
        payload = {"skipped": True, "reason": reason}
        path = context.dirs["artifacts"] / "execution_skip.json"
        write_json(path, payload)
        artifacts = {
            "execution_skip.json": artifact_from_path(
                name="execution_skip.json",
                path=path,
                output_dir=context.output_dir,
                artifact_type="execution_skip",
                producer_step=self.name,
                description="Execution skip reason.",
            )
        }
        return AgentResult(status="skipped", payload=payload, artifacts=artifacts, notes=[reason])
