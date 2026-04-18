"""Tests for the spec validator."""

from optical_spec_agent.models.base import (
    SourceSetting,
    StatusField,
    confirmed,
    missing,
)
from optical_spec_agent.models.spec import OpticalSpec
from optical_spec_agent.validators.spec_validator import SpecValidator


class TestSpecValidator:
    def test_empty_spec_not_executable(self):
        spec = OpticalSpec()
        validator = SpecValidator()
        result = validator.validate(spec)
        assert result.validation_status.is_executable is False
        assert len(result.validation_status.errors) > 0

    def test_simulation_spec_executable(self):
        spec = OpticalSpec()
        spec.task.task_type = confirmed("simulation")
        spec.task.research_goal = confirmed("research goal")
        spec.physics.model_dimension = confirmed("3d")
        spec.simulation.solver_method = confirmed("fdtd")
        spec.simulation.software_tool = confirmed("meep")
        spec.simulation.excitation_source = confirmed("plane_wave")
        spec.simulation.source_setting = confirmed(SourceSetting(source_type="plane_wave"))
        spec.simulation.boundary_condition = confirmed({"x_min": "PML"})
        spec.simulation.monitor_setting = confirmed({"monitor_type": "frequency_domain"})
        validator = SpecValidator()
        result = validator.validate(spec)
        assert result.validation_status.is_executable is True
        assert result.validation_status.errors == []

    def test_warnings_for_missing_recommended(self):
        spec = OpticalSpec()
        spec.task.task_type = confirmed("simulation")
        spec.task.research_goal = confirmed("goal")
        spec.simulation.solver_method = confirmed("fdtd")
        spec.simulation.software_tool = confirmed("lumerical")
        spec.simulation.excitation_source = confirmed("tfsf")
        spec.simulation.source_setting = confirmed(SourceSetting(source_type="tfsf"))
        spec.simulation.boundary_condition = confirmed({"x_min": "PML"})
        spec.simulation.monitor_setting = confirmed({"monitor_type": "frequency_domain"})
        validator = SpecValidator()
        result = validator.validate(spec)
        assert len(result.validation_status.warnings) > 0

    def test_solver_software_consistency_warning(self):
        spec = OpticalSpec()
        spec.task.task_type = confirmed("simulation")
        spec.task.research_goal = confirmed("goal")
        spec.simulation.solver_method = confirmed("fem")
        spec.simulation.software_tool = confirmed("lumerical")
        spec.simulation.excitation_source = confirmed("plane_wave")
        spec.simulation.source_setting = confirmed(SourceSetting())
        spec.simulation.boundary_condition = confirmed({"x_min": "PML"})
        spec.simulation.monitor_setting = confirmed({})
        validator = SpecValidator()
        result = validator.validate(spec)
        assert any("FEM" in w for w in result.validation_status.warnings)

    def test_nanoparticle_on_film_rules(self):
        spec = OpticalSpec()
        spec.task.task_type = confirmed("simulation")
        spec.task.research_goal = confirmed("goal")
        spec.physics.physical_system = confirmed("nanoparticle_on_film")
        spec.simulation.solver_method = confirmed("fdtd")
        spec.simulation.software_tool = confirmed("lumerical")
        spec.simulation.excitation_source = confirmed("tfsf")
        spec.simulation.source_setting = confirmed(SourceSetting(source_type="tfsf"))
        spec.simulation.boundary_condition = confirmed({"x_min": "PML"})
        spec.simulation.monitor_setting = confirmed({})
        # particle_info, substrate_or_film_info, gap_medium are all missing → error
        validator = SpecValidator()
        result = validator.validate(spec)
        nanoparticle_issues = [
            e for e in result.validation_status.errors if "nanoparticle_on_film" in e
        ]
        assert len(nanoparticle_issues) >= 1

    def test_postprocess_needs_spectrum(self):
        spec = OpticalSpec()
        spec.task.task_type = confirmed("fitting")
        spec.task.research_goal = confirmed("goal")
        spec.output.postprocess_target = confirmed([
            {"target_type": "fwhm_extraction"}
        ])
        spec.output.output_observables = confirmed(["field_distribution"])
        validator = SpecValidator()
        result = validator.validate(spec)
        assert any("spectrum" in e for e in result.validation_status.errors)

    def test_postprocess_fwhm_with_spectrum_ok(self):
        """FWHM extraction with a spectrum observable should not error."""
        spec = OpticalSpec()
        spec.task.task_type = confirmed("fitting")
        spec.task.research_goal = confirmed("goal")
        spec.output.postprocess_target = confirmed([
            {"target_type": "fwhm_extraction"}
        ])
        spec.output.output_observables = confirmed(["scattering_spectrum"])
        validator = SpecValidator()
        result = validator.validate(spec)
        assert not any("spectrum" in e for e in result.validation_status.errors)

    def test_postprocess_t2_without_spectrum_errors(self):
        """T2 extraction without spectrum observable should be an error."""
        spec = OpticalSpec()
        spec.task.task_type = confirmed("fitting")
        spec.task.research_goal = confirmed("goal")
        spec.output.postprocess_target = confirmed([
            {"target_type": "T2_extraction"}
        ])
        spec.output.output_observables = confirmed(["field_enhancement"])
        validator = SpecValidator()
        result = validator.validate(spec)
        assert any("spectrum" in e for e in result.validation_status.errors)

    def test_fdtd_missing_three_critical_settings_errors(self):
        """FDTD simulation missing 3+ critical settings should produce a specific error."""
        spec = OpticalSpec()
        spec.task.task_type = confirmed("simulation")
        spec.task.research_goal = confirmed("goal")
        spec.simulation.solver_method = confirmed("fdtd")
        spec.simulation.software_tool = confirmed("meep")
        # excitation_source, source_setting, boundary_condition, monitor_setting all missing
        validator = SpecValidator()
        result = validator.validate(spec)
        fdtd_errors = [e for e in result.validation_status.errors if "FDTD" in e]
        assert len(fdtd_errors) >= 1

    def test_fdtd_with_source_ok(self):
        """FDTD simulation with source present should not trigger FDTD-specific error."""
        spec = OpticalSpec()
        spec.task.task_type = confirmed("simulation")
        spec.task.research_goal = confirmed("goal")
        spec.simulation.solver_method = confirmed("fdtd")
        spec.simulation.software_tool = confirmed("meep")
        spec.simulation.excitation_source = confirmed("plane_wave")
        spec.simulation.source_setting = confirmed(SourceSetting(source_type="plane_wave"))
        # boundary + monitor still missing, but only 2 missing → no FDTD-specific error
        validator = SpecValidator()
        result = validator.validate(spec)
        fdtd_errors = [e for e in result.validation_status.errors if "FDTD" in e and "缺少" in e]
        assert len(fdtd_errors) == 0

    def test_fem_missing_boundary_and_monitor_errors(self):
        """FEM simulation missing both boundary and monitor should produce specific error."""
        spec = OpticalSpec()
        spec.task.task_type = confirmed("simulation")
        spec.task.research_goal = confirmed("goal")
        spec.simulation.solver_method = confirmed("fem")
        spec.simulation.software_tool = confirmed("comsol")
        spec.simulation.excitation_source = confirmed("port")
        spec.simulation.source_setting = confirmed(SourceSetting(source_type="port"))
        # boundary + monitor missing
        validator = SpecValidator()
        result = validator.validate(spec)
        fem_errors = [e for e in result.validation_status.errors if "FEM" in e]
        assert len(fem_errors) >= 1

    def test_nanoparticle_on_film_all_geom_missing_errors(self):
        """nanoparticle_on_film with all geometry info missing should error."""
        spec = OpticalSpec()
        spec.task.task_type = confirmed("simulation")
        spec.task.research_goal = confirmed("goal")
        spec.physics.physical_system = confirmed("nanoparticle_on_film")
        spec.simulation.solver_method = confirmed("fdtd")
        spec.simulation.software_tool = confirmed("meep")
        spec.simulation.excitation_source = confirmed("tfsf")
        spec.simulation.source_setting = confirmed(SourceSetting(source_type="tfsf"))
        spec.simulation.boundary_condition = confirmed({"x_min": "PML"})
        spec.simulation.monitor_setting = confirmed({"monitor_type": "frequency_domain"})
        # particle_info, substrate_or_film_info, gap_medium all missing
        validator = SpecValidator()
        result = validator.validate(spec)
        geom_errors = [e for e in result.validation_status.errors if "nanoparticle_on_film" in e]
        assert len(geom_errors) >= 1

    def test_nanoparticle_on_film_partial_geom_only_warnings(self):
        """nanoparticle_on_film with 1-2 geometry fields missing should only warn."""
        spec = OpticalSpec()
        spec.task.task_type = confirmed("simulation")
        spec.task.research_goal = confirmed("goal")
        spec.physics.physical_system = confirmed("nanoparticle_on_film")
        spec.simulation.solver_method = confirmed("fdtd")
        spec.simulation.software_tool = confirmed("meep")
        spec.simulation.excitation_source = confirmed("tfsf")
        spec.simulation.source_setting = confirmed(SourceSetting(source_type="tfsf"))
        spec.simulation.boundary_condition = confirmed({"x_min": "PML"})
        spec.simulation.monitor_setting = confirmed({"monitor_type": "frequency_domain"})
        spec.geometry_material.particle_info = confirmed({"particle_type": "sphere", "material": "Au"})
        # substrate_or_film_info, gap_medium still missing (2 of 3)
        validator = SpecValidator()
        result = validator.validate(spec)
        geom_errors = [e for e in result.validation_status.errors if "nanoparticle_on_film" in e and "严重" in e]
        assert len(geom_errors) == 0
        geom_warnings = [w for w in result.validation_status.warnings if "nanoparticle_on_film" in w]
        assert len(geom_warnings) >= 1

    def test_physical_system_structure_type_mismatch_warning(self):
        """Inconsistent physical_system + structure_type should warn."""
        spec = OpticalSpec()
        spec.task.task_type = confirmed("simulation")
        spec.task.research_goal = confirmed("goal")
        spec.physics.physical_system = confirmed("waveguide")
        spec.physics.structure_type = confirmed("sphere_on_film")
        spec.simulation.solver_method = confirmed("fdtd")
        spec.simulation.software_tool = confirmed("meep")
        spec.simulation.excitation_source = confirmed("plane_wave")
        spec.simulation.source_setting = confirmed(SourceSetting(source_type="plane_wave"))
        spec.simulation.boundary_condition = confirmed({"x_min": "PML"})
        spec.simulation.monitor_setting = confirmed({"monitor_type": "frequency_domain"})
        validator = SpecValidator()
        result = validator.validate(spec)
        combo_warnings = [w for w in result.validation_status.warnings if "组合不常见" in w]
        assert len(combo_warnings) >= 1

    def test_physical_system_structure_type_valid_no_warning(self):
        """Consistent physical_system + structure_type should not warn."""
        spec = OpticalSpec()
        spec.task.task_type = confirmed("simulation")
        spec.task.research_goal = confirmed("goal")
        spec.physics.physical_system = confirmed("nanoparticle_on_film")
        spec.physics.structure_type = confirmed("sphere_on_film")
        spec.simulation.solver_method = confirmed("fdtd")
        spec.simulation.software_tool = confirmed("meep")
        spec.simulation.excitation_source = confirmed("plane_wave")
        spec.simulation.source_setting = confirmed(SourceSetting(source_type="plane_wave"))
        spec.simulation.boundary_condition = confirmed({"x_min": "PML"})
        spec.simulation.monitor_setting = confirmed({"monitor_type": "frequency_domain"})
        validator = SpecValidator()
        result = validator.validate(spec)
        combo_warnings = [w for w in result.validation_status.warnings if "组合不常见" in w]
        assert len(combo_warnings) == 0
