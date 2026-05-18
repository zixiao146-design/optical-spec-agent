from optical_spec_agent.optical_language import (
    diagnose_missing_inputs,
    infer_source_monitor_from_goal,
)


def test_missing_wavelength_reported_for_unknown_goal():
    diagnostics = diagnose_missing_inputs(goal="An optical design with no source or monitor context.")

    assert "wavelength_or_frequency" in diagnostics.missing_required_inputs
    assert diagnostics.blocking_questions
    assert diagnostics.safe_to_preview is True
    assert diagnostics.safe_to_run_solver is False


def test_defaulted_nanoparticle_polarization_is_recorded_not_blocking_preview():
    inference = infer_source_monitor_from_goal(
        "请为一个银纳米颗粒位于薄膜上的散射问题生成本地预览工作流。"
    )

    assert "polarization" in inference.source_model.defaulted_fields
    assert any("linear_x" in item for item in inference.diagnostics.default_assumptions_applied)
    assert any("Polarization was defaulted" in item for item in inference.diagnostics.ambiguity_notes)
    assert inference.diagnostics.safe_to_preview is True
    assert inference.diagnostics.safe_to_run_solver is False


def test_explicit_spec_can_satisfy_source_monitor_aliases():
    diagnostics = diagnose_missing_inputs(
        goal="An unclear optical design.",
        spec={
            "simulation": {
                "source_setting": {"wavelength_range": "500-700 nm", "polarization": "TE"},
                "monitor_setting": {"region": "near field", "observable": "field"},
            }
        },
    )

    assert "wavelength_or_frequency" not in diagnostics.missing_required_inputs
    assert diagnostics.safe_to_run_solver is False
