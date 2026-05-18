"""Failure-mode checks for local optical preview calculators."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from optical_spec_agent.api.app import app
from optical_spec_agent.optics.gaussian_beam import gaussian_beam_parameters, propagate_gaussian_beam_series
from optical_spec_agent.optics.paraxial import abcd_thin_lens
from optical_spec_agent.optics.thin_film import calculate_thin_film_stack
from optical_spec_agent.optics.waveguide import slab_waveguide_sweep, slab_waveguide_v_number


@pytest.mark.parametrize(
    ("callable_obj", "args", "match"),
    [
        (gaussian_beam_parameters, (), "positive"),
        (abcd_thin_lens, (0.0,), "non-zero"),
    ],
)
def test_common_invalid_inputs_raise_value_error(callable_obj, args, match):
    if callable_obj is gaussian_beam_parameters:
        args = (-1.0, 10.0)
    with pytest.raises(ValueError, match=match):
        callable_obj(*args)


def test_thin_film_rejects_invalid_indices_and_zero_thickness():
    with pytest.raises(ValueError, match="incident_n and substrate_n"):
        calculate_thin_film_stack([], 550.0, incident_n=0.0, substrate_n=1.5)
    with pytest.raises(ValueError, match="Layer refractive index"):
        calculate_thin_film_stack([{"n": 0.0, "thickness_nm": 100.0}], 550.0)
    with pytest.raises(ValueError, match="Layer thickness"):
        calculate_thin_film_stack([{"n": 1.5, "thickness_nm": 0.0}], 550.0)


def test_invalid_sweep_points_raise_value_error():
    with pytest.raises(ValueError, match="points"):
        propagate_gaussian_beam_series(1064.0, 10.0, 0.0, 1.0, 1)
    with pytest.raises(ValueError, match="points"):
        slab_waveguide_sweep(2.0, 1.5, 1550.0, 0.1, 0.5, 1)


def test_waveguide_rejects_unguided_index_case():
    with pytest.raises(ValueError, match="core_n must be greater"):
        slab_waveguide_v_number(1.44, 1.44, 0.3, 1550.0)


def test_api_calculator_failure_returns_stable_error_without_solver_or_llm():
    client = TestClient(app)
    response = client.post(
        "/api/optics/waveguide-estimate",
        json={"core_n": 1.44, "cladding_n": 1.5, "core_thickness_um": 0.3, "wavelength_nm": 1550.0},
    )
    assert response.status_code == 400
    body = response.json()
    assert body["status"] == "error"
    assert body["error_code"] == "preview_generation_error"
    assert body["external_solver_executed"] is False
    assert body["external_llm_required"] is False
    assert body["production_grade_validation_claimed"] is False
    assert body["formal_convergence_proof_claimed"] is False
