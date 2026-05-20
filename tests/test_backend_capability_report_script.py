"""Backend capability report script tests."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_backend_capability_report_script_generates_json_and_markdown(tmp_path: Path):
    json_out = tmp_path / "report.json"
    markdown_out = tmp_path / "report.md"
    result = subprocess.run(
        [
            sys.executable,
            "scripts/generate_backend_capability_report.py",
            "--json-out",
            str(json_out),
            "--markdown-out",
            str(markdown_out),
        ],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=120,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "NO SOLVER EXECUTION PERFORMED" in result.stdout
    assert "NO EXTERNAL LLM CALLED" in result.stdout
    assert json_out.exists()
    assert markdown_out.exists()
    report = json.loads(json_out.read_text(encoding="utf-8"))
    for section in [
        "package",
        "sub_agents",
        "internal_tools",
        "optical_calculators",
        "requirements_templates",
        "material_provenance_coverage",
        "ambiguous_requirement_matching",
        "missing_input_diagnostics",
        "application_domain_coverage",
        "material_template_cross_checks",
        "application_domain_benchmarks",
        "validation_maturity_summary",
        "preview_boundary_summary",
        "optional_solver_micro_benchmarks",
        "adapter_native_golden_coverage",
        "design_case_cross_checks",
        "blocked_external_actions",
    ]:
        assert section in report
    assert report["evidence_pack_available"] is True
    assert "Adapter-native golden coverage" in report["evidence_pack_sections"]
    assert report["package"]["package_version"] == "0.9.0rc8.dev0"
    assert report["production_grade_validation_claimed"] is False
    assert report["formal_convergence_proof_claimed"] is False
    assert len(report["requirements_templates"]) == 7
    tools = {item["tool_name"]: item for item in report["internal_tools"]}
    assert tools["material_suitability_diagnostics"]["callable"] is True
    assert tools["ambiguous_requirement_matching"]["executed_in_sample"] is True
    assert tools["application_domain_registry"]["executed_in_sample"] is True
    assert tools["material_template_cross_checks"]["executed_in_sample"] is True
    assert tools["application_domain_benchmarks"]["executed_in_sample"] is True
    assert tools["source_monitor_inference"]["executed_in_sample"] is True
    assert tools["missing_input_diagnostics"]["executed_in_sample"] is True
    assert tools["observable_diagnostics"]["executed_in_sample"] is True
    assert tools["adapter_native_mapping"]["executed_in_sample"] is True
    assert tools["adapter_native_golden_coverage"]["executed_in_sample"] is True
    assert tools["validation_maturity_summary"]["executed_in_sample"] is True
    assert report["adapter_native_golden_coverage"]["status"] == "ok"
    assert set(report["adapter_native_golden_coverage"]["adapters_covered"]) == {
        "meep",
        "mpb",
        "gmsh",
        "elmer",
        "optiland",
    }
    assert report["adapter_native_golden_coverage"]["missing_adapters"] == []
    assert report["material_provenance_coverage"]["production_grade_optical_constants_claimed"] is False
    assert report["ambiguous_requirement_matching"]["no_external_llm_used"] is True
    assert report["missing_input_diagnostics"]["safe_to_run_solver_default"] is False
    assert report["application_domain_coverage"]["domain_count"] == 10
    assert report["application_domain_coverage"]["failed_domains"] == []
    assert report["material_template_cross_checks"]["total"] == 10
    assert report["material_template_cross_checks"]["fail_count"] == 0
    assert report["application_domain_benchmarks"]["scenario_count"] >= 19
    assert report["application_domain_benchmarks"]["fail_count"] == 0
    assert report["application_domain_benchmarks"]["warn_count"] == 0
    assert report["application_domain_benchmarks"]["unsupported_count"] >= 3
    assert report["validation_maturity_summary"]["summary"]["record_count"] >= 17
    assert (
        report["validation_maturity_summary"]["summary"]["calculator_maturity_level"]
        == "sanity_checked_preview"
    )
    assert report["validation_claim_audit_available"] is True
    assert "adapters" in report["preview_boundary_summary"]
    solver_micro = report["optional_solver_micro_benchmarks"]
    assert solver_micro["manifest_exists"] is True
    assert solver_micro["readiness_available"] is True
    assert solver_micro["approval_matrix_available"] is True
    assert solver_micro["execution_approval_packet_available"] is True
    assert solver_micro["approval_records_present"] is True
    assert solver_micro["environment_profiles_available"] is True
    assert solver_micro["environment_profiles_path"] == "validation/solver_environment_profiles.json"
    assert (
        solver_micro["execution_approval_packet_path"]
        == "docs/optional_solver_micro_benchmark_execution_packet.md"
    )
    assert solver_micro["approval_records_path"] == "docs/optional_solver_approval_records"
    assert solver_micro["solver_python_env_var"] == "OSA_SOLVER_PYTHON"
    assert solver_micro["profile_env_var"] == "OSA_SOLVER_READINESS_PROFILE"
    assert solver_micro["default_runs_solver"] is False
    assert solver_micro["execution_default"] is False
    assert solver_micro["opt_in_required"] is True
    assert solver_micro["explicit_approval_required"] is True
    assert solver_micro["all_optional_solver_execution_authorized"] is False
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
    assert (
        gmsh["review_status"]
        == "accepted_as_optional_manual_mesh_generation_smoke_evidence"
    )
    assert gmsh["next_candidate_solver"] == "meep_or_mpb_after_osa_solver_python"
    assert gmsh["next_candidate_approved"] is False
    assert gmsh["no_further_solver_authorized"] is True
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
    assert any(
        "Optiland evidence was reviewed and accepted" in note
        for note in solver_micro["notes"]
    )
    assert solver_micro["elmer_deferred"] is True
    assert solver_micro["production_grade_claim"] is False
    assert solver_micro["formal_convergence_proof_claimed"] is False
    assert {item["calculator_name"] for item in report["optical_calculators"]} == {
        "thin_film",
        "paraxial",
        "gaussian_beam",
        "waveguide",
        "fiber_coupling",
        "polarization",
    }
    calculators = {item["calculator_name"]: item for item in report["optical_calculators"]}
    assert "fiber_gaussian_offset_loss" in calculators["fiber_coupling"]["reference_cases"]
    assert "fiber_gaussian_tilt_loss" in calculators["fiber_coupling"]["reference_cases"]
    assert "jones_linear_polarizer_malus" in calculators["polarization"]["reference_cases"]
    assert (
        "jones_quarter_waveplate_phase_preview"
        in calculators["polarization"]["reference_cases"]
    )
    assert all(item["matched_by_heuristic"] for item in report["requirements_templates"])
    assert all(action["executed"] is False for action in report["blocked_external_actions"])
    text = markdown_out.read_text(encoding="utf-8")
    assert "Backend Capability Report" in text
    assert "Adapter-Native Golden Coverage" in text
    assert "Validation Maturity Summary" in text
    assert "Preview Boundary Summary" in text
    assert "Optional Solver Micro-benchmarks" in text
    assert "readiness_available" in text
    assert "explicit_approval_required" in text
    assert "Maintainer Evidence Pack" in text
    assert "NO UPLOAD PERFORMED" in text


def test_backend_capability_report_script_does_not_contain_release_commands():
    text = (ROOT / "scripts" / "generate_backend_capability_report.py").read_text(
        encoding="utf-8"
    )
    forbidden = ["twine upload", "gh release create", "git tag", "TESTPYPI_TOKEN", "PYPI_TOKEN"]
    for phrase in forbidden:
        assert phrase not in text
