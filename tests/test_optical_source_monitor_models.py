from optical_spec_agent.optical_language import (
    OpticalLanguageDiagnostics,
    OpticalMonitorModel,
    OpticalSourceModel,
)


def test_source_monitor_models_are_preview_only_by_default():
    source = OpticalSourceModel(source_type="plane_wave")
    monitor = OpticalMonitorModel(monitor_type="scattering_spectrum", observable="scattering")
    diagnostics = OpticalLanguageDiagnostics()

    assert source.preview_only is True
    assert monitor.preview_only is True
    assert diagnostics.safe_to_preview is True
    assert diagnostics.safe_to_run_solver is False


def test_diagnostics_model_exposes_missing_defaults_and_questions():
    diagnostics = OpticalLanguageDiagnostics(
        missing_required_inputs=["wavelength_range_nm"],
        default_assumptions_applied=["Default to normal-incidence plane wave."],
        ambiguity_notes=["Polarization was defaulted."],
        blocking_questions=["What polarization should be used?"],
    )

    assert "wavelength_range_nm" in diagnostics.missing_required_inputs
    assert "Default to normal-incidence plane wave." in diagnostics.default_assumptions_applied
    assert diagnostics.blocking_questions
    assert diagnostics.safe_to_run_solver is False
