"""Preview paraxial optics helpers."""

from __future__ import annotations

import math

from .models import CalculatorResult, RayVector


def thin_lens(focal_length_mm: float, object_distance_mm: float) -> CalculatorResult:
    if focal_length_mm == 0:
        raise ValueError("focal_length_mm must be non-zero.")
    if object_distance_mm == 0:
        raise ValueError("object_distance_mm must be non-zero.")
    denominator = (1.0 / focal_length_mm) - (1.0 / object_distance_mm)
    if abs(denominator) < 1e-12:
        image_distance_mm = math.inf
        magnification = math.inf
        diagnostics = ["Object is at the focal plane; paraxial image distance tends to infinity."]
    else:
        image_distance_mm = 1.0 / denominator
        magnification = -image_distance_mm / object_distance_mm
        diagnostics = []
    return CalculatorResult(
        result={
            "focal_length_mm": focal_length_mm,
            "object_distance_mm": object_distance_mm,
            "image_distance_mm": image_distance_mm,
            "magnification": magnification,
        },
        assumptions=[
            "Thin-lens paraxial formula.",
            "Small-angle approximation.",
            "No aberration or aperture effects included.",
        ],
        diagnostics=diagnostics,
    )


def abcd_free_space(distance_mm: float) -> list[list[float]]:
    return [[1.0, distance_mm], [0.0, 1.0]]


def abcd_thin_lens(focal_length_mm: float) -> list[list[float]]:
    if focal_length_mm == 0:
        raise ValueError("focal_length_mm must be non-zero.")
    return [[1.0, 0.0], [-1.0 / focal_length_mm, 1.0]]


def propagate_ray(matrix: list[list[float]], ray: dict[str, float] | RayVector) -> CalculatorResult:
    if len(matrix) != 2 or any(len(row) != 2 for row in matrix):
        raise ValueError("matrix must be a 2x2 ABCD matrix.")
    vector = ray if isinstance(ray, RayVector) else RayVector.model_validate(ray)
    height = matrix[0][0] * vector.height_mm + matrix[0][1] * vector.angle_rad
    angle = matrix[1][0] * vector.height_mm + matrix[1][1] * vector.angle_rad
    return CalculatorResult(
        result={
            "input_ray": vector.model_dump(),
            "output_ray": {"height_mm": height, "angle_rad": angle},
            "matrix": matrix,
        },
        assumptions=[
            "Paraxial ray vector uses height and angle in radians.",
            "Matrix is caller-provided or from local preview helpers.",
        ],
    )
