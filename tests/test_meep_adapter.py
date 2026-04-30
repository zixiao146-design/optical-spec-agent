"""Tests for the Meep adapter (nanoparticle_on_film script generation)."""

import ast
import py_compile
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

from optical_spec_agent.adapters.meep import MeepAdapter, AdapterError
from optical_spec_agent.models.base import (
    BoundaryConditionSetting,
    GeometryDefinition,
    MaterialSystem,
    MaterialEntry,
    ParticleInfo,
    SourceSetting,
    SubstrateOrFilmInfo,
    SweepPlan,
    confirmed,
    missing,
)
from optical_spec_agent.models.spec import OpticalSpec
from optical_spec_agent.services.spec_service import SpecService
from optical_spec_agent.adapters.meep.template import render_script

CORE_MEEP_CASE = (
    "用 Meep FDTD 仿真 80 nm 金纳米球放在 100 nm 金膜上，中间 SiO2 gap 为 5 nm，"
    "平面波正入射，波长范围 400-900 nm，输出散射谱，提取共振波长和 FWHM。"
)


def _make_valid_spec() -> OpticalSpec:
    """Build a minimal valid spec for nanoparticle_on_film + meep."""
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


class TestMeepAdapterSuccess:
    def test_can_handle_valid_spec(self):
        adapter = MeepAdapter()
        spec = _make_valid_spec()
        assert adapter.can_handle(spec) is True

    def test_generate_produces_python_script(self):
        adapter = MeepAdapter()
        spec = _make_valid_spec()
        result = adapter.generate(spec)
        assert result.tool == "meep"
        assert result.language == "python"
        assert "import meep as mp" in result.content
        assert "mp.Simulation" in result.content
        assert "mp.Source" in result.content
        assert "mp.PML" in result.content

    def test_generated_script_has_material_defs(self):
        adapter = MeepAdapter()
        spec = _make_valid_spec()
        result = adapter.generate(spec)
        assert "particle_mat" in result.content
        assert "film_mat" in result.content
        assert "Au" in result.content

    def test_generated_script_has_geometry(self):
        adapter = MeepAdapter()
        spec = _make_valid_spec()
        result = adapter.generate(spec)
        assert "mp.Sphere" in result.content
        assert "r_particle" in result.content
        assert "film_thickness" in result.content

    def test_spec_with_sweep_generates_loop(self):
        adapter = MeepAdapter()
        spec = _make_valid_spec()
        spec.simulation.sweep_plan = confirmed(
            SweepPlan(sweep_type="parameter", variable="gap_nm", range_start=5.0, range_end=25.0, step=2.0, unit="nm")
        )
        result = adapter.generate(spec)
        assert "gap_values" in result.content
        assert "Sweeping gap" in result.content

    def test_spec_with_postprocess(self):
        adapter = MeepAdapter()
        spec = _make_valid_spec()
        spec.output.postprocess_target = confirmed([
            {"target_type": "resonance_wavelength"},
            {"target_type": "fwhm_extraction"},
        ])
        result = adapter.generate(spec)
        assert "find_peaks" in result.content
        assert "FWHM" in result.content
        assert "Resonance wavelength" in result.content

    def test_generated_script_passes_py_compile(self):
        """Generated script must be valid Python syntax."""
        adapter = MeepAdapter()
        spec = _make_valid_spec()
        result = adapter.generate(spec)
        with tempfile.NamedTemporaryFile(suffix=".py", mode="w", delete=False) as f:
            f.write(result.content)
            f.flush()
            py_compile.compile(f.name, doraise=True)

    def test_generated_script_has_no_syntax_errors(self):
        """Parse the script as AST to confirm no syntax errors."""
        import ast
        adapter = MeepAdapter()
        spec = _make_valid_spec()
        result = adapter.generate(spec)
        tree = ast.parse(result.content)
        top_imports = [
            n.names[0].name for n in ast.walk(tree) if isinstance(n, ast.Import)
        ]
        assert "meep" in top_imports
        assert "numpy" in top_imports

    def test_golden_output_deterministic(self):
        """Same spec input must produce identical output across calls."""
        adapter = MeepAdapter()
        spec = _make_valid_spec()
        result1 = adapter.generate(spec)
        result2 = adapter.generate(spec)
        assert result1.content == result2.content

    def test_preview_mode_keeps_preview_characteristics(self):
        adapter = MeepAdapter()
        spec = _make_valid_spec()
        result = adapter.generate(spec, script_mode="preview")
        assert "simplified single-Drude" in result.content
        assert "scattering_spectrum.png" in result.content
        assert "postprocess_results.json" not in result.content

    def test_smoke_mode_generates_smoke_script(self):
        adapter = MeepAdapter()
        spec = _make_valid_spec()
        result = adapter.generate(spec, script_mode="smoke")
        assert "SMOKE TEST PASSED" in result.content
        assert "NOT for production" in result.content

    def test_research_preview_mode_generates_research_script(self):
        adapter = MeepAdapter()
        spec = _make_valid_spec()
        result = adapter.generate(spec, script_mode="research-preview")
        assert 'Mode: research-preview' in result.content
        assert "get_flux_data" in result.content
        assert "load_minus_flux_data" in result.content
        assert "scattering_spectrum.csv" in result.content
        assert "postprocess_results.json" in result.content

    def test_research_preview_script_records_stability_options(self):
        adapter = MeepAdapter()
        spec = _make_valid_spec()
        result = adapter.generate(spec, script_mode="research-preview")
        assert "boundary_type=pml" in result.content
        assert "material_mode=library" in result.content
        assert "Courant=Meep default" in result.content
        assert "eps_averaging=Meep default" in result.content

    def test_research_preview_absorber_boundary_uses_absorber(self):
        adapter = MeepAdapter()
        spec = _make_valid_spec()
        result = adapter.generate(
            spec,
            script_mode="research-preview",
            boundary_type="absorber",
        )
        assert "boundary_type=absorber" in result.content
        assert "mp.Absorber(boundary_thickness_um)" in result.content
        assert "mp.PML(boundary_thickness_um)" not in result.content
        ast.parse(result.content)
        with tempfile.NamedTemporaryFile(suffix=".py", mode="w", delete=False) as f:
            f.write(result.content)
            f.flush()
            py_compile.compile(f.name, doraise=True)

    def test_research_preview_courant_and_eps_averaging_options(self):
        adapter = MeepAdapter()
        spec = _make_valid_spec()
        result = adapter.generate(
            spec,
            script_mode="research-preview",
            courant=0.25,
            eps_averaging=False,
        )
        assert '"Courant": 0.25' in result.content
        assert '"eps_averaging": False' in result.content
        ast.parse(result.content)

    def test_research_preview_dielectric_sanity_skips_materials_library(self):
        adapter = MeepAdapter()
        spec = _make_valid_spec()
        result = adapter.generate(
            spec,
            script_mode="research-preview",
            material_mode="dielectric_sanity",
        )
        assert "material_mode=dielectric_sanity" in result.content
        assert "dielectric_sanity is deliberately nonphysical" in result.content
        assert "from meep.materials import" not in result.content
        assert "particle_mat = mp.Medium(epsilon=2.25)" in result.content
        ast.parse(result.content)
        with tempfile.NamedTemporaryFile(suffix=".py", mode="w", delete=False) as f:
            f.write(result.content)
            f.flush()
            py_compile.compile(f.name, doraise=True)

    def test_research_preview_script_passes_ast_and_py_compile(self):
        adapter = MeepAdapter()
        spec = _make_valid_spec()
        result = adapter.generate(spec, script_mode="research_preview")
        ast.parse(result.content)
        with tempfile.NamedTemporaryFile(suffix=".py", mode="w", delete=False) as f:
            f.write(result.content)
            f.flush()
            py_compile.compile(f.name, doraise=True)

    def test_research_preview_output_deterministic(self):
        adapter = MeepAdapter()
        spec = _make_valid_spec()
        result1 = adapter.generate(spec, script_mode="research_preview")
        result2 = adapter.generate(spec, script_mode="research_preview")
        assert result1.content == result2.content

    def test_cli_golden_output_matches_stored(self):
        """Generated output for the standard spec must match stored golden file."""
        golden_path = Path(__file__).parent.parent / "examples" / "outputs" / "meep_nanoparticle_on_film.py"
        if not golden_path.exists():
            return  # skip if golden file not present
        adapter = MeepAdapter()
        spec = _make_valid_spec()
        result = adapter.generate(spec)
        golden_content = golden_path.read_text(encoding="utf-8")
        assert result.content == golden_content


class TestMeepAdapterRejection:
    def test_rejects_wrong_physical_system(self):
        adapter = MeepAdapter()
        spec = _make_valid_spec()
        spec.physics.physical_system = confirmed("waveguide")
        assert adapter.can_handle(spec) is False

    def test_rejects_wrong_solver(self):
        adapter = MeepAdapter()
        spec = _make_valid_spec()
        spec.simulation.solver_method = confirmed("fem")
        assert adapter.can_handle(spec) is False

    def test_rejects_wrong_software(self):
        adapter = MeepAdapter()
        spec = _make_valid_spec()
        spec.simulation.software_tool = confirmed("comsol")
        assert adapter.can_handle(spec) is False

    def test_generate_raises_on_incompatible(self):
        adapter = MeepAdapter()
        spec = _make_valid_spec()
        spec.physics.physical_system = confirmed("waveguide")
        try:
            adapter.generate(spec)
            assert False, "Should have raised AdapterError"
        except AdapterError as e:
            assert "nanoparticle_on_film" in str(e)

    def test_generate_raises_on_missing_particle_info(self):
        adapter = MeepAdapter()
        spec = _make_valid_spec()
        spec.geometry_material.particle_info = missing("no particle info")
        try:
            adapter.generate(spec)
            assert False, "Should have raised AdapterError"
        except AdapterError as e:
            assert "particle_info" in str(e)

    def test_generate_raises_on_missing_film_info(self):
        adapter = MeepAdapter()
        spec = _make_valid_spec()
        spec.geometry_material.substrate_or_film_info = missing("no film info")
        try:
            adapter.generate(spec)
            assert False, "Should have raised AdapterError"
        except AdapterError as e:
            assert "substrate_or_film_info" in str(e)

    def test_generate_uses_default_wavelength_when_missing(self):
        adapter = MeepAdapter()
        spec = _make_valid_spec()
        spec.simulation.source_setting = confirmed(SourceSetting())
        spec.simulation.sweep_plan = missing("no sweep")
        # Should not raise — uses default 400-900 nm
        result = adapter.generate(spec)
        assert "400" in result.content or "0.4" in result.content

    def test_unsupported_particle_shape(self):
        adapter = MeepAdapter()
        spec = _make_valid_spec()
        spec.geometry_material.particle_info = confirmed(
            ParticleInfo(particle_type="star", material="Au", dimensions={"直径": "80 nm"})
        )
        try:
            adapter.generate(spec)
            assert False, "Should have raised AdapterError"
        except AdapterError as e:
            assert "shape" in str(e).lower()


# ---------------------------------------------------------------------------
# Error categories
# ---------------------------------------------------------------------------

class TestAdapterErrorCategories:
    """Verify that AdapterError exposes structured category and field."""

    def _raise(self, *args, **kwargs):
        raise AdapterError(*args, **kwargs)

    def test_error_has_category_attribute(self):
        try:
            self._raise("unsupported_path", "test_field", "detail")
        except AdapterError as e:
            assert e.category == "unsupported_path"

    def test_error_has_field_attribute(self):
        try:
            self._raise("missing_required_field", "geometry_material.particle_info")
        except AdapterError as e:
            assert e.field == "geometry_material.particle_info"

    def test_error_str_format(self):
        try:
            self._raise("invalid_adapter_input", "gap_medium", "unknown 'Foo'")
        except AdapterError as e:
            msg = str(e)
            assert msg.startswith("[invalid_adapter_input]")
            assert "gap_medium" in msg
            assert "unknown 'Foo'" in msg

    def test_unsupported_path_wrong_system(self):
        adapter = MeepAdapter()
        spec = _make_valid_spec()
        spec.physics.physical_system = confirmed("waveguide")
        try:
            adapter.generate(spec)
            assert False
        except AdapterError as e:
            assert e.category == "unsupported_path"

    def test_missing_required_field_particle(self):
        adapter = MeepAdapter()
        spec = _make_valid_spec()
        spec.geometry_material.particle_info = missing("none")
        try:
            adapter.generate(spec)
            assert False
        except AdapterError as e:
            assert e.category == "missing_required_field"
            assert "particle_info" in e.field

    def test_missing_required_field_film_material(self):
        adapter = MeepAdapter()
        spec = _make_valid_spec()
        spec.geometry_material.substrate_or_film_info = confirmed(
            SubstrateOrFilmInfo(has_film=True, film_material="", film_thickness="100 nm")
        )
        try:
            adapter.generate(spec)
            assert False
        except AdapterError as e:
            assert e.category == "missing_required_field"
            assert "film_material" in e.field

    def test_invalid_adapter_input_bad_shape(self):
        adapter = MeepAdapter()
        spec = _make_valid_spec()
        spec.geometry_material.particle_info = confirmed(
            ParticleInfo(particle_type="star", material="Au", dimensions={"直径": "80 nm"})
        )
        try:
            adapter.generate(spec)
            assert False
        except AdapterError as e:
            assert e.category == "unsupported_path"
            assert "shape" in e.field

    def test_invalid_adapter_input_unknown_gap(self):
        adapter = MeepAdapter()
        spec = _make_valid_spec()
        spec.geometry_material.gap_medium = confirmed("Unobtanium")
        try:
            adapter.generate(spec)
            assert False
        except AdapterError as e:
            assert e.category == "invalid_adapter_input"
            assert "gap_medium" in e.field

    def test_invalid_adapter_input_unparseable_dimensions(self):
        adapter = MeepAdapter()
        spec = _make_valid_spec()
        spec.geometry_material.particle_info = confirmed(
            ParticleInfo(particle_type="sphere", material="Au", dimensions={"note": "big"})
        )
        try:
            adapter.generate(spec)
            assert False
        except AdapterError as e:
            assert e.category == "invalid_adapter_input"
            assert "dimensions" in e.field


# ---------------------------------------------------------------------------
# Default value tracking
# ---------------------------------------------------------------------------

class TestAdapterDefaults:
    """Verify that defaults are tracked and annotated in generated scripts."""

    def test_full_spec_no_defaults(self):
        adapter = MeepAdapter()
        spec = _make_valid_spec()
        model = adapter._translate(spec)
        assert model.defaults_applied == []

    def test_missing_gap_medium_tracked(self):
        adapter = MeepAdapter()
        spec = _make_valid_spec()
        spec.geometry_material.gap_medium = missing("none")
        model = adapter._translate(spec)
        assert any("gap_medium" in d for d in model.defaults_applied)

    def test_missing_wavelength_tracked(self):
        adapter = MeepAdapter()
        spec = _make_valid_spec()
        spec.simulation.source_setting = confirmed(SourceSetting())
        spec.simulation.sweep_plan = missing("none")
        model = adapter._translate(spec)
        assert any("wavelength_range" in d for d in model.defaults_applied)

    def test_missing_film_thickness_tracked(self):
        adapter = MeepAdapter()
        spec = _make_valid_spec()
        spec.geometry_material.substrate_or_film_info = confirmed(
            SubstrateOrFilmInfo(has_film=True, film_material="Au", film_thickness="")
        )
        model = adapter._translate(spec)
        assert any("film_thickness" in d for d in model.defaults_applied)

    def test_defaults_annotated_in_script_header(self):
        adapter = MeepAdapter()
        spec = _make_valid_spec()
        spec.geometry_material.gap_medium = missing("none")
        spec.simulation.source_setting = confirmed(SourceSetting())
        spec.simulation.sweep_plan = missing("none")
        result = adapter.generate(spec)
        assert "Adapter-applied defaults" in result.content
        assert "gap_medium" in result.content

    def test_no_defaults_annotation_when_all_provided(self):
        adapter = MeepAdapter()
        spec = _make_valid_spec()
        result = adapter.generate(spec)
        assert "Adapter-applied defaults" not in result.content


class TestAdapterReadiness:
    def test_validate_ready_rejects_missing_particle_size(self):
        adapter = MeepAdapter()
        spec = _make_valid_spec()
        spec.geometry_material.particle_info = confirmed(
            ParticleInfo(particle_type="sphere", material="Au", dimensions={})
        )
        readiness = adapter.validate_ready(spec)
        assert readiness.adapter_ready is False
        assert any("particle size" in error for error in readiness.errors)

    def test_validate_ready_core_case(self):
        adapter = MeepAdapter()
        spec = SpecService().process(CORE_MEEP_CASE, task_id="core-readiness")
        readiness = adapter.validate_ready(spec)
        assert readiness.adapter_ready is True
        assert readiness.errors == []


# ---------------------------------------------------------------------------
# Smoke run helpers
# ---------------------------------------------------------------------------

_meep_cmd: list[str] | None = None


def _find_meep_python() -> list[str] | None:
    """Return a command prefix that can run Python with Meep importable, or None."""
    global _meep_cmd
    if _meep_cmd is not None:
        return _meep_cmd or None

    # 1. Try current interpreter
    try:
        import meep  # noqa: F401
        _meep_cmd = [sys.executable]
        return _meep_cmd
    except ImportError:
        pass

    # 2. Try micromamba env named "meep"
    if shutil.which("micromamba"):
        try:
            r = subprocess.run(
                ["micromamba", "run", "-n", "meep", "python", "-c", "import meep"],
                capture_output=True, timeout=30,
            )
            if r.returncode == 0:
                _meep_cmd = ["micromamba", "run", "-n", "meep", "python"]
                return _meep_cmd
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass

    _meep_cmd = []
    return None


_meep_available = _find_meep_python() is not None


class TestMeepSmokeRun:
    """Generate a minimal Meep script and actually run it.

    These tests are auto-skipped when Meep is not installed locally.
    """

    @staticmethod
    def _make_smoke_script() -> str:
        adapter = MeepAdapter()
        spec = _make_valid_spec()
        model = adapter._translate(spec)
        smoke_model = model.model_copy(update={"smoke": True})
        return render_script(smoke_model)

    def test_smoke_script_is_valid_python(self):
        """Smoke script must be syntactically valid Python even without Meep."""
        script = self._make_smoke_script()
        ast.parse(script)
        # Also verify via py_compile (catches some edge cases)
        with tempfile.NamedTemporaryFile(suffix=".py", mode="w", delete=False) as f:
            f.write(script)
            f.flush()
            py_compile.compile(f.name, doraise=True)

    @pytest.mark.skipif(not _meep_available, reason="Meep not available locally")
    def test_smoke_script_runs(self, tmp_path):
        """Generate and execute smoke script through Meep."""
        script = self._make_smoke_script()

        script_path = tmp_path / "smoke_test.py"
        script_path.write_text(script)

        cmd = _find_meep_python() + [str(script_path)]
        result = subprocess.run(
            cmd, capture_output=True, timeout=120, cwd=str(tmp_path),
        )
        assert result.returncode == 0, (
            f"Smoke script failed with exit code {result.returncode}.\n"
            f"stdout: {result.stdout.decode(errors='replace')}\n"
            f"stderr: {result.stderr.decode(errors='replace')}"
        )
        assert b"SMOKE TEST PASSED" in result.stdout
