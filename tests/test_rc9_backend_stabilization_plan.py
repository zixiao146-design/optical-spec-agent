"""rc9 backend stabilization plan checks."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_rc9_backend_stabilization_plan_has_expected_sections():
    path = ROOT / "docs" / "rc9_backend_stabilization_plan.md"
    assert path.exists()
    text = path.read_text(encoding="utf-8")

    for phrase in [
        "## Done / stable enough",
        "## Needs monitoring",
        "## Deferred",
        "## Future",
    ]:
        assert phrase in text


def test_rc9_backend_stabilization_plan_records_backend_evidence():
    text = (ROOT / "docs" / "rc9_backend_stabilization_plan.md").read_text(
        encoding="utf-8"
    )

    for phrase in [
        "Application domain benchmarks: 19 pass / 0 warn / 0 fail",
        "Optional solver evidence closed for Gmsh, Optiland, Meep, and MPB",
        "Backend validation maturity matrix is available",
        "Preview boundary policy is available",
        "Material provenance",
        "Backend evidence pack",
        "Elmer Level 3",
        "No production-grade physical validation is claimed",
    ]:
        assert phrase in text
