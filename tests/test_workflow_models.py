"""Tests for v0.9 workflow data models."""

from pathlib import Path

from optical_spec_agent.workflows.models import (
    WorkflowArtifact,
    WorkflowRun,
    WorkflowStepResult,
    utc_now_iso,
)


def test_workflow_models_json_serializable(tmp_path):
    artifact_path = tmp_path / "artifact.txt"
    artifact_path.write_text("hello", encoding="utf-8")
    artifact = WorkflowArtifact.from_path(
        name="artifact.txt",
        path=artifact_path,
        output_dir=tmp_path,
        artifact_type="test",
        producer_step="unit",
        required=True,
    )
    step = WorkflowStepResult(
        step_id="01_unit",
        agent_name="unit",
        status="success",
        started_at=utc_now_iso(),
        finished_at=utc_now_iso(),
        duration_ms=1.0,
        artifacts={"artifact.txt": artifact},
    )
    run = WorkflowRun(
        run_id="workflow-test",
        created_at=utc_now_iso(),
        input_text="test",
        output_dir=str(tmp_path),
        steps=[step],
        artifacts={"artifact.txt": artifact},
    )
    payload = run.model_dump(mode="json")
    assert payload["artifacts"]["artifact.txt"]["exists"] is True
    assert payload["artifacts"]["artifact.txt"]["size_bytes"] > 0


def test_workflow_artifact_missing_file(tmp_path):
    artifact = WorkflowArtifact.from_path(
        name="missing.txt",
        path=Path(tmp_path / "missing.txt"),
        output_dir=tmp_path,
        artifact_type="test",
        producer_step="unit",
    )
    assert artifact.exists is False
    assert artifact.size_bytes is None
