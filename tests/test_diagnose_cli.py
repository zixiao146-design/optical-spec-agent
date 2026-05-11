"""CLI tests for post-hoc physical diagnostics."""

from __future__ import annotations

import json

from typer.testing import CliRunner

from optical_spec_agent.cli.main import app


runner = CliRunner()


def test_diagnose_creates_demo_spec_and_artifacts(tmp_path):
    spec_path = tmp_path / "outputs" / "my_spec.json"
    output_dir = tmp_path / "outputs"

    result = runner.invoke(
        app,
        [
            "diagnose",
            str(spec_path),
            "--output-dir",
            str(output_dir),
            "--create-demo-spec-if-missing",
        ],
    )

    assert result.exit_code == 0, result.output
    assert spec_path.exists()
    assert (output_dir / "mesh_report.csv").exists()
    assert (output_dir / "flux_report.csv").exists()
    assert (output_dir / "execution_diagnostics.json").exists()
    assert (output_dir / "diagnostic_preview.png").read_bytes().startswith(b"\x89PNG")


def test_diagnose_missing_spec_without_demo_flag_fails(tmp_path):
    spec_path = tmp_path / "missing.json"
    output_dir = tmp_path / "outputs"

    result = runner.invoke(
        app,
        ["diagnose", "--spec", str(spec_path), "--output-dir", str(output_dir)],
    )

    assert result.exit_code != 0
    assert "Spec file not found" in result.output


def test_diagnose_missing_run_artifacts_are_reported(tmp_path):
    spec_path = tmp_path / "my_spec.json"
    output_dir = tmp_path / "outputs"
    run_dir = tmp_path / "run"
    run_dir.mkdir()

    result = runner.invoke(
        app,
        [
            "diagnose",
            str(spec_path),
            "--output-dir",
            str(output_dir),
            "--run-dir",
            str(run_dir),
            "--create-demo-spec-if-missing",
            "--json",
        ],
    )

    assert result.exit_code == 0, result.output
    diagnostics = json.loads((output_dir / "execution_diagnostics.json").read_text(encoding="utf-8"))
    assert diagnostics["status"] == "warning"
    assert diagnostics["run_dir"] == str(run_dir)
    assert set(diagnostics["missing_artifacts"]) == {
        "stdout.txt",
        "stderr.txt",
        "execution_result.json",
        "run_manifest.json",
    }
    assert diagnostics["nan_detected"] is False
    assert diagnostics["inf_detected"] is False
    assert diagnostics["timeout_detected"] is False


def test_diagnose_report_schema_contains_required_fields(tmp_path):
    spec_path = tmp_path / "my_spec.json"
    output_dir = tmp_path / "outputs"

    result = runner.invoke(
        app,
        [
            "diagnose",
            "--spec",
            str(spec_path),
            "--output-dir",
            str(output_dir),
            "--create-demo-spec-if-missing",
        ],
    )

    assert result.exit_code == 0, result.output
    diagnostics = json.loads((output_dir / "execution_diagnostics.json").read_text(encoding="utf-8"))
    for key in [
        "schema_version",
        "spec_path",
        "output_dir",
        "run_dir",
        "generated_at",
        "status",
        "warnings",
        "errors",
        "missing_artifacts",
        "nan_detected",
        "inf_detected",
        "timeout_detected",
        "notes",
    ]:
        assert key in diagnostics

    mesh_header = (output_dir / "mesh_report.csv").read_text(encoding="utf-8").splitlines()[0]
    flux_header = (output_dir / "flux_report.csv").read_text(encoding="utf-8").splitlines()[0]
    assert "check_name,value,threshold,unit,status,message" == mesh_header
    assert flux_header.startswith("monitor_name,surface,value,unit,status,message")
