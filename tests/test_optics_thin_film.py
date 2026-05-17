"""Thin-film preview calculator tests."""

from __future__ import annotations

from optical_spec_agent.optics.thin_film import calculate_thin_film_stack


def test_thin_film_stack_returns_bounded_preview_values():
    response = calculate_thin_film_stack(
        [{"n": 1.22, "k": 0.0, "thickness_nm": 112.7}],
        550.0,
        incident_n=1.0,
        substrate_n=1.5,
    )
    result = response.result
    assert 0 <= result["reflectance"] <= 1
    assert 0 <= result["transmittance"] <= 1
    assert 0 <= result["absorptance_estimate"] <= 1
    assert response.production_grade_validation_claimed is False
    assert response.formal_convergence_proof_claimed is False
    assert response.assumptions
    assert response.limitations

