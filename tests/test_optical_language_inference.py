from optical_spec_agent.optical_language import infer_source_monitor_from_goal


def test_chinese_nanoparticle_goal_infers_plane_wave_scattering_defaults():
    result = infer_source_monitor_from_goal(
        "请为一个银纳米颗粒位于薄膜上的散射问题生成本地预览工作流。"
    )

    assert result.matched_template_id == "nanoparticle_plasmonics"
    assert result.source_model.source_type == "plane_wave"
    assert result.source_model.wavelength_start_nm == 400.0
    assert result.source_model.wavelength_stop_nm == 900.0
    assert result.source_model.polarization == "linear_x"
    assert result.monitor_model.monitor_type == "scattering_spectrum"
    assert "scattering" in result.monitor_model.observable


def test_thin_film_goal_infers_reflectance_transmittance():
    result = infer_source_monitor_from_goal("Design an anti-reflection coating for glass at 550 nm.")

    assert result.matched_template_id == "thin_film_ar_coating"
    assert result.source_model.source_type == "plane_wave"
    assert result.monitor_model.monitor_type == "reflectance_transmittance"


def test_gaussian_beam_goal_infers_gaussian_source_and_focal_monitor():
    result = infer_source_monitor_from_goal("Preview Gaussian beam waist and focus.")

    assert result.matched_template_id == "gaussian_beam_focus"
    assert result.source_model.source_type == "gaussian_beam"
    assert result.monitor_model.monitor_type == "focal_spot"


def test_waveguide_goal_infers_mode_source_and_mode_monitor():
    result = infer_source_monitor_from_goal("Estimate single mode slab waveguide behavior.")

    assert result.matched_template_id == "slab_waveguide_single_mode"
    assert result.source_model.source_type == "mode_source"
    assert result.monitor_model.monitor_type == "mode_overlap"


def test_unknown_goal_returns_unknown_models_with_diagnostics():
    result = infer_source_monitor_from_goal("Help me with an unclear optical thing.")

    assert result.matched_template_id is None
    assert result.source_model.source_type == "unknown"
    assert result.monitor_model.monitor_type == "unknown"
    assert result.diagnostics.ambiguity_notes
    assert result.diagnostics.safe_to_preview is True
    assert result.diagnostics.safe_to_run_solver is False
