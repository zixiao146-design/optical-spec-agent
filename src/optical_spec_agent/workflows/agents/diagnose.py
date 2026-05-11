"""Workflow diagnostics agent."""

from __future__ import annotations

from optical_spec_agent.analysis import generate_physical_diagnostics
from optical_spec_agent.workflows.agents.base import WorkflowAgent, WorkflowContext
from optical_spec_agent.workflows.artifacts import artifact_from_path, write_json
from optical_spec_agent.workflows.models import AgentResult


class DiagnosticsAgent(WorkflowAgent):
    """Run post-hoc diagnostics for Meep workflows or write not-applicable metadata."""

    name = "diagnostics"

    def run(self, context: WorkflowContext) -> AgentResult:
        if not context.config.run_diagnostics:
            return self._not_applicable(context, reason="Diagnostics disabled by workflow configuration.")
        if context.selected_tool != "meep":
            return self._not_applicable(
                context,
                reason=f"Post-hoc physical diagnostics currently target Meep artifacts, not {context.selected_tool}.",
            )

        spec_path = context.dirs["artifacts"] / "spec.json"
        if not spec_path.exists():
            return AgentResult(status="error", errors=["No spec.json available for diagnostics."])

        result = generate_physical_diagnostics(
            spec_path=spec_path,
            output_dir=context.dirs["artifacts"],
            artifact_dir=context.output_dir / "execution",
            initial_warnings=[
                "Workflow diagnostics are post-hoc sanity checks, not production validation."
            ],
        )
        context.diagnostics = result.to_dict()
        artifacts = {}
        for name, path in result.generated_outputs.items():
            artifacts[name] = artifact_from_path(
                name=name,
                path=context.dirs["artifacts"] / name,
                output_dir=context.output_dir,
                artifact_type="diagnostic",
                producer_step=self.name,
                description=f"Workflow diagnostic artifact: {name}",
            )
        return AgentResult(
            status=result.status,
            payload=result.to_dict(),
            artifacts=artifacts,
            warnings=result.warnings,
            errors=result.errors,
            notes=result.notes,
        )

    def _not_applicable(self, context: WorkflowContext, *, reason: str) -> AgentResult:
        payload = {"applicable": False, "reason": reason}
        path = context.dirs["artifacts"] / "diagnostics_not_applicable.json"
        write_json(path, payload)
        artifacts = {
            "diagnostics_not_applicable.json": artifact_from_path(
                name="diagnostics_not_applicable.json",
                path=path,
                output_dir=context.output_dir,
                artifact_type="diagnostic",
                producer_step=self.name,
                description="Reason diagnostics were not run.",
            )
        }
        return AgentResult(status="skipped", payload=payload, artifacts=artifacts, notes=[reason])
