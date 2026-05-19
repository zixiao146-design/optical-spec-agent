"""Application-domain benchmark evaluator tests."""

from __future__ import annotations

from optical_spec_agent.examples.domain_benchmarks import (
    evaluate_all_domain_scenarios,
    evaluate_domain_scenario,
)


def test_application_domain_benchmark_evaluator_has_no_failures():
    response = evaluate_all_domain_scenarios()
    assert response.status == "ok"
    assert response.summary["total"] >= 19
    assert response.summary["fail"] == 0
    assert response.summary["positive"] >= 10
    assert response.summary["ambiguous"] >= 3
    assert response.summary["underconstrained"] >= 3
    assert response.summary["unsupported"] >= 3
    assert response.external_solver_executed is False
    assert response.external_llm_required is False
    assert response.production_grade_validation_claimed is False


def test_positive_scenarios_pass_or_warn_without_unsafe_calls():
    response = evaluate_all_domain_scenarios()
    positives = [item for item in response.results if item.scenario_id.endswith("_positive")]
    assert positives
    for result in positives:
        assert result.status in {"pass", "warn"}
        assert result.external_solver_executed is False
        assert result.external_llm_required is False
        assert result.production_grade_validation_claimed is False


def test_ambiguous_scenarios_keep_candidates_and_questions():
    for scenario_id in (
        "waveguide_or_coating_ambiguous",
        "lens_or_gaussian_focus_ambiguous",
        "generic_optical_system_ambiguous",
    ):
        result = evaluate_domain_scenario(scenario_id)
        assert result.status in {"pass", "warn"}
        assert len(result.actual_candidates) >= 2
        assert result.actual_questions
        assert result.external_solver_executed is False


def test_unsupported_requests_are_blocked_or_deferred():
    for scenario_id in (
        "full_zemax_optimization_request",
        "full_lumerical_fdtd_request",
        "production_grade_validation_request",
    ):
        result = evaluate_domain_scenario(scenario_id)
        assert result.status == "pass"
        assert "external_solver" in result.blocked_actions
        assert result.actual_tool_calls == []
        assert result.external_solver_executed is False
        assert result.external_llm_required is False
