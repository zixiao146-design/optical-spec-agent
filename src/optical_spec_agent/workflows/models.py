"""Serializable workflow models for v0.9 local orchestration."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Literal
from uuid import uuid4

from pydantic import BaseModel, Field


WORKFLOW_SCHEMA_VERSION = "workflow.v0.9"
WORKFLOW_PLAN_SCHEMA_VERSION = "workflow_plan.v0.9"
WORKFLOW_REPLAY_SCHEMA_VERSION = "workflow_replay.v0.9"
WORKFLOW_EVALUATION_SCHEMA_VERSION = "workflow_evaluation.v0.9"

WorkflowStatus = Literal["success", "warning", "error", "skipped"]


def utc_now_iso() -> str:
    """Return a stable ISO timestamp for workflow artifacts."""
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def make_workflow_run_id(prefix: str = "workflow") -> str:
    """Generate a human-readable run ID."""
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    return f"{prefix}-{stamp}-{uuid4().hex[:8]}"


class WorkflowArtifact(BaseModel):
    """One file emitted or expected during a workflow run."""

    name: str
    path: str
    artifact_type: str
    producer_step: str
    description: str = ""
    required: bool = False
    exists: bool = False
    size_bytes: int | None = None

    @classmethod
    def from_path(
        cls,
        *,
        name: str,
        path: Path,
        output_dir: Path,
        artifact_type: str,
        producer_step: str,
        description: str = "",
        required: bool = False,
    ) -> "WorkflowArtifact":
        """Build an artifact record from a path, stored relative to output_dir when possible."""
        exists = path.exists()
        try:
            rel_path = path.relative_to(output_dir)
        except ValueError:
            rel_path = path
        return cls(
            name=name,
            path=str(rel_path),
            artifact_type=artifact_type,
            producer_step=producer_step,
            description=description,
            required=required,
            exists=exists,
            size_bytes=path.stat().st_size if exists and path.is_file() else None,
        )


class WorkflowStepResult(BaseModel):
    """Auditable result for one workflow agent step."""

    step_id: str
    agent_name: str
    status: WorkflowStatus
    started_at: str
    finished_at: str
    duration_ms: float
    inputs_summary: dict[str, Any] = Field(default_factory=dict)
    outputs_summary: dict[str, Any] = Field(default_factory=dict)
    artifacts: dict[str, WorkflowArtifact] = Field(default_factory=dict)
    warnings: list[str] = Field(default_factory=list)
    errors: list[str] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)


class AgentResult(BaseModel):
    """Internal result returned by a workflow agent."""

    status: WorkflowStatus = "success"
    payload: dict[str, Any] = Field(default_factory=dict)
    artifacts: dict[str, WorkflowArtifact] = Field(default_factory=dict)
    warnings: list[str] = Field(default_factory=list)
    errors: list[str] = Field(default_factory=list)
    assumptions: list[str] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)


class WorkflowPlan(BaseModel):
    """Dry-run plan for a workflow without running adapters or solvers."""

    schema_version: str = WORKFLOW_PLAN_SCHEMA_VERSION
    input_text: str
    planned_steps: list[str]
    parser_mode: str = "rule"
    selected_tool: str = "auto"
    execute_policy: str = "no_execute"
    expected_artifacts: list[str] = Field(default_factory=list)
    risk_flags: list[str] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)


class WorkflowRun(BaseModel):
    """Top-level workflow run record. This is the v0.9 source of truth."""

    schema_version: str = WORKFLOW_SCHEMA_VERSION
    run_id: str
    created_at: str
    input_text: str
    parser_mode: str = "rule"
    llm_provider: str = "mock"
    selected_tool: str = "auto"
    output_dir: str
    status: Literal["success", "warning", "error"] = "success"
    steps: list[WorkflowStepResult] = Field(default_factory=list)
    artifacts: dict[str, WorkflowArtifact] = Field(default_factory=dict)
    warnings: list[str] = Field(default_factory=list)
    errors: list[str] = Field(default_factory=list)
    assumptions: list[str] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)


class WorkflowRunnerConfig(BaseModel):
    """Configuration for synchronous local workflow execution."""

    parser: str = "rule"
    llm_provider: str = "mock"
    tool: str = "auto"
    output_dir: Path
    allow_execute: bool = False
    strict: bool = False
    strict_execution: bool = False
    continue_on_warning: bool = True
    run_diagnostics: bool = True
    run_eval: bool = False
    create_demo_spec_if_missing: bool = False
    max_input_chars: int = 20_000
    workflow_schema_version: str = WORKFLOW_SCHEMA_VERSION

    model_config = {"arbitrary_types_allowed": True}


class ReplayReport(BaseModel):
    """Result of replaying an existing workflow run."""

    schema_version: str = WORKFLOW_REPLAY_SCHEMA_VERSION
    original_run_id: str
    replay_run_id: str
    deterministic_match: bool
    compared_fields: list[str] = Field(default_factory=list)
    differences: list[dict[str, Any]] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    errors: list[str] = Field(default_factory=list)
    replay_workflow_run: str | None = None
