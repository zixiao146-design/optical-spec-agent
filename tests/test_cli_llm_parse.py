"""CLI tests for v0.8 parser selection."""

import json

from typer.testing import CliRunner

from optical_spec_agent.cli.main import app


runner = CliRunner()


def test_parse_default_still_works():
    result = runner.invoke(app, ["parse", "用 Meep FDTD 仿真金纳米球散射。"])
    assert result.exit_code == 0
    assert "Optical Spec Agent" in result.output


def test_parse_rule_json_outputs_valid_json():
    result = runner.invoke(app, ["parse", "用 Meep FDTD 仿真金纳米球散射。", "--parser", "rule", "--json"])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data["simulation"]["software_tool"]["value"] == "meep"


def test_parse_llm_mock_json_outputs_valid_json():
    result = runner.invoke(
        app,
        ["parse", "Use MPB to compute a photonic crystal band diagram.", "--parser", "llm", "--llm-provider", "mock", "--json"],
    )
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data["simulation"]["software_tool"]["value"] == "mpb"


def test_parse_hybrid_parser_report_output(tmp_path):
    report_path = tmp_path / "parser_report.json"
    result = runner.invoke(
        app,
        [
            "parse",
            "Use Gmsh to mesh a waveguide.",
            "--parser",
            "hybrid",
            "--llm-provider",
            "mock",
            "--parser-report-output",
            str(report_path),
        ],
    )
    assert result.exit_code == 0
    report = json.loads(report_path.read_text(encoding="utf-8"))
    assert report["parser_mode"] == "hybrid"


def test_parse_unsupported_llm_provider_fails_cleanly():
    result = runner.invoke(
        app,
        ["parse", "Use MPB.", "--parser", "llm", "--llm-provider", "real-provider"],
    )
    assert result.exit_code != 0
    assert "Unsupported LLM provider" in result.output
