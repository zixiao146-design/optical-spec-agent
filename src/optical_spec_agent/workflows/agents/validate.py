"""Workflow validation agent."""

from __future__ import annotations

from optical_spec_agent.validators.spec_validator import SpecValidator
from optical_spec_agent.workflows.agents.base import WorkflowAgent, WorkflowContext
from optical_spec_agent.workflows.artifacts import artifact_from_path, write_json
from optical_spec_agent.workflows.models import AgentResult


class ValidateAgent(WorkflowAgent):
    """Run SpecValidator and write a validation report."""

    name = "validate"

    def run(self, context: WorkflowContext) -> AgentResult:
        if context.current_spec is None:
            return AgentResult(status="error", errors=["No spec available for validation."])

        spec = SpecValidator().validate(context.current_spec)
        context.current_spec = spec
        report = {
            "is_executable": spec.validation_status.is_executable,
            "errors": spec.validation_status.errors,
            "warnings": spec.validation_status.warnings,
            "missing_fields": spec.missing_fields,
            "confirmed_fields": spec.confirmed_fields,
            "inferred_fields": spec.inferred_fields,
        }
        context.validation_result = report
        report_path = context.dirs["artifacts"] / "validation_report.json"
        write_json(report_path, report)
        artifacts = {
            "validation_report.json": artifact_from_path(
                name="validation_report.json",
                path=report_path,
                output_dir=context.output_dir,
                artifact_type="validation",
                producer_step=self.name,
                description="SpecValidator result.",
                required=True,
            )
        }
        # SpecValidator errors mean "not directly executable" for the generic
        # spec contract. In non-strict workflow mode we keep going so adapters
        # can still produce reviewable scaffolds.
        status = (
            "error"
            if report["errors"] and context.config.strict
            else "warning"
            if report["errors"] or report["warnings"]
            else "success"
        )
        return AgentResult(
            status=status,
            payload=report,
            artifacts=artifacts,
            warnings=[*report["warnings"], *report["errors"]],
            errors=report["errors"] if context.config.strict else [],
        )
