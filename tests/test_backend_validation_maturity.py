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
        "gmsh_optional_solver_micro_benchmark",
        "meep_optional_solver_micro_benchmark",
        "mpb_optional_solver_micro_benchmark",
        "optiland_optional_solver_micro_benchmark",
        "elmer_optional_solver_micro_benchmark",
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
    optional_solver_records = [
        record for record in records if record.area == "optional_solver_micro_benchmarks"
    ]
    assert len(optional_solver_records) == 5
    assert all(record.external_solver_required is True for record in optional_solver_records)
    assert all(
        record.external_solver_executed_by_default is False
        for record in optional_solver_records
    )
    assert (
        next(
            record
            for record in optional_solver_records
            if record.component_id == "elmer_optional_solver_micro_benchmark"
        ).maturity_level
        == "documented_preview"
    )


def test_backend_validation_maturity_summary_has_preview_boundaries():
    summary = build_backend_validation_maturity_summary()
    assert summary.summary["calculator_maturity_level"] == "sanity_checked_preview"
    assert summary.summary["application_domain_maturity_level"] == "benchmark_checked_preview"
    assert summary.summary["adapter_source_monitor_maturity_level"] == "fixture_guarded_preview"
    assert summary.summary["material_maturity_level"] == "documented_preview_user_must_verify"
    assert summary.summary["optional_solver_micro_benchmark_default"] == "no_solver_execution"
    assert summary.summary["optional_solver_micro_benchmarks_opt_in_required"] is True
    assert summary.summary["optional_solver_readiness_available"] is True
    assert summary.summary["optional_solver_approval_matrix_available"] is True
    assert summary.summary["optional_solver_environment_profiles_available"] is True
    assert summary.summary["optional_solver_execution_approval_packet_available"] is True
    assert summary.summary["optional_solver_evidence_summary_available"] is True
    assert summary.summary["rc8_backend_readiness_review_available"] is True
    assert summary.summary["solver_evidence_validation_maturity_mapping_available"] is True
    assert summary.summary["optional_solver_approval_records_present"] is True
    assert summary.summary["solver_evidence_closed_for"] == ["gmsh", "optiland", "meep", "mpb"]
    assert summary.summary["solver_evidence_deferred_for"] == ["elmer"]
    assert summary.summary["optional_solver_evidence_review_complete"] is True
    assert summary.summary["optional_solver_execution_default"] is False
    assert summary.summary["explicit_solver_approval_required"] is True
    assert summary.summary["all_optional_solver_execution_authorized"] is False
    assert summary.summary["gmsh_optional_micro_benchmark_status"] == "passed_2026-05-20"
    assert (
        summary.summary["gmsh_optional_micro_benchmark_review_status"]
        == "accepted_as_optional_manual_mesh_generation_smoke_evidence"
    )
    assert summary.summary["optiland_optional_micro_benchmark_status"] == "passed_2026-05-20"
    assert (
        summary.summary["optiland_optional_micro_benchmark_review_status"]
        == "accepted_as_optional_manual_ray_path_smoke_evidence"
    )
    assert summary.summary["meep_optional_micro_benchmark_decision_packet_available"] is True
    assert summary.summary["meep_optional_micro_benchmark_status"] == "passed_2026-05-20"
    assert (
        summary.summary["meep_optional_micro_benchmark_review_status"]
        == "accepted_as_optional_manual_pymeep_fdtd_smoke_evidence"
    )
    assert (
        summary.summary["meep_optional_micro_benchmark_readiness_profile"]
        == "osa-solvers_import_only"
    )
    assert summary.summary["mpb_optional_micro_benchmark_decision_packet_available"] is True
    assert summary.summary["mpb_optional_micro_benchmark_status"] == "passed_2026-05-20"
    assert (
        summary.summary["mpb_optional_micro_benchmark_review_status"]
        == "accepted_as_optional_manual_mpb_band_structure_smoke_evidence"
    )
    assert (
        summary.summary["mpb_optional_micro_benchmark_readiness_profile"]
        == "osa-solvers_import_only_meep_mpb"
    )
    assert (
        summary.summary["next_optional_solver_candidate"]
        == "none_elmer_deferred"
    )
    assert summary.summary["elmer_micro_benchmark_status"] == "deferred"
    assert "not a production-grade optical constants database" in summary.preview_boundary_summary["materials"]
    assert "not physical correctness" in summary.preview_boundary_summary["application_domains"]
    assert "explicit opt-in" in summary.preview_boundary_summary["optional_solver_micro_benchmarks"]
    assert "availability" in summary.preview_boundary_summary["optional_solver_micro_benchmarks"]
    assert "OSA_SOLVER_PYTHON" in summary.preview_boundary_summary["optional_solver_micro_benchmarks"]
    assert "one-solver-at-a-time" in summary.preview_boundary_summary["optional_solver_micro_benchmarks"]
    assert "reviewed ray/path smoke evidence" in summary.preview_boundary_summary["optional_solver_micro_benchmarks"]
    assert "Meep-only pass" in summary.preview_boundary_summary["optional_solver_micro_benchmarks"]
    assert "reviewed optional manual PyMeep/FDTD smoke evidence" in summary.preview_boundary_summary["optional_solver_micro_benchmarks"]
    assert "PyMeep/FDTD smoke evidence" in summary.preview_boundary_summary["optional_solver_micro_benchmarks"]
    assert "MPB/band-structure smoke evidence" in summary.preview_boundary_summary[
        "optional_solver_micro_benchmarks"
    ]
    assert "reviewed optional manual MPB/band-structure" in summary.preview_boundary_summary[
        "optional_solver_micro_benchmarks"
    ]
    assert "close the optional solver evidence review loops" in summary.preview_boundary_summary[
        "optional_solver_micro_benchmarks"
    ]
    assert "Elmer deferred and not Level 3" in summary.preview_boundary_summary[
        "optional_solver_micro_benchmarks"
    ]
    assert summary.production_grade_validation_claimed is False
    assert summary.formal_convergence_proof_claimed is False
