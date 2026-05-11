"""Workflow self-evaluation agent."""

from __future__ import annotations

from optical_spec_agent.workflows.agents.base import WorkflowAgent, WorkflowContext
from optical_spec_agent.workflows.artifacts import artifact_from_path, write_json
from optical_spec_agent.workflows.models import AgentResult, WORKFLOW_EVALUATION_SCHEMA_VERSION


class EvaluationAgent(WorkflowAgent):
    """Evaluate workflow completeness, not physical correctness."""

    name = "evaluation"

    def run(self, context: WorkflowContext) -> AgentResult:
        checks = [
            _check("input_nonempty", bool(context.input_text.strip())),
            _check("spec_generated", (context.dirs["artifacts"] / "spec.json").exists()),
            _check("spec_validated", context.validation_result is not None),
            _check("missing_fields_collected", context.current_spec is not None),
            _check(
                "parser_report_exists_when_expected",
                context.config.parser == "rule" or (context.dirs["artifacts"] / "parser_report.json").exists(),
                warning=True,
            ),
            _check("adapter_selected", context.selected_adapter is not None, warning=True),
            _check("generated_input_exists", bool(context.generated_files), warning=True),
            _check(
                "diagnostics_generated_or_not_applicable",
                (context.dirs["artifacts"] / "execution_diagnostics.json").exists()
                or (context.dirs["artifacts"] / "diagnostics_not_applicable.json").exists(),
                warning=True,
            ),
            _check(
                "no_solver_execution_claim_without_execution_artifact",
                not context.config.allow_execute
                or (context.output_dir / "execution" / "execution_result.json").exists()
                or context.selected_tool != "meep",
            ),
            _check("limitations_declared", bool(context.limitations), warning=True),
            _check("no_external_api_used_by_default", context.config.llm_provider in {"mock", "disabled"}),
        ]
        failed = [item for item in checks if item["status"] == "error"]
        warning_checks = [item for item in checks if item["status"] == "warning"]
        payload = {
            "schema_version": WORKFLOW_EVALUATION_SCHEMA_VERSION,
            "checks": checks,
            "passed_checks": len([item for item in checks if item["status"] == "success"]),
            "failed_checks": len(failed),
            "warning_checks": len(warning_checks),
            "score": round(len([item for item in checks if item["status"] == "success"]) / len(checks), 3),
            "status": "error" if failed else "warning" if warning_checks else "success",
            "warnings": [item["name"] for item in warning_checks],
            "errors": [item["name"] for item in failed],
        }
        path = context.dirs["artifacts"] / "workflow_evaluation.json"
        write_json(path, payload)
        artifacts = {
            "workflow_evaluation.json": artifact_from_path(
                name="workflow_evaluation.json",
                path=path,
                output_dir=context.output_dir,
                artifact_type="evaluation",
                producer_step=self.name,
                description="Workflow completeness checks, not physics validation.",
                required=True,
            )
        }
        return AgentResult(
            status=payload["status"],
            payload=payload,
            artifacts=artifacts,
            warnings=payload["warnings"],
            errors=payload["errors"],
            notes=["Workflow evaluation checks engineering completeness, not physical correctness."],
        )


def _check(name: str, passed: bool, *, warning: bool = False) -> dict:
    if passed:
        status = "success"
    else:
        status = "warning" if warning else "error"
    return {"name": name, "status": status}
