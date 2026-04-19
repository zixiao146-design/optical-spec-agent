"""Tests for the Meep adapter (nanoparticle_on_film script generation)."""

import py_compile
import tempfile
from pathlib import Path

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
from optical_spec_agent.adapters.meep import MeepAdapter, AdapterError


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
