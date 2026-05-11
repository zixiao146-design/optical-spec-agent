"""Workflow intake agent."""

from __future__ import annotations

from optical_spec_agent.workflows.agents.base import WorkflowAgent, WorkflowContext
from optical_spec_agent.workflows.artifacts import artifact_from_path, write_json, write_text
from optical_spec_agent.workflows.models import AgentResult


class IntakeAgent(WorkflowAgent):
    """Capture and sanity-check the input task."""

    name = "intake"

    def run(self, context: WorkflowContext) -> AgentResult:
        warnings: list[str] = []
        errors: list[str] = []
        text = context.input_text or ""
        if not text.strip():
            errors.append("Input text is empty.")
        if len(text) > context.config.max_input_chars:
            errors.append(
                f"Input text exceeds max_input_chars={context.config.max_input_chars}."
            )
        if any(ord(char) < 32 and char not in "\n\t\r" for char in text):
            warnings.append("Input contains control characters; review before execution.")

        input_path = context.output_dir / "input.txt"
        summary_path = context.dirs["artifacts"] / "intake_summary.json"
        write_text(input_path, text)
        payload = {
            "run_id": context.run_id,
            "input_chars": len(text),
            "parser": context.config.parser,
            "llm_provider": context.config.llm_provider,
            "preferred_tool": context.config.tool,
        }
        write_json(summary_path, payload)

        artifacts = {
            "input.txt": artifact_from_path(
                name="input.txt",
                path=input_path,
                output_dir=context.output_dir,
                artifact_type="input",
                producer_step=self.name,
                description="Original natural-language workflow input.",
                required=True,
            ),
            "intake_summary.json": artifact_from_path(
                name="intake_summary.json",
                path=summary_path,
                output_dir=context.output_dir,
                artifact_type="summary",
                producer_step=self.name,
                description="Input sanity-check summary.",
            ),
        }
        return AgentResult(
            status="error" if errors else "warning" if warnings else "success",
            payload=payload,
            artifacts=artifacts,
            warnings=warnings,
            errors=errors,
        )
