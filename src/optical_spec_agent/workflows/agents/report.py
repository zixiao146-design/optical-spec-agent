"""Workflow summary report agent."""

from __future__ import annotations

from optical_spec_agent.workflows.agents.base import WorkflowAgent, WorkflowContext
from optical_spec_agent.workflows.artifacts import artifact_from_path, write_json, write_text
from optical_spec_agent.workflows.models import AgentResult


class ReportAgent(WorkflowAgent):
    """Write workflow_summary.md and workflow_summary.json."""

    name = "report"

    def run(self, context: WorkflowContext) -> AgentResult:
        payload = {
            "run_id": context.run_id,
            "input_text": context.input_text,
            "parser": context.config.parser,
            "llm_provider": context.config.llm_provider,
            "selected_tool": context.selected_tool,
            "validation": context.validation_result,
            "generated_files": context.generated_files,
            "warnings": context.warnings,
            "errors": context.errors,
            "limitations": sorted(set(context.limitations)),
            "next_recommended_action": "Review generated inputs and checklist before any manual solver execution.",
        }
        json_path = context.output_dir / "workflow_summary.json"
        md_path = context.output_dir / "workflow_summary.md"
        write_json(json_path, payload)
        write_text(md_path, _render_markdown(payload))
        artifacts = {
            "workflow_summary.json": artifact_from_path(
                name="workflow_summary.json",
                path=json_path,
                output_dir=context.output_dir,
                artifact_type="summary",
                producer_step=self.name,
                description="Machine-readable workflow summary.",
                required=True,
            ),
            "workflow_summary.md": artifact_from_path(
                name="workflow_summary.md",
                path=md_path,
                output_dir=context.output_dir,
                artifact_type="summary",
                producer_step=self.name,
                description="Human-readable workflow summary.",
                required=True,
            ),
        }
        return AgentResult(
            status="warning" if context.warnings else "success",
            payload=payload,
            artifacts=artifacts,
            warnings=[],
            limitations=payload["limitations"],
        )


def _render_markdown(payload: dict) -> str:
    lines = [
        "# Workflow Summary",
        "",
        f"- Run ID: `{payload['run_id']}`",
        f"- Parser: `{payload['parser']}`",
        f"- LLM provider: `{payload['llm_provider']}`",
        f"- Selected tool: `{payload['selected_tool']}`",
        "",
        "## Input",
        payload["input_text"],
        "",
        "## Validation",
        f"- Errors: {len((payload.get('validation') or {}).get('errors', []))}",
        f"- Warnings: {len((payload.get('validation') or {}).get('warnings', []))}",
        "",
        "## Generated Files",
        *_bullet_lines(payload.get("generated_files", {}).values()),
        "",
        "## Warnings",
        *_bullet_lines(payload.get("warnings", [])),
        "",
        "## Limitations",
        *_bullet_lines(payload.get("limitations", [])),
        "",
        "## Recommended Next Action",
        payload["next_recommended_action"],
        "",
        "> This workflow report is an orchestration artifact, not production-grade physical validation.",
    ]
    return "\n".join(lines)


def _bullet_lines(items) -> list[str]:
    values = [str(item) for item in items]
    if not values:
        return ["- none"]
    return [f"- {item}" for item in values]
