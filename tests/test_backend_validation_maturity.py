"""Backend validation maturity model tests."""

from __future__ import annotations

from optical_spec_agent.validation_maturity import (
    build_backend_validation_maturity_records,
    build_backend_validation_maturity_summary,
)


def test_backend_validation_maturity_records_cover_expected_areas():
    records = build_backend_validation_maturity_records()
    by_component = {record.component_id: record for record in records}
    for component_id in [
        "material_library",
        "design_requirement_templates",
        "application_domain_benchmarks",
        "thin_film_calculator",
        "paraxial_calculator",
        "gaussian_beam_calculator",
        "waveguide_calculator",
        "fiber_coupling_calculator",
        "polarization_calculator",
        "source_monitor_diagnostics",
        "observable_diagnostics",
        "adapter_native_mapping",
        "adapter_golden_coverage",
        "sub_agent_task_sessions",
        "tool_call_ledger",
        "agent_studio",
    ]:
        assert component_id in by_component


def test_backend_validation_maturity_levels_are_conservative():
    records = build_backend_validation_maturity_records()
    calculators = [
        record
        for record in records
        if record.area == "calculators"
    ]
    assert len(calculators) == 6
    assert all(record.maturity_level == "sanity_checked_preview" for record in calculators)
    assert (
        next(record for record in records if record.component_id == "application_domain_benchmarks")
        .maturity_level
        == "benchmark_checked_preview"
    )
    material = next(record for record in records if record.component_id == "material_library")
    assert material.maturity_level == "documented_preview"
    assert any("User must verify" in item for item in material.limitations)
    assert all(
        record.production_grade_physical_validation_claimed is False
        for record in records
    )
    assert all(record.formal_convergence_proof_claimed is False for record in records)
    assert all(record.external_solver_executed_by_default is False for record in records)


def test_backend_validation_maturity_summary_has_preview_boundaries():
    summary = build_backend_validation_maturity_summary()
    assert summary.summary["calculator_maturity_level"] == "sanity_checked_preview"
    assert summary.summary["application_domain_maturity_level"] == "benchmark_checked_preview"
    assert summary.summary["adapter_source_monitor_maturity_level"] == "fixture_guarded_preview"
    assert summary.summary["material_maturity_level"] == "documented_preview_user_must_verify"
    assert "not a production-grade optical constants database" in summary.preview_boundary_summary["materials"]
    assert "not physical correctness" in summary.preview_boundary_summary["application_domains"]
    assert summary.production_grade_validation_claimed is False
    assert summary.formal_convergence_proof_claimed is False

