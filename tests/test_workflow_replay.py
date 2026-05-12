"""Workflow replay tests."""

import json

from optical_spec_agent.workflows import WorkflowRunner, WorkflowRunnerConfig, replay_workflow


def test_workflow_replay_generates_report(tmp_path):
    run_dir = tmp_path / "original"
    workflow = WorkflowRunner(
        WorkflowRunnerConfig(
            parser="hybrid",
            llm_provider="mock",
            tool="mpb",
            output_dir=run_dir,
        )
    ).run("用 MPB 计算二维光子晶体 band diagram。")

    report = replay_workflow(run_dir / "workflow_run.json", output_dir=tmp_path / "replay")
    assert report.original_run_id == workflow.run_id
    assert report.replay_run_id != workflow.run_id
    replay_report_path = tmp_path / "replay/replay/replay_report.json"
    replay_run_path = tmp_path / "replay/workflow_run.json"
    assert replay_report_path.exists()
    assert replay_run_path.exists()
    assert "selected_tool" in report.compared_fields
    assert report.deterministic_match is True
    assert report.differences == []
    assert report.replay_workflow_run == str(replay_run_path)

    replay_data = json.loads(replay_run_path.read_text(encoding="utf-8"))
    assert replay_data["selected_tool"] == "mpb"
    assert replay_data["parser_mode"] == "hybrid"
    assert replay_data["llm_provider"] == "mock"
    assert replay_data["status"] in {"success", "warning"}
    assert replay_data["artifacts"]["execution_skip.json"]["exists"] is True
    assert replay_data["artifacts"]["diagnostics_not_applicable.json"]["exists"] is True
    assert replay_data["artifacts"]["generated_input"]["artifact_type"] == "solver_input"

    report_data = json.loads(replay_report_path.read_text(encoding="utf-8"))
    assert report_data["schema_version"] == "workflow_replay.v0.9"
    assert report_data["deterministic_match"] is True
