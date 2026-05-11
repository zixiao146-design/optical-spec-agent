"""Workflow replay tests."""

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
    assert (tmp_path / "replay/replay/replay_report.json").exists()
    assert "selected_tool" in report.compared_fields
