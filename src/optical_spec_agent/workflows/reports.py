"""Report rendering for workflow_run.json artifacts."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from optical_spec_agent.workflows.artifacts import write_json, write_text
from optical_spec_agent.workflows.models import WorkflowRun


def load_workflow_run(path: Path) -> WorkflowRun:
    """Load a workflow_run.json artifact."""
    return WorkflowRun.model_validate_json(Path(path).read_text(encoding="utf-8"))


def render_workflow_report(workflow: WorkflowRun, *, fmt: str = "markdown") -> str | dict[str, Any]:
    """Render a workflow run as Markdown or JSON-compatible dict."""
    if fmt == "json":
        return {
            "schema_version": workflow.schema_version,
            "run_id": workflow.run_id,
            "status": workflow.status,
            "input_text": workflow.input_text,
            "parser_mode": workflow.parser_mode,
            "llm_provider": workflow.llm_provider,
            "selected_tool": workflow.selected_tool,
            "artifacts": {
                name: artifact.model_dump(mode="json")
                for name, artifact in workflow.artifacts.items()
            },
            "warnings": workflow.warnings,
            "errors": workflow.errors,
            "limitations": workflow.limitations,
        }
    if fmt != "markdown":
        raise ValueError("Unsupported report format. Use markdown or json.")
    return "\n".join(
        [
            "# Optical Spec Workflow Report",
            "",
            "## Run Metadata",
            f"- Run ID: `{workflow.run_id}`",
            f"- Status: `{workflow.status}`",
            f"- Created at: `{workflow.created_at}`",
            f"- Parser: `{workflow.parser_mode}`",
            f"- LLM provider: `{workflow.llm_provider}`",
            f"- Selected tool: `{workflow.selected_tool}`",
            "",
            "## Input Task",
            workflow.input_text,
            "",
            "## Step Summary",
            *[
                f"- `{step.step_id}` / `{step.agent_name}`: `{step.status}`"
                for step in workflow.steps
            ],
            "",
            "## Generated Artifacts",
            *[
                f"- `{name}`: `{artifact.path}` (exists={artifact.exists})"
                for name, artifact in workflow.artifacts.items()
            ],
            "",
            "## Warnings",
            *_bullet_lines(workflow.warnings),
            "",
            "## Errors",
            *_bullet_lines(workflow.errors),
            "",
            "## Limitations",
            *_bullet_lines(workflow.limitations),
            "",
            "## Recommended Next Action",
            "Review `human_review_checklist.md` and generated solver input before any manual solver run.",
            "",
            "> This report is not production-grade physical validation and does not prove convergence.",
        ]
    )


def write_workflow_report(workflow_run_path: Path, *, output: Path, fmt: str = "markdown") -> Path:
    """Load workflow_run.json and write a report."""
    workflow = load_workflow_run(workflow_run_path)
    rendered = render_workflow_report(workflow, fmt=fmt)
    if fmt == "json":
        write_json(output, rendered)
    else:
        write_text(output, str(rendered))
    return output


def _bullet_lines(items: list[str]) -> list[str]:
    if not items:
        return ["- none"]
    return [f"- {item}" for item in items]
