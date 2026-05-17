"""Paraxial preview calculator tests."""

from __future__ import annotations

from optical_spec_agent.optics.paraxial import (
    abcd_free_space,
    abcd_thin_lens,
    propagate_ray,
    thin_lens,
)


def test_thin_lens_formula_sanity():
    response = thin_lens(focal_length_mm=50.0, object_distance_mm=200.0)
    assert round(response.result["image_distance_mm"], 6) == round(200 / 3, 6)
    assert round(response.result["magnification"], 6) == round(-1 / 3, 6)
    assert response.production_grade_validation_claimed is False


def test_abcd_matrix_and_ray_sanity():
    space = abcd_free_space(10.0)
    lens = abcd_thin_lens(50.0)
    assert space == [[1.0, 10.0], [0.0, 1.0]]
    assert lens == [[1.0, 0.0], [-0.02, 1.0]]
    propagated = propagate_ray(space, {"height_mm": 1.0, "angle_rad": 0.1})
    assert propagated.result["output_ray"]["height_mm"] == 2.0
    assert propagated.result["output_ray"]["angle_rad"] == 0.1

