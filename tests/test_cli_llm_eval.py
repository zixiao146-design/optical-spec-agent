"""CLI tests for llm-eval."""

import json

from typer.testing import CliRunner

from optical_spec_agent.cli.main import app


runner = CliRunner()


def _write_cases(path):
    path.write_text(
        json.dumps(
            [
                {
                    "id": "tmp-1",
                    "text": "Use MPB to compute a photonic crystal band diagram.",
                    "expected": {"simulation.software_tool": "mpb"},
                },
                {
                    "id": "tmp-2",
                    "text": "帮我仿真一下这个结构。",
                    "expected": {"task.task_type": "simulation"},
                },
            ],
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )


def test_llm_eval_writes_report(tmp_path):
    cases = tmp_path / "cases.json"
    report = tmp_path / "report.json"
    _write_cases(cases)
    result = runner.invoke(
        app,
        ["llm-eval", str(cases), "--parser", "hybrid", "--llm-provider", "mock", "--report", str(report)],
    )
    assert result.exit_code == 0
    data = json.loads(report.read_text(encoding="utf-8"))
    assert data["schema_version"] == "llm_eval_report.v0.8"
    assert data["total_cases"] == 2


def test_llm_eval_json_output(tmp_path):
    cases = tmp_path / "cases.json"
    _write_cases(cases)
    result = runner.invoke(
        app,
        ["llm-eval", str(cases), "--parser", "hybrid", "--llm-provider", "mock", "--json"],
    )
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data["passed_cases"] == 2
