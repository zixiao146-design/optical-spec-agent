"""Workflow adapter-selection agent."""

from __future__ import annotations

from optical_spec_agent.adapters.registry import dispatch_adapter
from optical_spec_agent.workflows.agents.base import WorkflowAgent, WorkflowContext
from optical_spec_agent.workflows.artifacts import artifact_from_path, write_json
from optical_spec_agent.workflows.models import AgentResult


class AdapterSelectionAgent(WorkflowAgent):
    """Select a solver-input adapter and record readiness metadata."""

    name = "adapter_selection"

    def run(self, context: WorkflowContext) -> AgentResult:
        if context.current_spec is None:
            return AgentResult(status="error", errors=["No spec available for adapter selection."])

        try:
            adapter = dispatch_adapter(context.current_spec, preferred_tool=context.config.tool)
        except Exception as exc:  # noqa: BLE001 - non-strict workflows should still produce review artifacts.
            report = {
                "selected_tool": None,
                "metadata": {},
                "readiness": {
                    "adapter_ready": False,
                    "errors": [str(exc)],
                    "warnings": [],
                    "missing_required": ["adapter_selection"],
                    "defaults_applied": [],
                },
                "limitations": ["No adapter was selected; generation will be skipped."],
            }
            report_path = context.dirs["artifacts"] / "adapter_selection.json"
            write_json(report_path, report)
            artifacts = {
                "adapter_selection.json": artifact_from_path(
                    name="adapter_selection.json",
                    path=report_path,
                    output_dir=context.output_dir,
                    artifact_type="adapter_selection",
                    producer_step=self.name,
                    description="Adapter selection failure report.",
                    required=True,
                )
            }
            status = "error" if context.config.strict else "warning"
            return AgentResult(
                status=status,
                payload=report,
                artifacts=artifacts,
                warnings=[] if context.config.strict else [str(exc)],
                errors=[str(exc)] if context.config.strict else [],
                limitations=report["limitations"],
            )

        context.selected_adapter = adapter
        context.selected_tool = adapter.tool_name
        readiness = adapter.validate_ready(context.current_spec)
        metadata = adapter.metadata().model_dump(mode="json")
        report = {
            "selected_tool": adapter.tool_name,
            "metadata": metadata,
            "readiness": readiness.model_dump(mode="json")
            if hasattr(readiness, "model_dump")
            else dict(readiness),
            "limitations": metadata.get("limitations", []),
        }
        context.limitations.extend(metadata.get("limitations", []))
        report_path = context.dirs["artifacts"] / "adapter_selection.json"
        write_json(report_path, report)
        artifacts = {
            "adapter_selection.json": artifact_from_path(
                name="adapter_selection.json",
                path=report_path,
                output_dir=context.output_dir,
                artifact_type="adapter_selection",
                producer_step=self.name,
                description="Selected adapter and readiness report.",
                required=True,
            )
        }
        errors = list(report["readiness"].get("errors", []))
        missing = list(report["readiness"].get("missing_required", []))
        warnings = [
            *list(report["readiness"].get("warnings", [])),
            *[f"Missing adapter-required field: {item}" for item in missing],
        ]
        status = (
            "error"
            if errors and context.config.strict
            else "warning"
            if errors or warnings
            else "success"
        )
        return AgentResult(
            status=status,
            payload=report,
            artifacts=artifacts,
            warnings=warnings,
            errors=errors if context.config.strict else [],
            limitations=metadata.get("limitations", []),
        )
