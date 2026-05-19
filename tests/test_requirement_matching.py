"""Natural-language requirement matching tests."""

from __future__ import annotations

from optical_spec_agent.examples.requirements import match_goal_to_template


def test_english_coating_goal_maps_to_thin_film_template():
    match = match_goal_to_template(
        "Design an anti-reflection coating for glass at 550 nm using local preview calculations."
    )
    assert match.matched_template_id == "thin_film_ar_coating"
    assert match.confidence in {"medium", "high"}
    assert match.external_solver_executed is False
    assert match.external_llm_required is False


def test_chinese_nanoparticle_goal_maps_to_nanoparticle_template():
    match = match_goal_to_template("请为银纳米颗粒位于薄膜上的散射问题生成本地预览工作流。")
    assert match.matched_template_id == "nanoparticle_plasmonics"
    assert match.optical_language_summary["physical_system"] == "nanoparticle_on_film"


def test_chinese_waveguide_goal_maps_to_waveguide_template():
    match = match_goal_to_template("估算 SiN 波导在 1550 nm 是否可能单模。")
    assert match.matched_template_id == "slab_waveguide_single_mode"
    assert "waveguide" in match.optical_language_summary["physical_system"]


def test_gaussian_beam_goal_maps_to_gaussian_template():
    match = match_goal_to_template("Preview Gaussian beam waist and Rayleigh range after focusing.")
    assert match.matched_template_id == "gaussian_beam_focus"
    assert "gaussian" in match.optical_language_summary["physical_system"]


def test_unknown_goal_returns_low_confidence_safe_result():
    match = match_goal_to_template("Help with an unusual optical idea that has no specific system.")
    assert match.matched_template_id is None
    assert match.confidence == "none"
    assert match.status == "needs_review"
    assert match.recommended_questions
    assert match.external_solver_executed is False
    assert match.external_llm_required is False
    assert match.production_grade_validation_claimed is False
