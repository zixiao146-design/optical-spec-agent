"""Design case cross-check tests."""

from __future__ import annotations

from optical_spec_agent.examples.cross_check import (
    cross_check_all_design_cases,
    cross_check_design_case,
)


def test_cross_check_all_design_cases_returns_all_examples():
    response = cross_check_all_design_cases()
    checks = {check.example_id: check for check in response.cross_checks}
    assert set(checks) == {
        "nanoparticle_plasmonics",
        "thin_film_coating",
        "waveguide_mode",
        "photonic_crystal_band",
        "dielectric_metasurface_preview",
        "lens_raytrace_preview",
    }
    assert response.summary["total"] == 6
    assert response.summary["fail"] == 0
    assert response.external_solver_executed is False
    assert response.external_llm_required is False
    assert response.production_grade_validation_claimed is False


def test_design_case_expected_calculator_mappings_pass():
    expected = {
        "thin_film_coating": "optics.thin_film",
        "waveguide_mode": "optics.waveguide",
        "lens_raytrace_preview": "optics.paraxial",
    }
    for example_id, calculator in expected.items():
        check = cross_check_design_case(example_id)
        assert check.status == "pass"
        assert check.expected_calculator == calculator
        assert check.calculator_called is True
        assert any(name.startswith(calculator) for name in check.tool_call_ledger_entries)
        assert check.safety_flags.external_solver_executed is False


def test_design_cases_without_scalar_calculator_keep_adapter_trace_path():
    for example_id in [
        "nanoparticle_plasmonics",
        "photonic_crystal_band",
        "dielectric_metasurface_preview",
    ]:
        check = cross_check_design_case(example_id)
        assert check.status == "pass"
        assert check.expected_calculator is None
        assert "agent_trace.build" in check.tool_call_ledger_entries
        assert "material_catalog.suggest" in check.tool_call_ledger_entries
        assert check.adapter_recommendation
        assert check.safety_flags.production_grade_validation_claimed is False
