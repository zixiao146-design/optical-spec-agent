"""Workflow report rendering tests."""

from optical_spec_agent.workflows import (
    WorkflowRunner,
    WorkflowRunnerConfig,
    load_workflow_run,
    render_workflow_report,
    write_workflow_report,
)


def test_workflow_report_includes_limitations(tmp_path):
    WorkflowRunner(
        WorkflowRunnerConfig(
            parser="hybrid",
            llm_provider="mock",
            tool="mpb",
            output_dir=tmp_path,
        )
    ).run("用 MPB 计算二维光子晶体 band diagram。")
    workflow = load_workflow_run(tmp_path / "workflow_run.json")
    markdown = render_workflow_report(workflow)
    assert "Limitations" in markdown
    assert "not production-grade physical validation" in markdown


def test_write_workflow_report_json(tmp_path):
    WorkflowRunner(
        WorkflowRunnerConfig(
            parser="hybrid",
            llm_provider="mock",
            tool="mpb",
            output_dir=tmp_path,
        )
    ).run("用 MPB 计算二维光子晶体 band diagram。")
    output = tmp_path / "report.json"
    write_workflow_report(tmp_path / "workflow_run.json", output=output, fmt="json")
    assert output.exists()
    assert "selected_tool" in output.read_text(encoding="utf-8")
