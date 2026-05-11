"""Workflow human-review checklist agent."""

from __future__ import annotations

from optical_spec_agent.workflows.agents.base import WorkflowAgent, WorkflowContext
from optical_spec_agent.workflows.artifacts import artifact_from_path, write_text
from optical_spec_agent.workflows.models import AgentResult


class HumanReviewAgent(WorkflowAgent):
    """Generate a non-interactive human review checklist."""

    name = "human_review"

    def run(self, context: WorkflowContext) -> AgentResult:
        spec = context.current_spec
        missing = spec.missing_fields if spec else []
        inferred = list(spec.inferred_fields.keys()) if spec else []
        confirmed = list(spec.confirmed_fields.keys()) if spec else []
        content = "\n".join(
            [
                "# Human Review Checklist",
                "",
                "This checklist is required because workflow orchestration does not prove physical correctness.",
                "",
                "## Input Task",
                context.input_text,
                "",
                "## Confirmed Fields",
                *_bullet_lines(confirmed),
                "",
                "## Inferred Fields",
                *_bullet_lines(inferred),
                "",
                "## Missing Fields",
                *_bullet_lines(missing),
                "",
                "## Adapter Limitations",
                *_bullet_lines(context.limitations),
                "",
                "## Generated Files To Inspect",
                *_bullet_lines(context.generated_files.values()),
                "",
                "## Required Human Decisions",
                "- Confirm geometry dimensions.",
                "- Confirm material model.",
                "- Confirm boundary/source settings.",
                "- Confirm sweep range.",
                "- Confirm mesh/resolution.",
                "- Confirm whether solver execution should be run manually.",
                "- Confirm convergence study requirements.",
                "- Confirm output observables are sufficient.",
            ]
        )
        path = context.output_dir / "human_review_checklist.md"
        write_text(path, content)
        artifacts = {
            "human_review_checklist.md": artifact_from_path(
                name="human_review_checklist.md",
                path=path,
                output_dir=context.output_dir,
                artifact_type="review",
                producer_step=self.name,
                description="Human review checklist for inferred/missing fields and limitations.",
                required=True,
            )
        }
        warnings = ["Human review is required before using generated inputs for research."]
        return AgentResult(
            status="warning",
            payload={"missing_fields": missing, "inferred_fields": inferred},
            artifacts=artifacts,
            warnings=warnings,
            notes=["Generated checklist is non-interactive."],
        )


def _bullet_lines(items) -> list[str]:
    values = list(items)
    if not values:
        return ["- none"]
    return [f"- {item}" for item in values]
