"""CLI tests for v0.9 workflow commands."""

import json

from typer.testing import CliRunner

from optical_spec_agent.cli.main import app


runner = CliRunner()


def test_workflow_plan_human_and_json(tmp_path):
    text = "用 MPB 计算二维光子晶体 band diagram。"
    human = runner.invoke(app, ["workflow-plan", text, "--tool", "mpb"])
    assert human.exit_code == 0
    assert "Workflow plan" in human.output

    result = runner.invoke(app, ["workflow-plan", text, "--tool", "mpb", "--json"])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data["selected_tool"] == "mpb"


def test_workflow_run_json_and_artifacts(tmp_path):
    result = runner.invoke(
        app,
        [
            "workflow-run",
            "用 MPB 计算二维光子晶体 band diagram。",
            "--parser",
            "hybrid",
            "--llm-provider",
            "mock",
            "--tool",
            "mpb",
            "--output-dir",
            str(tmp_path),
            "--no-execute",
            "--json",
        ],
    )
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data["selected_tool"] == "mpb"
    assert (tmp_path / "workflow_run.json").exists()
    assert (tmp_path / "artifacts/generated_input.py").exists()


def test_workflow_replay_and_report(tmp_path):
    run_dir = tmp_path / "run"
    result = runner.invoke(
        app,
        [
            "workflow-run",
            "用 MPB 计算二维光子晶体 band diagram。",
            "--parser",
            "hybrid",
            "--llm-provider",
            "mock",
            "--tool",
            "mpb",
            "--output-dir",
            str(run_dir),
            "--no-execute",
        ],
    )
    assert result.exit_code == 0

    replay_dir = tmp_path / "replay"
    replay = runner.invoke(
        app,
        ["workflow-replay", str(run_dir / "workflow_run.json"), "--output-dir", str(replay_dir)],
    )
    assert replay.exit_code == 0
    assert (replay_dir / "replay/replay_report.json").exists()

    report_path = run_dir / "report.md"
    report = runner.invoke(
        app,
        ["workflow-report", str(run_dir / "workflow_run.json"), "--output", str(report_path)],
    )
    assert report.exit_code == 0
    assert report_path.exists()
    assert "production-grade physical validation" in report_path.read_text(encoding="utf-8")


def test_workflow_run_unsupported_provider_fails_cleanly(tmp_path):
    result = runner.invoke(
        app,
        [
            "workflow-run",
            "用 MPB 计算 band diagram。",
            "--parser",
            "hybrid",
            "--llm-provider",
            "unsupported",
            "--tool",
            "mpb",
            "--output-dir",
            str(tmp_path),
            "--strict",
            "--json",
        ],
    )
    assert result.exit_code != 0
    data = json.loads(result.output)
    assert data["status"] == "error"
