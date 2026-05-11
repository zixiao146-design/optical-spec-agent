"""CLI tests for post-hoc physical diagnostics."""

from __future__ import annotations

import json
import subprocess
import sys

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


def test_diagnose_json_mode_is_machine_readable(tmp_path):
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
            "--json",
        ],
    )

    assert result.exit_code == 0, result.output
    payload = json.loads(result.stdout)
    assert payload["status"] in {"success", "warning"}
    assert payload["spec_path"] == str(spec_path)
    assert payload["output_dir"] == str(output_dir)
    assert "mesh_report.csv" in payload["generated_outputs"]


def test_diagnose_spec_option_takes_precedence_over_positional_path(tmp_path):
    positional_spec = tmp_path / "positional.json"
    option_spec = tmp_path / "option.json"
    output_dir = tmp_path / "outputs"

    result = runner.invoke(
        app,
        [
            "diagnose",
            str(positional_spec),
            "--spec",
            str(option_spec),
            "--output-dir",
            str(output_dir),
            "--create-demo-spec-if-missing",
            "--json",
        ],
    )

    assert result.exit_code == 0, result.output
    payload = json.loads(result.stdout)
    assert positional_spec.exists() is False
    assert option_spec.exists() is True
    assert payload["spec_path"] == str(option_spec)
    assert any("--spec was provided" in warning for warning in payload["warnings"])


def test_diagnose_partial_run_artifacts_detect_nan_inf_timeout(tmp_path):
    spec_path = tmp_path / "my_spec.json"
    output_dir = tmp_path / "outputs"
    run_dir = tmp_path / "run"
    run_dir.mkdir()
    (run_dir / "stdout.txt").write_text(
        "This information line should not trigger Inf by itself.\nfield = NaN\n",
        encoding="utf-8",
    )
    (run_dir / "stderr.txt").write_text(
        "solver reported Inf token and timed out after 300 seconds\n",
        encoding="utf-8",
    )

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
        ],
    )

    assert result.exit_code == 0, result.output
    diagnostics = json.loads((output_dir / "execution_diagnostics.json").read_text(encoding="utf-8"))
    assert diagnostics["nan_detected"] is True
    assert diagnostics["inf_detected"] is True
    assert diagnostics["timeout_detected"] is True
    assert set(diagnostics["missing_artifacts"]) == {"execution_result.json", "run_manifest.json"}


def test_diagnose_does_not_treat_information_as_inf(tmp_path):
    spec_path = tmp_path / "my_spec.json"
    output_dir = tmp_path / "outputs"
    run_dir = tmp_path / "run"
    run_dir.mkdir()
    (run_dir / "stdout.txt").write_text("information only\n", encoding="utf-8")
    (run_dir / "stderr.txt").write_text("more information\n", encoding="utf-8")

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
        ],
    )

    assert result.exit_code == 0, result.output
    diagnostics = json.loads((output_dir / "execution_diagnostics.json").read_text(encoding="utf-8"))
    assert diagnostics["inf_detected"] is False


def test_diagnose_corrupted_execution_result_is_warning(tmp_path):
    spec_path = tmp_path / "my_spec.json"
    output_dir = tmp_path / "outputs"
    run_dir = tmp_path / "run"
    run_dir.mkdir()
    (run_dir / "execution_result.json").write_text("{not-json", encoding="utf-8")

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
        ],
    )

    assert result.exit_code == 0, result.output
    diagnostics = json.loads((output_dir / "execution_diagnostics.json").read_text(encoding="utf-8"))
    assert diagnostics["status"] == "warning"
    assert any("Could not parse execution_result.json" in warning for warning in diagnostics["warnings"])


def test_diagnose_nonzero_execution_result_is_warning(tmp_path):
    spec_path = tmp_path / "my_spec.json"
    output_dir = tmp_path / "outputs"
    run_dir = tmp_path / "run"
    run_dir.mkdir()
    (run_dir / "stdout.txt").write_text("", encoding="utf-8")
    (run_dir / "stderr.txt").write_text("", encoding="utf-8")
    (run_dir / "run_manifest.json").write_text("{}", encoding="utf-8")
    (run_dir / "execution_result.json").write_text(
        json.dumps({"success": False, "returncode": 1, "errors": ["failed"], "warnings": []}),
        encoding="utf-8",
    )

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
        ],
    )

    assert result.exit_code == 0, result.output
    diagnostics = json.loads((output_dir / "execution_diagnostics.json").read_text(encoding="utf-8"))
    assert diagnostics["status"] == "warning"
    assert any("nonzero returncode" in warning for warning in diagnostics["warnings"])
    assert any("success=false" in warning for warning in diagnostics["warnings"])


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
    assert len((output_dir / "mesh_report.csv").read_text(encoding="utf-8").splitlines()) > 1
    assert len((output_dir / "flux_report.csv").read_text(encoding="utf-8").splitlines()) > 1
    assert "check_name,value,threshold,unit,status,message" == mesh_header
    assert flux_header.startswith("monitor_name,surface,value,unit,status,message")


def test_diagnostics_script_wrapper_still_generates_artifacts(tmp_path):
    spec_path = tmp_path / "my_spec.json"
    output_dir = tmp_path / "outputs"
    result = subprocess.run(
        [
            sys.executable,
            "scripts/generate_physical_diagnostics.py",
            "--spec",
            str(spec_path),
            "--output-dir",
            str(output_dir),
            "--create-demo-spec-if-missing",
            "--json",
        ],
        capture_output=True,
        text=True,
        timeout=30,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    payload = json.loads(result.stdout)
    assert payload["status"] in {"success", "warning"}
    assert (output_dir / "mesh_report.csv").exists()
    assert (output_dir / "flux_report.csv").exists()
    assert (output_dir / "execution_diagnostics.json").exists()
    assert (output_dir / "diagnostic_preview.png").stat().st_size > 0
