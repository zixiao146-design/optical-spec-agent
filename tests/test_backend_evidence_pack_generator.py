"""Maintainer backend evidence pack generator tests."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_backend_evidence_pack_generator_writes_json_and_markdown(tmp_path):
    json_out = tmp_path / "evidence-pack.json"
    markdown_out = tmp_path / "evidence-pack.md"
    result = subprocess.run(
        [
            sys.executable,
            "scripts/generate_backend_evidence_pack.py",
            "--json-out",
            str(json_out),
            "--markdown-out",
            str(markdown_out),
        ],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=180,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    payload = json.loads(json_out.read_text(encoding="utf-8"))
    for section in [
        "package_and_release_status",
        "sub_agent_reality",
        "tool_call_reality",
        "optical_calculators",
        "material_provenance_coverage",
        "ambiguous_requirement_matching",
        "missing_input_diagnostics",
        "application_domain_coverage",
        "material_template_cross_checks",
        "application_domain_benchmarks",
        "design_case_cross_checks",
        "source_monitor_observable_diagnostics",
        "adapter_native_golden_coverage",
        "validation_maturity_summary",
        "preview_boundary_summary",
        "optional_solver_micro_benchmarks",
        "blocked_or_deferred_capabilities",
        "maintainer_review_questions",
    ]:
        assert section in payload
    assert payload["external_solver_executed"] is False
    assert payload["external_llm_required"] is False
    assert payload["production_grade_validation_claimed"] is False
    assert payload["formal_convergence_proof_claimed"] is False
    assert all(
        item["executed"] is False
        for item in payload["blocked_or_deferred_capabilities"]
    )
    assert payload["material_provenance_coverage"]["production_grade_optical_constants_database"] is False
    assert payload["ambiguous_requirement_matching"]["ambiguous_goals_generate_questions"] is True
    assert payload["missing_input_diagnostics"]["safe_to_run_solver_default"] is False
    assert payload["application_domain_coverage"]["domain_count"] == 10
    assert payload["application_domain_coverage"]["failed_domains"] == []
    assert payload["material_template_cross_checks"]["total"] == 10
    assert payload["material_template_cross_checks"]["fail_count"] == 0
    assert payload["application_domain_benchmarks"]["scenario_count"] >= 19
    assert payload["application_domain_benchmarks"]["fail_count"] == 0
    assert payload["application_domain_benchmarks"]["warn_count"] == 0
    assert payload["validation_maturity_summary"]["summary"]["record_count"] >= 17
    assert (
        payload["validation_maturity_summary"]["summary"]["calculator_maturity_level"]
        == "sanity_checked_preview"
    )
    assert payload["validation_claim_audit_available"] is True
    assert "materials" in payload["preview_boundary_summary"]
    solver_micro = payload["optional_solver_micro_benchmarks"]
    assert solver_micro["manifest_exists"] is True
    assert solver_micro["readiness_available"] is True
    assert solver_micro["approval_matrix_available"] is True
    assert solver_micro["execution_approval_packet_available"] is True
    assert solver_micro["approval_records_present"] is True
    assert solver_micro["environment_profiles_available"] is True
    assert solver_micro["optional_solver_environment_profiles_available"] is True
    assert solver_micro["solver_python_env_var"] == "OSA_SOLVER_PYTHON"
    assert solver_micro["profile_env_var"] == "OSA_SOLVER_READINESS_PROFILE"
    assert solver_micro["default_runs_solver"] is False
    assert solver_micro["execution_default"] is False
    assert solver_micro["explicit_approval_required"] is True
    assert solver_micro["optional_solver_readiness_available"] is True
    assert solver_micro["optional_solver_approval_matrix_available"] is True
    assert solver_micro["optional_solver_execution_approval_packet_available"] is True
    assert solver_micro["optional_solver_approval_records_present"] is True
    assert solver_micro["meep_decision_packet_available"] is True
    assert (
        solver_micro["meep_decision_packet_path"]
        == "docs/optional_solver_approval_records/meep_micro_benchmark_decision_packet.md"
    )
    assert solver_micro["mpb_decision_packet_available"] is True
    assert (
        solver_micro["mpb_decision_packet_path"]
        == "docs/optional_solver_approval_records/mpb_micro_benchmark_decision_packet.md"
    )
    assert solver_micro["optional_solver_execution_default"] is False
    assert solver_micro["manual_opt_in_only"] is True
    assert solver_micro["all_optional_solver_execution_authorized"] is False
    assert solver_micro["no_production_grade_claim"] is True
    assert len(solver_micro["solvers"]) == 5
    gmsh = next(item for item in solver_micro["solvers"] if item["solver_name"] == "gmsh")
    assert gmsh["approval_status"] == "approved_executed"
    assert gmsh["last_execution_status"] == "passed"
    assert gmsh["last_execution_evidence"] == (
        "validation/gmsh/gmsh_micro_benchmark_2026-05-20.md"
    )
    assert gmsh["review_record_path"].endswith(
        "gmsh_micro_benchmark_review_2026-05-20.md"
    )
    assert gmsh["next_candidate_solver"] == "mpb_after_osa_solver_python"
    assert gmsh["next_candidate_approved"] is False
    optiland = next(item for item in solver_micro["solvers"] if item["solver_name"] == "optiland")
    assert optiland["approval_status"] == "approved_executed"
    assert optiland["last_execution_status"] == "passed"
    assert optiland["last_execution_evidence"] == (
        "validation/optiland/optiland_micro_benchmark_2026-05-20.md"
    )
    assert optiland["review_record_path"].endswith(
        "optiland_micro_benchmark_review_2026-05-20.md"
    )
    assert (
        optiland["review_status"]
        == "accepted_as_optional_manual_ray_path_smoke_evidence"
    )
    meep = next(item for item in solver_micro["solvers"] if item["solver_name"] == "meep")
    assert meep["approval_status"] == "approved_executed"
    assert meep["execution_authorized"] is False
    assert meep["last_execution_status"] == "passed"
    assert meep["last_execution_evidence"] == (
        "validation/meep/meep_micro_benchmark_2026-05-20.md"
    )
    assert meep["decision_packet_path"].endswith(
        "meep_micro_benchmark_decision_packet.md"
    )
    assert meep["review_record_path"].endswith(
        "meep_micro_benchmark_review_2026-05-20.md"
    )
    assert (
        meep["review_status"]
        == "accepted_as_optional_manual_pymeep_fdtd_smoke_evidence"
    )
    mpb = next(item for item in solver_micro["solvers"] if item["solver_name"] == "mpb")
    assert mpb["approval_status"] == "pending"
    assert mpb["execution_authorized"] is False
    assert mpb["last_execution_status"] == "not_run"
    assert mpb["decision_packet_path"].endswith(
        "mpb_micro_benchmark_decision_packet.md"
    )
    assert mpb["cli_required"] is False
    assert any(
        "Optiland evidence was reviewed and accepted" in note
        for note in solver_micro["notes"]
    )
    assert any(
        "Meep evidence was reviewed and accepted" in note
        for note in solver_micro["notes"]
    )
    assert any("MPB has a prepared decision packet" in note for note in solver_micro["notes"])
    assert solver_micro["elmer_deferred"] is True
    assert {item["calculator_name"] for item in payload["optical_calculators"]} == {
        "thin_film",
        "paraxial",
        "gaussian_beam",
        "waveguide",
        "fiber_coupling",
        "polarization",
    }
    calculators = {
        item["calculator_name"]: item for item in payload["optical_calculators"]
    }
    assert (
        "fiber_gaussian_offset_loss"
        in calculators["fiber_coupling"]["sanity_reference_cases"]
    )
    assert (
        "jones_quarter_waveplate_phase_preview"
        in calculators["polarization"]["sanity_reference_cases"]
    )
    markdown = markdown_out.read_text(encoding="utf-8")
    for heading in [
        "Sub-agent reality",
        "Tool-call reality",
        "Optical calculators",
        "Material provenance coverage",
        "Ambiguous requirement matching",
        "Missing-input diagnostics",
        "Application-domain coverage",
        "Material-template cross-checks",
        "Application-domain benchmarks",
        "Validation maturity summary",
        "Preview boundary summary",
        "Optional solver micro-benchmarks",
        "Design-case cross-checks",
        "Adapter-native golden coverage",
        "Blocked or deferred capabilities",
    ]:
        assert heading in markdown
    assert "production-grade physical validation" in markdown
    assert "NO SOLVER EXECUTION PERFORMED" in result.stdout
    assert "NO EXTERNAL LLM CALLED" in result.stdout
    assert "NO UPLOAD PERFORMED" in result.stdout
    assert "NO TAG CREATED" in result.stdout
    assert "NO RELEASE CREATED" in result.stdout
