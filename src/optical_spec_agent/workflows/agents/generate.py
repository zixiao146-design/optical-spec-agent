"""Workflow generation agent."""

from __future__ import annotations

from optical_spec_agent.workflows.agents.base import WorkflowAgent, WorkflowContext
from optical_spec_agent.workflows.artifacts import artifact_from_path, write_json, write_text
from optical_spec_agent.workflows.models import AgentResult


class GenerationAgent(WorkflowAgent):
    """Generate solver-native input scaffold without running external solvers."""

    name = "generation"

    def run(self, context: WorkflowContext) -> AgentResult:
        if context.current_spec is None:
            return self._skip_or_error(context, reason="No spec available for generation.")
        if context.selected_adapter is None:
            return self._skip_or_error(context, reason="No adapter selected for generation.")

        adapter = context.selected_adapter
        try:
            if adapter.tool_name == "elmer":
                result = adapter.generate(context.current_spec)
            else:
                result = adapter.generate(context.current_spec)
        except Exception as exc:  # noqa: BLE001 - keep non-strict workflow auditable.
            return self._skip_or_error(context, reason=f"{type(exc).__name__}: {exc}")

        extension = adapter.metadata().output_extension or ".txt"
        output_path = context.dirs["artifacts"] / f"generated_input{extension}"
        write_text(output_path, result.content)
        result.generated_files["primary"] = str(output_path)
        context.generated_files["primary"] = str(output_path)

        report = {
            "tool": result.tool,
            "language": result.language,
            "output_path": str(output_path),
            "missing_required": result.missing_required,
            "warnings": result.warnings,
            "errors": result.errors,
            "defaults_applied": result.defaults_applied,
            "limitations": result.limitations,
            "generated_files": result.generated_files,
        }
        report_path = context.dirs["artifacts"] / "generation_report.json"
        write_json(report_path, report)
        artifacts = {
            "generated_input": artifact_from_path(
                name="generated_input",
                path=output_path,
                output_dir=context.output_dir,
                artifact_type="solver_input",
                producer_step=self.name,
                description="Generated solver-native input scaffold.",
                required=True,
            ),
            "generation_report.json": artifact_from_path(
                name="generation_report.json",
                path=report_path,
                output_dir=context.output_dir,
                artifact_type="generation_report",
                producer_step=self.name,
                description="Adapter generation report.",
            ),
        }
        warnings = [*result.warnings, *result.defaults_applied, *result.missing_required]
        status = (
            "error"
            if result.errors and context.config.strict
            else "warning"
            if result.errors or warnings
            else "success"
        )
        return AgentResult(
            status=status,
            payload=report,
            artifacts=artifacts,
            warnings=warnings,
            errors=result.errors if context.config.strict else [],
            limitations=result.limitations,
        )

    def _skip_or_error(self, context: WorkflowContext, *, reason: str) -> AgentResult:
        payload = {"skipped": True, "reason": reason}
        path = context.dirs["artifacts"] / "generation_skipped.json"
        write_json(path, payload)
        artifacts = {
            "generation_skipped.json": artifact_from_path(
                name="generation_skipped.json",
                path=path,
                output_dir=context.output_dir,
                artifact_type="generation_report",
                producer_step=self.name,
                description="Generation skip or failure reason.",
            )
        }
        return AgentResult(
            status="error" if context.config.strict else "warning",
            payload=payload,
            artifacts=artifacts,
            warnings=[] if context.config.strict else [reason],
            errors=[reason] if context.config.strict else [],
        )
