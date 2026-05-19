"""Adapter golden coverage report tests."""

from __future__ import annotations

from optical_spec_agent.optical_language.golden_coverage import (
    build_adapter_golden_coverage_report,
)


def test_adapter_golden_coverage_report_covers_all_registered_preview_adapters():
    report = build_adapter_golden_coverage_report()
    assert report.status == "ok"
    assert set(report.adapters_covered) == {"meep", "mpb", "gmsh", "elmer", "optiland"}
    assert report.missing_adapters == []
    assert len(report.coverage_items) == 5
    assert report.external_solver_executed is False
    assert report.external_llm_required is False
    assert report.preview_only is True
    assert report.production_grade_validation_claimed is False
    assert report.formal_convergence_proof_claimed is False
    assert all(item.coverage_status == "pass" for item in report.coverage_items)
    assert all(item.preview_only is True for item in report.coverage_items)
    assert all(item.external_solver_executed is False for item in report.coverage_items)
