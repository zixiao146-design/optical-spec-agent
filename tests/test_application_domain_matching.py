"""Application-domain matching tests."""

from __future__ import annotations

from optical_spec_agent.examples.application_domains import match_goal_to_application_domains


def test_chinese_waveguide_goal_matches_slab_waveguide():
    result = match_goal_to_application_domains("请设计一个 1550 nm 单模硅氮波导预览。")
    assert result.confidence == "high"
    assert result.matched_domains == ["slab_waveguide"]


def test_english_coating_goal_matches_thin_film():
    result = match_goal_to_application_domains("Design a thin film anti-reflection coating.")
    assert result.matched_domains == ["thin_film_coating"]
    assert result.external_solver_executed is False


def test_gaussian_beam_goal_matches_gaussian_domain():
    result = match_goal_to_application_domains("Preview Gaussian beam waist and focusing.")
    assert result.matched_domains == ["gaussian_beam_focusing"]


def test_generic_goal_returns_candidates_and_questions():
    result = match_goal_to_application_domains("设计一个光学系统")
    assert result.confidence == "low"
    assert result.candidate_domains
    assert result.recommended_questions
    assert result.no_external_llm_used is True


def test_unknown_goal_is_safe():
    result = match_goal_to_application_domains("Optimize a thermal vacuum package.")
    assert result.confidence == "none"
    assert result.matched_domains == []
    assert result.external_llm_required is False
    assert result.production_grade_validation_claimed is False

