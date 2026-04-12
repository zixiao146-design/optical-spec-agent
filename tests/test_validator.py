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
        # particle_info, substrate_or_film_info, gap_medium are missing
        validator = SpecValidator()
        result = validator.validate(spec)
        nanoparticle_warnings = [w for w in result.validation_status.warnings if "nanoparticle_on_film" in w]
        assert len(nanoparticle_warnings) >= 1

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
        assert any("spectrum" in w for w in result.validation_status.warnings)
