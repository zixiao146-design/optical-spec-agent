"""Benchmark closure tests for fiber and polarization preview domains."""

from __future__ import annotations

from optical_spec_agent.examples.domain_benchmarks import (
    evaluate_all_domain_scenarios,
    evaluate_domain_scenario,
)


def test_fiber_and_polarization_benchmarks_now_pass():
    for scenario_id, expected_tool in [
        ("fiber_coupling_preview_positive", "optics.fiber_coupling.gaussian_mode_overlap"),
        ("polarization_optics_preview_positive", "optics.polarization.jones"),
    ]:
        result = evaluate_domain_scenario(scenario_id)
        assert result.status == "pass"
        assert expected_tool in result.actual_tool_calls
        assert result.external_solver_executed is False
        assert result.external_llm_required is False
        assert result.production_grade_validation_claimed is False


def test_application_domain_benchmark_suite_has_no_warnings_after_closure():
    response = evaluate_all_domain_scenarios()
    assert response.summary["fail"] == 0
    assert response.summary["warn"] == 0
    assert response.summary["pass"] == response.summary["total"]
