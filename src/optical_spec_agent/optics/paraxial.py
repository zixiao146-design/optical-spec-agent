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


def _matmul(a: list[list[float]], b: list[list[float]]) -> list[list[float]]:
    return [
        [
            a[0][0] * b[0][0] + a[0][1] * b[1][0],
            a[0][0] * b[0][1] + a[0][1] * b[1][1],
        ],
        [
            a[1][0] * b[0][0] + a[1][1] * b[1][0],
            a[1][0] * b[0][1] + a[1][1] * b[1][1],
        ],
    ]


def compose_abcd(elements: list[dict[str, float | str]]) -> CalculatorResult:
    """Compose a paraxial ABCD matrix from free-space and thin-lens elements."""

    matrix = [[1.0, 0.0], [0.0, 1.0]]
    expanded_elements: list[dict[str, float | str]] = []
    for index, element in enumerate(elements):
        element_type = str(element.get("type", "")).strip().lower()
        if element_type == "free_space":
            distance = float(element["distance_mm"])
            element_matrix = abcd_free_space(distance)
            expanded_elements.append({"index": index, "type": "free_space", "distance_mm": distance})
        elif element_type == "thin_lens":
            focal_length = float(element["focal_length_mm"])
            element_matrix = abcd_thin_lens(focal_length)
            expanded_elements.append({"index": index, "type": "thin_lens", "focal_length_mm": focal_length})
        else:
            raise ValueError(f"Unsupported paraxial element type: {element_type}")
        matrix = _matmul(element_matrix, matrix)
    return CalculatorResult(
        result={
            "matrix": matrix,
            "elements": expanded_elements,
            "element_count": len(expanded_elements),
            "summary": f"Composed {len(expanded_elements)} paraxial ABCD elements.",
        },
        assumptions=[
            "Paraxial ABCD matrix composition.",
            "Element order follows input order from object side to image side.",
            "Thin lenses are ideal and free-space sections are homogeneous.",
        ],
    )


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


def analyze_two_lens_relay(
    f1_mm: float,
    f2_mm: float,
    separation_mm: float,
    object_distance_mm: float,
) -> CalculatorResult:
    """Preview a two-lens paraxial relay with sequential thin-lens imaging."""

    if object_distance_mm == 0:
        raise ValueError("object_distance_mm must be non-zero.")
    first = thin_lens(f1_mm, object_distance_mm)
    first_image_distance = first.result["image_distance_mm"]
    diagnostics = list(first.diagnostics)
    if math.isinf(first_image_distance):
        second_object_distance = math.inf
        second_image_distance = math.inf
        total_magnification = math.inf
        diagnostics.append("First image is at infinity; second lens preview is degenerate.")
    else:
        second_object_distance = separation_mm - first_image_distance
        if abs(second_object_distance) < 1e-12:
            second_image_distance = math.inf
            second_magnification = math.inf
            diagnostics.append("Intermediate image falls on the second lens focal plane/object plane.")
        else:
            second = thin_lens(f2_mm, second_object_distance)
            second_image_distance = second.result["image_distance_mm"]
            second_magnification = second.result["magnification"]
            diagnostics.extend(second.diagnostics)
        total_magnification = first.result["magnification"] * second_magnification

    system = compose_abcd(
        [
            {"type": "free_space", "distance_mm": object_distance_mm},
            {"type": "thin_lens", "focal_length_mm": f1_mm},
            {"type": "free_space", "distance_mm": separation_mm},
            {"type": "thin_lens", "focal_length_mm": f2_mm},
        ]
    )
    return CalculatorResult(
        result={
            "f1_mm": f1_mm,
            "f2_mm": f2_mm,
            "separation_mm": separation_mm,
            "object_distance_mm": object_distance_mm,
            "first_image_distance_mm": first_image_distance,
            "second_object_distance_mm": second_object_distance,
            "second_image_distance_mm": second_image_distance,
            "total_magnification": total_magnification,
            "abcd_matrix": system.result["matrix"],
            "summary": "Two-lens relay preview generated with ideal thin-lens steps.",
        },
        assumptions=[
            "Sequential ideal thin-lens imaging.",
            "Paraxial small-angle approximation.",
            "No stop, aperture, aberration, or field curvature analysis included.",
        ],
        diagnostics=diagnostics,
    )


def summarize_paraxial_system(result: CalculatorResult) -> dict[str, float | str | int | None]:
    payload = result.result
    if "total_magnification" in payload:
        return {
            "summary": payload.get("summary", "Two-lens relay preview generated."),
            "total_magnification": payload.get("total_magnification"),
            "second_image_distance_mm": payload.get("second_image_distance_mm"),
            "diagnostic_count": len(result.diagnostics),
        }
    if "matrix" in payload:
        return {
            "summary": payload.get("summary", "Paraxial ABCD system preview generated."),
            "element_count": payload.get("element_count"),
            "matrix": payload.get("matrix"),
            "diagnostic_count": len(result.diagnostics),
        }
    return {
        "summary": (
            f"Thin-lens preview image distance {payload.get('image_distance_mm')} mm "
            f"with magnification {payload.get('magnification')}."
        ),
        "image_distance_mm": payload.get("image_distance_mm"),
        "magnification": payload.get("magnification"),
        "diagnostic_count": len(result.diagnostics),
    }
