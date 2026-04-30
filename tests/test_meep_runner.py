"""Tests for the optional Meep execution harness."""

from __future__ import annotations

import json
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
