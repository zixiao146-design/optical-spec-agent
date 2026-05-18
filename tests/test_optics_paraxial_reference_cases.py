"""Reference sanity cases for paraxial preview calculators."""

from __future__ import annotations

import pytest

from optical_spec_agent.optics.paraxial import (
    abcd_free_space,
    abcd_thin_lens,
    analyze_two_lens_relay,
    thin_lens,
)


def test_thin_lens_one_to_one_reference_case():
    response = thin_lens(focal_length_mm=50.0, object_distance_mm=100.0)
    assert response.result["image_distance_mm"] == pytest.approx(100.0)
    assert response.result["magnification"] == pytest.approx(-1.0)
    assert response.quality.reference_case == "thin_lens_1_to_1_imaging"


def test_abcd_reference_matrices():
    assert abcd_free_space(25.0) == [[1.0, 25.0], [0.0, 1.0]]
    assert abcd_thin_lens(50.0) == [[1.0, 0.0], [-0.02, 1.0]]


def test_two_lens_four_f_relay_reference_case():
    response = analyze_two_lens_relay(
        f1_mm=50.0,
        f2_mm=50.0,
        separation_mm=100.0,
        object_distance_mm=50.0,
    )
    assert response.result["total_magnification"] == pytest.approx(-1.0)
    assert response.result["second_image_distance_mm"] == pytest.approx(50.0)
    assert response.quality.reference_case == "two_lens_4f_relay_1_to_1"
