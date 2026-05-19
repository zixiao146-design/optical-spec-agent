"""Application-domain material/template cross-check tests."""

from __future__ import annotations

from optical_spec_agent.examples.domain_cross_check import (
    cross_check_all_application_domains,
    cross_check_application_domain,
)


def test_cross_check_all_application_domains_returns_all_domains():
    response = cross_check_all_application_domains()
    assert response.summary["total"] == 10
    assert response.summary["fail"] == 0
    assert response.external_solver_executed is False
    assert response.production_grade_validation_claimed is False


def test_core_domains_pass_material_template_tool_checks():
    for domain_id in ("thin_film_coating", "slab_waveguide", "nanoparticle_plasmonics"):
        check = cross_check_application_domain(domain_id)
        assert check.status == "pass"
        assert check.template_coverage is True
        assert check.material_suitability_coverage is True
        assert check.missing_input_questions_present is True
        assert check.expected_tool_status == "covered"


def test_fiber_and_polarization_are_partial_with_explanation():
    for domain_id in ("fiber_coupling_preview", "polarization_optics_preview"):
        check = cross_check_application_domain(domain_id)
        assert check.status == "warning"
        assert check.deferred_capability
        assert check.external_solver_executed is False
        assert check.preview_only is True

