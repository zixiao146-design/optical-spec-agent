"""Base classes and shared context for workflow agents."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from optical_spec_agent.adapters.base import BaseAdapter
from optical_spec_agent.models.spec import OpticalSpec
from optical_spec_agent.workflows.models import AgentResult, WorkflowArtifact, WorkflowRunnerConfig


@dataclass(slots=True)
class WorkflowContext:
    """Mutable in-memory context passed through synchronous workflow agents."""

    input_text: str
    output_dir: Path
    config: WorkflowRunnerConfig
    run_id: str
    dirs: dict[str, Path]
    current_spec: OpticalSpec | None = None
    validation_result: dict[str, Any] | None = None
    selected_adapter: BaseAdapter | None = None
    selected_tool: str = "auto"
    generated_files: dict[str, str] = field(default_factory=dict)
    diagnostics: dict[str, Any] | None = None
    parser_report: dict[str, Any] | None = None
    workflow_artifacts: dict[str, WorkflowArtifact] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    assumptions: list[str] = field(default_factory=list)
    limitations: list[str] = field(default_factory=list)


class WorkflowAgent:
    """Base synchronous workflow agent."""

    name = "workflow_agent"

    def run(self, context: WorkflowContext) -> AgentResult:
        """Run this agent."""
        raise NotImplementedError
