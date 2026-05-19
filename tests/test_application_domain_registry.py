"""Application-domain registry tests."""

from __future__ import annotations

from optical_spec_agent.examples.application_domains import list_application_domains


def test_application_domain_registry_has_ten_preview_domains():
    domains = list_application_domains()
    assert len(domains) == 10
    ids = {domain.domain_id for domain in domains}
    assert {
        "nanoparticle_plasmonics",
        "thin_film_coating",
        "slab_waveguide",
        "photonic_crystal",
        "dielectric_metasurface",
        "lens_ray_optics",
        "gaussian_beam_focusing",
        "imaging_system_preview",
        "fiber_coupling_preview",
        "polarization_optics_preview",
    } == ids
    for domain in domains:
        assert domain.suggested_materials
        assert domain.linked_requirement_templates
        assert domain.recommended_questions
        assert domain.common_missing_inputs
        assert domain.preview_only is True
        assert domain.production_grade_validation_claimed is False
        assert domain.formal_convergence_proof_claimed is False
    by_id = {domain.domain_id: domain for domain in domains}
    assert "optics.fiber_coupling.gaussian_mode_overlap" in by_id["fiber_coupling_preview"].expected_calculators
    assert "optics.polarization.jones" in by_id["polarization_optics_preview"].expected_calculators
