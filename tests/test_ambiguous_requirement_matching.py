"""Ambiguous natural-language requirement matching tests."""

from optical_spec_agent.examples.requirements import match_goal_to_template


def test_generic_optical_system_returns_no_template_and_questions():
    result = match_goal_to_template("设计一个光学系统")
    assert result.confidence == "none"
    assert result.matched_template_id is None
    assert result.candidate_templates == []
    assert result.recommended_questions
    assert result.no_external_llm_used is True


def test_waveguide_and_coating_goal_returns_multiple_candidates():
    result = match_goal_to_template("做一个波导和薄膜的设计")
    assert result.confidence == "low"
    assert "slab_waveguide_single_mode" in result.candidate_templates
    assert "thin_film_ar_coating" in result.candidate_templates
    assert result.recommended_questions


def test_clear_nanoparticle_goal_returns_high_confidence():
    result = match_goal_to_template("请为银纳米颗粒散射生成本地预览工作流")
    assert result.confidence == "high"
    assert result.matched_template_id == "nanoparticle_plasmonics"
    assert result.no_external_llm_used is True


def test_unknown_goal_is_safe_low_or_none_confidence():
    result = match_goal_to_template("Create a quantum sparkle optimizer for an undefined optical artifact.")
    assert result.confidence == "none"
    assert result.matched_template_id is None
    assert result.status == "needs_review"
    assert result.recommended_questions
