"""Tests for the optional Meep execution harness."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import pytest

from optical_spec_agent.adapters.meep import MeepAdapter
from optical_spec_agent.execution import (
    ExecutionResult,
    check_meep_available,
    collect_meep_outputs,
    find_meep_python,
    run_meep_script,
)
from optical_spec_agent.models.base import (
    BoundaryConditionSetting,
    ParticleInfo,
    SourceSetting,
    SubstrateOrFilmInfo,
    confirmed,
)
from optical_spec_agent.models.spec import OpticalSpec


def _make_valid_spec() -> OpticalSpec:
    spec = OpticalSpec()
    spec.task.task_type = confirmed("simulation")
    spec.task.research_goal = confirmed("simulate gap plasmon")
    spec.physics.physical_system = confirmed("nanoparticle_on_film")
    spec.physics.structure_type = confirmed("sphere_on_film")
    spec.simulation.solver_method = confirmed("fdtd")
    spec.simulation.software_tool = confirmed("meep")
    spec.simulation.excitation_source = confirmed("plane_wave")
    spec.simulation.source_setting = confirmed(
        SourceSetting(source_type="plane_wave", wavelength_range="400-900 nm")
    )
    spec.simulation.boundary_condition = confirmed(
        BoundaryConditionSetting(x_min="PML", x_max="PML", y_min="PML", y_max="PML", z_min="PML", z_max="PML")
    )
    spec.simulation.monitor_setting = confirmed({"monitor_type": "frequency_domain"})
    spec.geometry_material.particle_info = confirmed(
        ParticleInfo(particle_type="sphere", material="Au", dimensions={"直径": "80 nm"})
    )
    spec.geometry_material.substrate_or_film_info = confirmed(
        SubstrateOrFilmInfo(has_film=True, film_material="Au", film_thickness="100 nm")
    )
    spec.geometry_material.gap_medium = confirmed("SiO2")
    spec.output.output_observables = confirmed(["scattering_spectrum"])
    return spec


def test_check_meep_available_returns_structured_result():
    result = check_meep_available()
    assert isinstance(result, ExecutionResult)
    assert result.schema_version == "execution_result.v0.1"
    assert result.run_id.startswith("meep-check-")
    assert result.created_at.endswith("Z")
    assert isinstance(result.success, bool)
    assert isinstance(result.available, bool)
    assert isinstance(result.command, list)
    assert isinstance(result.errors, list)
    assert isinstance(result.warnings, list)
    if result.available:
        assert result.success is True
    else:
        assert any("Meep is not available" in error for error in result.errors)


def test_run_meep_script_missing_file_returns_error(tmp_path):
    result = run_meep_script(tmp_path / "missing.py", workdir=tmp_path / "run")
    assert result.success is False
    assert any("File not found" in error for error in result.errors)


def test_run_meep_script_missing_file_writes_artifacts(tmp_path):
    run_dir = tmp_path / "run"
    result = run_meep_script(tmp_path / "missing.py", workdir=run_dir)

    assert result.success is False
    assert (run_dir / "execution_result.json").exists()
    assert (run_dir / "run_manifest.json").exists()
    saved = json.loads((run_dir / "execution_result.json").read_text(encoding="utf-8"))
    assert saved["success"] is False
    assert saved["run_id"] == result.run_id


def test_run_meep_script_when_meep_unavailable_returns_unavailable(tmp_path, monkeypatch):
    script_path = tmp_path / "noop.py"
    script_path.write_text("print('hello')\n", encoding="utf-8")
    monkeypatch.setattr(
        "optical_spec_agent.execution.meep_runner.find_meep_python",
        lambda: None,
    )

    result = run_meep_script(script_path, workdir=tmp_path / "run")

    assert result.success is False
    assert result.available is False
    assert any("Meep is not available" in error for error in result.errors)


def test_run_meep_script_meep_unavailable_writes_artifacts(tmp_path, monkeypatch):
    script_path = tmp_path / "noop.py"
    script_path.write_text("print('hello')\n", encoding="utf-8")
    run_dir = tmp_path / "run"
    monkeypatch.setattr(
        "optical_spec_agent.execution.meep_runner.find_meep_python",
        lambda: None,
    )

    result = run_meep_script(script_path, workdir=run_dir)

    assert result.success is False
    assert result.available is False
    assert (run_dir / "execution_result.json").exists()
    assert (run_dir / "run_manifest.json").exists()


def test_run_meep_script_unsupported_expected_mode_returns_error(tmp_path):
    script_path = tmp_path / "noop.py"
    script_path.write_text("print('hello')\n", encoding="utf-8")

    result = run_meep_script(script_path, workdir=tmp_path / "run", expected_mode="paper")

    assert result.success is False
    assert any("Unsupported expected_mode" in error for error in result.errors)


def test_collect_meep_outputs_reads_known_files(tmp_path):
    (tmp_path / "scattering_spectrum.csv").write_text(
        "wavelength_nm,particle_induced_flux_relative\n500,1.0\n",
        encoding="utf-8",
    )
    (tmp_path / "scattering_spectrum.png").write_bytes(b"fake-png")
    expected_json = {
        "mode": "research_preview",
        "resonance_wavelength_nm": None,
        "fwhm_nm": None,
    }
    (tmp_path / "postprocess_results.json").write_text(
        json.dumps(expected_json),
        encoding="utf-8",
    )

    outputs, postprocess_results = collect_meep_outputs(tmp_path)

    assert set(outputs) == {
        "scattering_spectrum.csv",
        "scattering_spectrum.png",
        "postprocess_results.json",
    }
    assert postprocess_results == expected_json


def test_research_preview_missing_required_outputs_fails(tmp_path, monkeypatch):
    script_path = tmp_path / "noop.py"
    script_path.write_text("print('done')\n", encoding="utf-8")
    monkeypatch.setattr(
        "optical_spec_agent.execution.meep_runner.find_meep_python",
        lambda: [sys.executable],
    )

    result = run_meep_script(
        script_path,
        workdir=tmp_path / "run",
        expected_mode="research_preview",
    )

    assert result.success is False
    assert result.expected_mode == "research_preview"
    assert result.required_outputs == [
        "scattering_spectrum.csv",
        "postprocess_results.json",
    ]
    assert "scattering_spectrum.csv" in result.missing_outputs
    assert "postprocess_results.json" in result.missing_outputs


def test_research_preview_required_outputs_pass(tmp_path, monkeypatch):
    postprocess = {
        "mode": "research_preview",
        "resonance_wavelength_nm": 640.5,
        "fwhm_nm": 72.0,
        "gap_thickness_nm": 5.0,
        "wavelength_min_nm": 400.0,
        "wavelength_max_nm": 900.0,
        "defaults_applied": ["resolution=50"],
        "limitations": ["heuristic peak extraction"],
    }
    script_path = tmp_path / "write_outputs.py"
    script_path.write_text(
        "\n".join(
            [
                "from pathlib import Path",
                "Path('scattering_spectrum.csv').write_text('wavelength_nm,particle_induced_flux_relative\\n500,1.0\\n')",
                f"Path('postprocess_results.json').write_text({json.dumps(json.dumps(postprocess))})",
                "print('done')",
            ]
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(
        "optical_spec_agent.execution.meep_runner.find_meep_python",
        lambda: [sys.executable],
    )

    result = run_meep_script(
        script_path,
        workdir=tmp_path / "run",
        expected_mode="research-preview",
    )

    assert result.success is True
    assert result.expected_mode == "research_preview"
    assert result.missing_outputs == []
    assert result.postprocess_results == postprocess
    assert result.typed_postprocess_results is not None
    assert result.typed_postprocess_results["resonance_wavelength_nm"] == 640.5
    assert result.typed_postprocess_results["fwhm_nm"] == 72.0
    assert result.typed_postprocess_results["defaults_applied"] == ["resolution=50"]


def test_research_preview_invalid_postprocess_json_fails(tmp_path, monkeypatch):
    script_path = tmp_path / "bad_json.py"
    script_path.write_text(
        "\n".join(
            [
                "from pathlib import Path",
                "Path('scattering_spectrum.csv').write_text('wavelength_nm,particle_induced_flux_relative\\n500,1.0\\n')",
                "Path('postprocess_results.json').write_text('{not valid json')",
            ]
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(
        "optical_spec_agent.execution.meep_runner.find_meep_python",
        lambda: [sys.executable],
    )

    result = run_meep_script(
        script_path,
        workdir=tmp_path / "run",
        expected_mode="research_preview",
    )

    assert result.success is False
    assert any("Could not parse" in error for error in result.errors)


def test_research_preview_postprocess_json_must_be_object(tmp_path, monkeypatch):
    script_path = tmp_path / "json_array.py"
    script_path.write_text(
        "\n".join(
            [
                "from pathlib import Path",
                "Path('scattering_spectrum.csv').write_text('wavelength_nm,particle_induced_flux_relative\\n500,1.0\\n')",
                "Path('postprocess_results.json').write_text('[]')",
            ]
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(
        "optical_spec_agent.execution.meep_runner.find_meep_python",
        lambda: [sys.executable],
    )

    result = run_meep_script(
        script_path,
        workdir=tmp_path / "run",
        expected_mode="research_preview",
    )

    assert result.success is False
    assert any("JSON object" in error for error in result.errors)


def test_run_meep_script_writes_artifact_files(tmp_path, monkeypatch):
    script_path = tmp_path / "artifacts.py"
    script_path.write_text(
        "import sys\nprint('stdout marker')\nsys.stderr.write('stderr marker\\n')\n",
        encoding="utf-8",
    )
    run_dir = tmp_path / "run"
    monkeypatch.setattr(
        "optical_spec_agent.execution.meep_runner.find_meep_python",
        lambda: [sys.executable],
    )

    result = run_meep_script(script_path, workdir=run_dir, expected_mode="preview")

    assert result.success is True
    assert result.schema_version == "execution_result.v0.1"
    assert re.match(r"^meep-\d{8}-\d{6}-[0-9a-f]{8}$", result.run_id)
    assert result.created_at.endswith("Z")
    assert result.script_path == str(script_path.resolve())
    assert (run_dir / "stdout.txt").read_text(encoding="utf-8").strip() == "stdout marker"
    assert (run_dir / "stderr.txt").read_text(encoding="utf-8").strip() == "stderr marker"
    saved = json.loads((run_dir / "execution_result.json").read_text(encoding="utf-8"))
    assert saved["success"] is True
    assert saved["schema_version"] == "execution_result.v0.1"
    assert saved["run_id"] == result.run_id
    assert saved["created_at"] == result.created_at
    assert saved["script_path"] == str(script_path.resolve())
    assert saved["expected_mode"] == "preview"
    manifest = json.loads((run_dir / "run_manifest.json").read_text(encoding="utf-8"))
    assert manifest["schema_version"] == "execution_result.v0.1"
    assert manifest["run_id"] == result.run_id
    assert manifest["script_path"] == str(script_path.resolve())
    assert manifest["workdir"] == str(run_dir)
    assert manifest["success"] is True
    assert manifest["outputs"] == {}


def test_run_meep_script_accepts_explicit_run_id(tmp_path, monkeypatch):
    script_path = tmp_path / "explicit_run_id.py"
    script_path.write_text("print('ok')\n", encoding="utf-8")
    monkeypatch.setattr(
        "optical_spec_agent.execution.meep_runner.find_meep_python",
        lambda: [sys.executable],
    )

    result = run_meep_script(
        script_path,
        workdir=tmp_path / "run",
        expected_mode="preview",
        run_id="manual-run-001",
    )

    assert result.success is True
    assert result.run_id == "manual-run-001"


def test_save_artifacts_false_skips_artifact_files(tmp_path, monkeypatch):
    script_path = tmp_path / "no_artifacts.py"
    script_path.write_text("print('ok')\n", encoding="utf-8")
    run_dir = tmp_path / "run"
    monkeypatch.setattr(
        "optical_spec_agent.execution.meep_runner.find_meep_python",
        lambda: [sys.executable],
    )

    result = run_meep_script(
        script_path,
        workdir=run_dir,
        expected_mode="preview",
        save_artifacts=False,
    )

    assert result.success is True
    assert not (run_dir / "stdout.txt").exists()
    assert not (run_dir / "stderr.txt").exists()
    assert not (run_dir / "execution_result.json").exists()
    assert not (run_dir / "run_manifest.json").exists()


def test_smoke_mode_does_not_require_outputs(tmp_path, monkeypatch):
    script_path = tmp_path / "smoke_like.py"
    script_path.write_text("print('smoke done')\n", encoding="utf-8")
    monkeypatch.setattr(
        "optical_spec_agent.execution.meep_runner.find_meep_python",
        lambda: [sys.executable],
    )

    result = run_meep_script(script_path, workdir=tmp_path / "run", expected_mode="smoke")

    assert result.success is True
    assert result.required_outputs == []
    assert result.missing_outputs == []


_meep_available = find_meep_python() is not None


@pytest.mark.skipif(not _meep_available, reason="Meep not available locally")
def test_smoke_script_runs_when_meep_available(tmp_path):
    adapter = MeepAdapter()
    script = adapter.generate(_make_valid_spec(), script_mode="smoke").content
    script_path = tmp_path / "smoke.py"
    script_path.write_text(script, encoding="utf-8")

    result = run_meep_script(script_path, workdir=tmp_path / "run", timeout=120)

    assert result.available is True
    assert result.success is True
    assert "SMOKE TEST PASSED" in result.stdout
