"""Release-engineering script and contract tests."""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tomllib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _load_docs_check_module():
    path = ROOT / "scripts" / "check_docs_consistency.py"
    spec = importlib.util.spec_from_file_location("check_docs_consistency_for_tests", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _run(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, *args],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=180,
        check=False,
    )


def _write_minimal_release_repo(root: Path, *, version: str, readme: str) -> None:
    (root / "docs").mkdir(parents=True)
    (root / "tests").mkdir()
    (root / "benchmarks").mkdir()
    (root / ".github" / "workflows").mkdir(parents=True)
    (root / "src" / "optical_spec_agent" / "cli").mkdir(parents=True)
    (root / "pyproject.toml").write_text(
        f"""
[project]
name = "optical-spec-agent"
version = "{version}"
requires-python = ">=3.11"
dependencies = []

[project.optional-dependencies]
dev = ["pytest>=8.0", "build>=1.2", "twine>=5.0"]
""".strip(),
        encoding="utf-8",
    )
    (root / "README.md").write_text(readme, encoding="utf-8")
    (root / "Makefile").write_text("check:\n\tpytest -q\n", encoding="utf-8")
    (root / ".github" / "workflows" / "ci.yml").write_text(
        "steps:\n  - run: pytest -q\n  - run: python benchmarks/run_benchmark.py --mode key_fields\n",
        encoding="utf-8",
    )
    (root / "src" / "optical_spec_agent" / "cli" / "main.py").write_text("", encoding="utf-8")
    for name in [
        "versioning_policy.md",
        "release_readiness_current.md",
        "release_notes_current.md",
        "release_decision_matrix.md",
        "release_blockers_current.md",
        "version_bump_plan_0.9.0rc1.md",
        "artifact_contracts.md",
        "security_and_robustness.md",
        "api_contract.md",
        "cli_contract.md",
        "benchmark_contract.md",
    ]:
        (root / "docs" / name).write_text("Draft preview documentation.\n", encoding="utf-8")


def test_cli_surface_check_runs():
    result = _run(["scripts/check_cli_surface.py", "--json"])
    assert result.returncode == 0, result.stdout + result.stderr
    report = json.loads(result.stdout)
    assert report["schema_version"] == "cli_surface_check.v0.1"
    assert report["errors"] == []


def test_docs_consistency_check_runs():
    result = _run(["scripts/check_docs_consistency.py", "--json"])
    assert result.returncode == 0, result.stdout + result.stderr
    report = json.loads(result.stdout)
    assert report["schema_version"] == "docs_consistency_check.v0.1"
    assert report["errors"] == []


def test_validation_boundary_docs_keep_non_overclaiming_contract():
    text = (ROOT / "docs" / "validation_boundary.md").read_text(encoding="utf-8")
    required = [
        "No production-grade physical validation",
        "No formal convergence proof",
        "External solver validation is optional/manual",
        "do not require Meep, MPB, Gmsh, Elmer, Optiland, or external LLM providers",
    ]
    for phrase in required:
        assert phrase in text


def test_pypi_publication_decision_requires_explicit_approval():
    text = (ROOT / "docs" / "pypi_publication_decision.md").read_text(encoding="utf-8")
    assert "PyPI published: no" in text
    assert "Do not publish automatically" in text
    assert "explicit maintainer approval" in text


def test_validation_and_packaging_gate_docs_exist_and_bound_claims():
    required_docs = [
        "packaging_gate.md",
        "validation_gate.md",
        "external_solver_policy.md",
        "external_llm_policy.md",
        "pypi_publication_decision.md",
        "pypi_publication_readiness_checklist.md",
        "pypi_post_publication_verification_plan.md",
        "rc9_v1_0_readiness_gap_audit.md",
        "rc9_backend_stabilization_plan.md",
        "rc9_pypi_publication_decision_review.md",
        "rc9_go_no_go_matrix.md",
        "rc9_release_strategy.md",
        "validation_boundary.md",
        "release_engineering_playbook.md",
        "adapter_support_matrix.md",
        "testpypi_dry_run_gate.md",
        "v1_0_stability_gate.md",
        "schema_compatibility_policy.md",
        "open_source_solver_strategy.md",
        "proprietary_solver_policy.md",
        "v1_0_compatibility_policy.md",
        "validation_evidence_manifest.md",
        "open_source_solver_validation_plan.md",
        "open_solver_validation_harness.md",
        "solver_validation_micro_benchmarks.md",
        "solver_validation_micro_benchmarks.zh-CN.md",
        "optional_solver_evidence_summary.md",
        "optional_solver_evidence_summary.zh-CN.md",
        "rc8_backend_readiness_review.md",
        "rc8_backend_readiness_review.zh-CN.md",
        "solver_evidence_validation_maturity_mapping.md",
        "solver_evidence_validation_maturity_mapping.zh-CN.md",
        "optional_solver_micro_benchmark_approval_matrix.md",
        "optional_solver_micro_benchmark_approval_matrix.zh-CN.md",
        "optional_solver_micro_benchmark_approval_record_template.md",
        "optional_solver_micro_benchmark_approval_record_template.zh-CN.md",
        "optional_solver_micro_benchmark_execution_packet.md",
        "optional_solver_micro_benchmark_execution_packet.zh-CN.md",
        "optional_solver_execution_sequence.md",
        "optional_solver_execution_sequence.zh-CN.md",
        "optional_solver_micro_benchmark_readiness_status.md",
        "optional_solver_approval_records/gmsh_micro_benchmark_review_2026-05-20.md",
        "optional_solver_approval_records/optiland_micro_benchmark_review_2026-05-20.md",
        "optional_solver_approval_records/meep_micro_benchmark_decision_packet.md",
        "optional_solver_approval_records/meep_micro_benchmark_approval_2026-05-20.md",
        "optional_solver_approval_records/meep_micro_benchmark_review_2026-05-20.md",
        "optional_solver_approval_records/mpb_micro_benchmark_decision_packet.md",
        "optional_solver_approval_records/mpb_micro_benchmark_approval_2026-05-20.md",
        "optional_solver_approval_records/mpb_micro_benchmark_review_2026-05-20.md",
        "optional_solver_environment_profiles.md",
        "optional_solver_environment_profiles.zh-CN.md",
        "adapter_maturity_model.md",
        "gmsh_optional_validation_pilot.md",
        "gmsh_level3_readiness.md",
        "meep_optional_validation_pilot.md",
        "meep_level3_readiness.md",
        "mpb_optional_validation_pilot.md",
        "mpb_level3_readiness.md",
        "optiland_optional_validation_pilot.md",
        "optiland_level3_readiness.md",
        "elmer_optional_validation_pilot.md",
        "elmer_level3_readiness.md",
        "manual_solver_validation_report_template.md",
        "manual_solver_validation_reports/solver_micro_benchmark_report_schema.json",
        "manual_solver_validation_reports/gmsh_validation_pilot_template.md",
        "manual_solver_validation_reports/meep_validation_report_schema.json",
        "manual_solver_validation_reports/mpb_validation_report_schema.json",
        "manual_solver_validation_reports/optiland_validation_report_schema.json",
        "manual_solver_validation_reports/elmer_validation_report_schema.json",
        "pytest_marker_policy.md",
        "testpypi_upload_approval_v0.9.0rc7.md",
        "testpypi_upload_approval_v0.9.0rc6.dev0.md",
        "testpypi_upload_approval_v0.9.0rc6.md",
        "testpypi_upload_attempt_v0.9.0rc6.dev0.md",
        "testpypi_status_v0.9.0rc6.dev0.md",
        "testpypi_trusted_publishing.md",
        "release_readiness_v0.9.0rc7.md",
        "release_readiness_v0.9.0rc6.md",
        "github_release_draft_v0.9.0rc6.md",
        "release_notes_v0.9.0rc6.md",
        "v1_0_gap_audit.md",
        "rc6_development_plan.md",
        "v1_0_decision_matrix.md",
        "v1_0_public_contract_freeze_checklist.md",
        "v1_0_public_contract_freeze_confirmation.md",
        "v1_0_public_contract_freeze_status.md",
        "v1_0_contract_frozen_surface.md",
        "v1_0_contract_non_goals.md",
        "v1_0_breaking_change_policy.md",
        "v1_0_release_criteria.md",
        "v1_0_release_plan.md",
        "rc_to_v1_0_transition_path.md",
        "v1_0_pypi_decision_gate.md",
        "v1_0_post_release_verification_plan.md",
        "agent_studio_frontend_roadmap.md",
        "api_agent_contract.md",
        "api_error_model.md",
        "api_versioning_policy.md",
        "api_request_validation_contract.md",
        "api_migration_notes.md",
        "api_local_launch_guide.md",
        "frontend_handoff_spec.md",
        "api_curl_examples.md",
        "frontend_mvp_product_spec.md",
        "frontend_information_architecture.md",
        "frontend_api_mapping.md",
        "frontend_mvp_user_flows.md",
        "frontend_mvp_acceptance_criteria.md",
        "frontend_safety_policy.md",
        "frontend_mvp_implementation_plan.md",
        "frontend_mvp_runbook.md",
        "frontend_mvp_qa_checklist.md",
        "frontend_visual_smoke_plan.md",
        "frontend_visual_smoke_runbook.md",
        "agent_studio_demo_runbook.md",
        "agent_studio_demo_checklist.md",
        "agent_studio_demo_storyboard.md",
        "agent_studio_demo_troubleshooting.md",
        "agent_studio_demo_feedback.md",
        "frontend_hardening_backlog.md",
        "quickstart.md",
        "quickstart.zh-CN.md",
        "frontend_i18n_zh_CN.md",
        "agent_studio_chinese_guided_tutorial.md",
        "frontend_chinese_terminology.md",
        "example_gallery.md",
        "example_gallery.zh-CN.md",
        "agent_trace_timeline.md",
        "agent_trace_timeline.zh-CN.md",
        "agent_command_center.md",
        "agent_command_center.zh-CN.md",
        "tool_call_reality_matrix.md",
        "backend_functionality_status.md",
        "backend_capability_report.md",
        "backend_capability_report.zh-CN.md",
        "backend_evidence_review_pack.md",
        "backend_evidence_review_pack.zh-CN.md",
        "backend_validation_maturity_matrix.md",
        "backend_validation_maturity_matrix.zh-CN.md",
        "preview_boundary_policy.md",
        "preview_boundary_policy.zh-CN.md",
        "solver_validation_micro_benchmarks.md",
        "solver_validation_micro_benchmarks.zh-CN.md",
        "optional_solver_evidence_summary.md",
        "optional_solver_evidence_summary.zh-CN.md",
        "rc8_backend_readiness_review.md",
        "rc8_backend_readiness_review.zh-CN.md",
        "solver_evidence_validation_maturity_mapping.md",
        "solver_evidence_validation_maturity_mapping.zh-CN.md",
        "optional_solver_micro_benchmark_approval_matrix.md",
        "optional_solver_micro_benchmark_approval_matrix.zh-CN.md",
        "optional_solver_micro_benchmark_approval_record_template.md",
        "optional_solver_micro_benchmark_approval_record_template.zh-CN.md",
        "optional_solver_micro_benchmark_execution_packet.md",
        "optional_solver_micro_benchmark_execution_packet.zh-CN.md",
        "optional_solver_execution_sequence.md",
        "optional_solver_execution_sequence.zh-CN.md",
        "optional_solver_micro_benchmark_readiness_status.md",
        "optional_solver_approval_records/gmsh_micro_benchmark_review_2026-05-20.md",
        "optional_solver_approval_records/optiland_micro_benchmark_review_2026-05-20.md",
        "optional_solver_approval_records/meep_micro_benchmark_decision_packet.md",
        "optional_solver_approval_records/meep_micro_benchmark_approval_2026-05-20.md",
        "optional_solver_approval_records/meep_micro_benchmark_review_2026-05-20.md",
        "optional_solver_approval_records/mpb_micro_benchmark_decision_packet.md",
        "optional_solver_approval_records/mpb_micro_benchmark_approval_2026-05-20.md",
        "optional_solver_approval_records/mpb_micro_benchmark_review_2026-05-20.md",
        "optional_solver_environment_profiles.md",
        "optional_solver_environment_profiles.zh-CN.md",
        "backend_evidence_review_decision.md",
        "rc8_backend_roadmap.md",
        "rc8_capability_gap_audit.md",
        "rc8_to_v1_0_decision_path.md",
        "design_case_cross_checks.md",
        "design_case_cross_checks.zh-CN.md",
        "design_requirement_templates.md",
        "design_requirement_templates.zh-CN.md",
        "natural_language_to_optical_language.md",
        "natural_language_to_optical_language.zh-CN.md",
        "application_domain_benchmarks.md",
        "application_domain_benchmarks.zh-CN.md",
        "domain_benchmark_results_policy.md",
        "domain_benchmark_results_policy.zh-CN.md",
        "optical_language_source_monitor.md",
        "optical_language_source_monitor.zh-CN.md",
        "source_monitor_missing_input_diagnostics.md",
        "source_monitor_missing_input_diagnostics.zh-CN.md",
        "adapter_native_source_monitor_mapping.md",
        "adapter_native_source_monitor_mapping.zh-CN.md",
        "adapter_native_golden_cases.md",
        "adapter_native_golden_cases.zh-CN.md",
        "adapter_native_golden_coverage_matrix.md",
        "adapter_native_golden_coverage_matrix.zh-CN.md",
        "observable_diagnostics.md",
        "observable_diagnostics.zh-CN.md",
        "optical_calculators.md",
        "optical_calculators.zh-CN.md",
        "fiber_coupling_preview_calculator.md",
        "fiber_coupling_preview_calculator.zh-CN.md",
        "polarization_preview_calculator.md",
        "polarization_preview_calculator.zh-CN.md",
        "fiber_polarization_reference_cases.md",
        "fiber_polarization_reference_cases.zh-CN.md",
        "optical_calculator_case_integration.md",
        "optical_calculator_case_integration.zh-CN.md",
        "optical_calculator_reference_cases.md",
        "optical_calculator_reference_cases.zh-CN.md",
        "material_library.md",
        "material_library.zh-CN.md",
        "sub_agent_architecture.md",
        "sub_agent_architecture.zh-CN.md",
        "open_source_optical_design_ecosystem.md",
        "cli_api_parity.md",
        "publication_decision_record.md",
        "release_readiness_v0.9.0rc5.md",
        "github_release_draft_v0.9.0rc5.md",
        "release_notes_v0.9.0rc5.md",
        "quality_gates.md",
        "ci_quality_gate_parity.md",
        "release_dry_run_operations.md",
        "secrets_and_token_hygiene.md",
        "v1_0_readiness_scorecard.md",
        "README.md",
        "maintainer_decision_log.md",
        "maintainer_operations_checklist.md",
        "offline_user_journey.md",
        "error_model.md",
        "migration_notes_pre_v1.md",
        "v1_0_public_contract_freeze.md",
        "public_contract_change_checklist.md",
    ]
    for name in required_docs:
        assert (ROOT / "docs" / name).exists()
    assert (ROOT / "examples" / "README.md").exists()
    assert (ROOT / "examples" / "examples_manifest.json").exists()
    assert (ROOT / "examples" / "e2e" / "README.md").exists()
    assert (ROOT / "examples" / "api" / "README.md").exists()
    assert (ROOT / "examples" / "api" / "frontend_fixture_manifest.json").exists()
    assert (ROOT / "examples" / "quickstart" / "README.md").exists()
    assert (ROOT / "examples" / "quickstart" / "nanoparticle_demo_spec.json").exists()
    assert (ROOT / "examples" / "quickstart" / "quickstart_workflow_request.json").exists()
    assert (ROOT / "examples" / "quickstart" / "zh_nanoparticle_prompt.txt").exists()
    assert (ROOT / "examples" / "quickstart" / "zh_quickstart_notes.md").exists()
    assert (ROOT / "examples" / "optics_reference_cases" / "README.md").exists()
    assert (ROOT / "examples" / "design_requirements" / "thin_film_ar_coating" / "requirement.json").exists()
    assert (ROOT / "examples" / "design_requirements" / "nanoparticle_plasmonics" / "goal_zh.txt").exists()
    assert (
        ROOT / "examples" / "optics_reference_cases" / "thin_film_single_interface_air_glass.json"
    ).exists()
    assert (
        ROOT / "examples" / "optics_reference_cases" / "gaussian_beam_rayleigh_range.json"
    ).exists()
    assert (
        ROOT
        / "examples"
        / "optics_reference_cases"
        / "fiber_coupling"
        / "perfect_gaussian_match.json"
    ).exists()
    assert (
        ROOT
        / "examples"
        / "optics_reference_cases"
        / "polarization"
        / "linear_polarizer_malus.json"
    ).exists()
    assert (ROOT / "examples" / "optical_design" / "nanoparticle_plasmonics" / "spec.json").exists()
    assert (ROOT / "examples" / "optical_design" / "thin_film_coating" / "spec.json").exists()
    assert (ROOT / "examples" / "optical_design" / "waveguide_mode" / "spec.json").exists()
    assert (ROOT / "examples" / "optical_design" / "photonic_crystal_band" / "spec.json").exists()
    assert (ROOT / "examples" / "optical_design" / "dielectric_metasurface_preview" / "spec.json").exists()
    assert (ROOT / "examples" / "optical_design" / "lens_raytrace_preview" / "spec.json").exists()
    assert (ROOT / "scripts" / "smoke_agent_api.sh").exists()
    assert (ROOT / "scripts" / "check_api_fixtures.py").exists()
    assert (ROOT / "scripts" / "smoke_frontend_mvp.sh").exists()
    assert (ROOT / "scripts" / "smoke_frontend_visual.sh").exists()
    assert (ROOT / "scripts" / "generate_backend_capability_report.py").exists()
    assert (ROOT / "scripts" / "smoke_backend_report.sh").exists()
    assert (ROOT / "scripts" / "demo_agent_studio.sh").exists()
    assert (ROOT / "scripts" / "bootstrap_demo_env.sh").exists()
    assert (ROOT / "scripts" / "run_quickstart_demo.sh").exists()
    assert (ROOT / "docs" / "public_contract_manifest.json").exists()
    assert (ROOT / "scripts" / "testpypi_preflight.sh").exists()
    assert (ROOT / "scripts" / "run_quality_gates.sh").exists()
    assert (ROOT / "scripts" / "open_solver_validation_preflight.sh").exists()
    assert (ROOT / "scripts" / "check_optional_solver_readiness.py").exists()
    assert (ROOT / "scripts" / "run_optional_solver_micro_benchmarks.sh").exists()
    assert (ROOT / "scripts" / "run_optional_gmsh_validation.sh").exists()
    assert (ROOT / "scripts" / "run_optional_meep_validation.sh").exists()
    assert (ROOT / "scripts" / "run_optional_mpb_validation.sh").exists()
    assert (ROOT / "scripts" / "run_optional_optiland_validation.sh").exists()
    assert (ROOT / "scripts" / "run_optional_elmer_validation.sh").exists()
    assert (
        ROOT / "validation" / "elmer" / "elmer_install_deferred_2026-05-15.md"
    ).exists()

    combined = "\n".join(
        (ROOT / "docs" / name).read_text(encoding="utf-8") for name in required_docs
    )
    assert "PyPI published: no" in combined or "PyPI status: not published" in combined
    assert "TestPyPI upload requires explicit maintainer approval" in combined
    assert "No production-grade physical validation" in combined
    assert "No formal convergence proof" in combined
    assert "External solvers are not run by default" in combined
    assert "External LLM access is not required by default" in combined
    assert "open-source-solver-first" in combined
    assert "not default dependencies" in combined
    assert "No proprietary license is required" in combined
    assert "v1.0 compatibility" in combined
    assert "Validation Evidence Manifest" in combined
    assert "Open-source Solver Validation Plan" in combined
    assert "Open-source Solver Validation Harness" in combined
    assert "Optional Solver-backed Validation Micro-benchmarks" in combined
    assert "Optional Solver Evidence Summary" in combined
    assert "rc8 Backend Readiness Review" in combined
    assert "Solver Evidence Validation Maturity Mapping" in combined
    assert "explicit opt-in" in combined
    assert "meep_micro_benchmark_decision_packet.md" in combined
    assert "meep_micro_benchmark_review_2026-05-20.md" in combined
    assert "OSA_SOLVER_PYTHON" in combined
    assert "Adapter Maturity Model" in combined
    assert "Gmsh Optional Validation Pilot" in combined
    assert "Gmsh Level 3 Readiness" in combined
    assert "Meep Optional Validation Pilot" in combined
    assert "Meep Level-3 Manual Validation Readiness" in combined
    assert "MPB Optional Validation Pilot" in combined
    assert "MPB Level-3 Manual Validation Readiness" in combined
    assert "Optiland Optional Validation Pilot" in combined
    assert "Optiland Level-3 Manual Validation Readiness" in combined
    assert "Elmer Optional Validation Pilot" in combined
    assert "Elmer Level-3 Manual Validation Readiness" in combined
    assert "elmer_install_deferred_2026-05-15.md" in combined
    assert "Manual Solver Validation Report Template" in combined
    assert "Pytest Marker Policy" in combined
    assert "0.9.0rc5" in combined
    assert "v0.9.0rc4" in combined
    assert "Never move existing tags" in combined
    assert "No automatic package publishing" in combined
    assert "scripts/testpypi_preflight.sh" in combined
    assert "TestPyPI upload approval for 0.9.0rc9.dev0: pending" in combined
    assert "Upload command authorized for 0.9.0rc9.dev0: no" in combined
    assert "TestPyPI uploaded: yes" in combined
    assert "TestPyPI clean install verification: passed" in combined
    assert "Local Agent API Contract" in combined
    assert "Local Agent API Error Model" in combined
    assert "Local Agent API Launch Guide" in combined
    assert "Frontend Handoff Spec" in combined
    assert "Local Agent API Curl Examples" in combined
    assert "Agent Studio Frontend MVP Product Spec" in combined
    assert "Agent Studio Frontend Information Architecture" in combined
    assert "Agent Studio Frontend API Mapping" in combined
    assert "Agent Studio Frontend MVP User Flows" in combined
    assert "Agent Studio Frontend MVP Acceptance Criteria" in combined
    assert "Agent Studio Frontend Safety Policy" in combined
    assert "Agent Studio Frontend MVP Implementation Plan" in combined
    assert "Frontend implementation: MVP implemented under `frontend/`" in combined
    assert "Agent Studio Frontend MVP Runbook" in combined
    assert "Agent Studio Frontend MVP QA Checklist" in combined
    assert "Demo fixture mode" in combined
    assert "not live validation" in combined
    assert "React + Vite + TypeScript" in combined
    assert "No PyPI/TestPyPI upload controls in MVP" in combined
    assert "No tag/release controls in MVP" in combined
    assert "CLI / API Parity" in combined
    assert "examples/api/" in combined
    assert "scripts/smoke_agent_api.sh" in combined
    assert "scripts/check_api_fixtures.py" in combined
    assert "scripts/smoke_frontend_mvp.sh" in combined
    assert "scripts/smoke_frontend_visual.sh" in combined
    assert "Backend Capability Report" in combined
    assert "Design Case Cross-Checks" in combined
    assert "scripts/smoke_backend_report.sh" in combined
    assert "Frontend Visual Smoke Runbook" in combined
    assert "Playwright visual smoke" in combined
    assert "Agent Studio Demo Runbook" in combined
    assert "Agent Studio Demo Checklist" in combined
    assert "Agent Studio Demo Storyboard" in combined
    assert "Agent Studio Demo Troubleshooting" in combined
    assert "Agent Studio Demo Feedback" in combined
    assert "Frontend Hardening Backlog" in combined
    assert "Quickstart" in combined
    assert "scripts/bootstrap_demo_env.sh" in combined
    assert "scripts/run_quickstart_demo.sh" in combined
    assert "examples/quickstart/" in combined
    assert "scripts/demo_agent_studio.sh" in combined
    assert "No external solver execution by default" in combined
    assert "No external LLM call by default" in combined
    assert "docs/testpypi_status_v0.9.0rc6.dev0.md" in combined
    assert "PyPI publication approval: not granted" in combined
    assert "NO UPLOAD PERFORMED" in combined
    assert "Offline User Journey" in combined
    assert "Error Model" in combined
    assert "Pre-v1 Migration Notes" in combined
    assert "v1.0 Public Contract Freeze" in combined
    assert "Public Contract Change Checklist" in combined
    assert "Quality Gates" in combined
    assert "CI and Quality Gate Parity" in combined
    assert "Release Dry-run Operations" in combined
    assert "Secrets and Token Hygiene" in combined
    assert "Maintainer Operations Checklist" in combined
    assert "v1.0 Readiness Scorecard" in combined
    assert "v1.0 Readiness Gap Audit" in combined
    assert "v0.9.0rc6 Development Plan" in combined
    assert "v1.0 Decision Matrix" in combined
    assert "v1.0 Public Contract Freeze Checklist" in combined
    assert "v1.0 Public Contract Freeze Confirmation" in combined
    assert "v1.0 Public Contract Freeze Status" in combined
    assert "v1.0 Contract Frozen Surface" in combined
    assert "v1.0 Contract Non-goals" in combined
    assert "v1.0 Breaking Change Policy" in combined
    assert "v1.0.0 Release Criteria" in combined
    assert "v1.0.0 Release Plan" in combined
    assert "RC to v1.0.0 Transition Path" in combined
    assert "v1.0 PyPI Decision Gate" in combined
    assert "v1.0.0 Post-release Verification Plan" in combined
    assert "Agent Studio Frontend Roadmap" in combined
    assert "not a v1.0.0 release blocker" in combined
    assert "Maintainer confirmation: approved" in combined
    assert "Publication Decision Record" in combined
    assert "PyPI Publication Readiness Checklist" in combined
    assert "PyPI Post-publication Verification Plan" in combined
    assert "Do not publish PyPI yet" in combined
    assert "PyPI publication does not imply production-grade physical validation" in combined
    assert "Maintainer Decision Log" in combined
    assert "no proprietary" in combined.lower()
    assert "Never paste tokens into chat" in combined
    assert "no GitHub release creation" in combined
    assert "NO SOLVER EXECUTION PERFORMED" in (
        ROOT / "scripts" / "open_solver_validation_preflight.sh"
    ).read_text(encoding="utf-8")
    optional_micro_script = (
        ROOT / "scripts" / "run_optional_solver_micro_benchmarks.sh"
    ).read_text(encoding="utf-8")
    readiness_script = (ROOT / "scripts" / "check_optional_solver_readiness.py").read_text(
        encoding="utf-8"
    )
    assert "SOLVER READINESS CHECK PASSED" in readiness_script
    assert "NO SOLVER EXECUTION PERFORMED" in readiness_script
    assert "NO SOLVER EXECUTION PERFORMED BY DEFAULT" in optional_micro_script
    assert "OSA_RUN_OPTIONAL_GMSH_VALIDATION" in optional_micro_script
    assert "OSA_RUN_OPTIONAL_MEEP_VALIDATION" in optional_micro_script
    assert "OSA_RUN_OPTIONAL_MPB_VALIDATION" in optional_micro_script
    assert "OSA_RUN_OPTIONAL_OPTILAND_VALIDATION" in optional_micro_script
    gmsh_script = (ROOT / "scripts" / "run_optional_gmsh_validation.sh").read_text(
        encoding="utf-8"
    )
    assert "NO GMSH EXECUTION PERFORMED" in gmsh_script
    assert "OPTIONAL VALIDATION NOT ENABLED" in gmsh_script
    assert "NO PRODUCTION-GRADE VALIDATION CLAIMED" in gmsh_script
    assert "level3_achieved" in gmsh_script
    meep_script = (ROOT / "scripts" / "run_optional_meep_validation.sh").read_text(
        encoding="utf-8"
    )
    assert "NO MEEP EXECUTION PERFORMED" in meep_script
    assert "OPTIONAL VALIDATION NOT ENABLED" in meep_script
    assert "NO PRODUCTION-GRADE VALIDATION CLAIMED" in meep_script
    assert "level3_achieved" in meep_script
    mpb_script = (ROOT / "scripts" / "run_optional_mpb_validation.sh").read_text(
        encoding="utf-8"
    )
    assert "NO MPB EXECUTION PERFORMED" in mpb_script
    assert "OPTIONAL VALIDATION NOT ENABLED" in mpb_script
    assert "NO PRODUCTION-GRADE VALIDATION CLAIMED" in mpb_script
    assert "NO MPB CLI REQUIRED" in mpb_script
    assert "level3_achieved" in mpb_script
    optiland_script = (ROOT / "scripts" / "run_optional_optiland_validation.sh").read_text(
        encoding="utf-8"
    )
    assert "NO OPTILAND EXECUTION PERFORMED" in optiland_script
    assert "OPTIONAL VALIDATION NOT ENABLED" in optiland_script
    assert "NO PRODUCTION-GRADE VALIDATION CLAIMED" in optiland_script
    assert "level3_achieved" in optiland_script
    elmer_script = (ROOT / "scripts" / "run_optional_elmer_validation.sh").read_text(
        encoding="utf-8"
    )
    assert "NO ELMER EXECUTION PERFORMED" in elmer_script
    assert "OPTIONAL VALIDATION NOT ENABLED" in elmer_script
    assert "NO PRODUCTION-GRADE VALIDATION CLAIMED" in elmer_script
    assert "level3_achieved" in elmer_script


def test_release_and_preflight_scripts_do_not_publish():
    scripts = [
        ROOT / "scripts" / "smoke_release.sh",
        ROOT / "scripts" / "testpypi_preflight.sh",
        ROOT / "scripts" / "run_quality_gates.sh",
        ROOT / "scripts" / "run_optional_gmsh_validation.sh",
        ROOT / "scripts" / "run_optional_meep_validation.sh",
        ROOT / "scripts" / "run_optional_mpb_validation.sh",
        ROOT / "scripts" / "run_optional_optiland_validation.sh",
        ROOT / "scripts" / "run_optional_elmer_validation.sh",
        ROOT / "scripts" / "run_optional_solver_micro_benchmarks.sh",
        ROOT / "scripts" / "check_optional_solver_readiness.py",
        ROOT / "scripts" / "smoke_agent_api.sh",
        ROOT / "scripts" / "smoke_backend_report.sh",
        ROOT / "scripts" / "generate_backend_capability_report.py",
        ROOT / "scripts" / "smoke_frontend_mvp.sh",
        ROOT / "scripts" / "smoke_frontend_visual.sh",
        ROOT / "Makefile",
    ]
    forbidden = [
        "twine upload",
        "python -m twine upload",
        "gh release create",
        "git push",
        "pypi upload",
    ]
    for path in scripts:
        text = path.read_text(encoding="utf-8").lower()
        for phrase in forbidden:
            assert phrase not in text, f"{path} contains forbidden publishing command: {phrase}"


def test_adapter_support_matrix_covers_registered_adapter_families():
    from optical_spec_agent.adapters.registry import list_adapters

    text = (ROOT / "docs" / "adapter_support_matrix.md").read_text(encoding="utf-8")
    for metadata in list_adapters():
        assert f"`{metadata.tool_name}`" in text
        assert metadata.current_status in text
    assert "External solvers are not run by default" in text
    assert "External LLM providers are not required" in text
    assert "no production-grade physical validation" in text.lower()
    assert "open-source-solver-first" in text
    assert "Proprietary/export-only future target" in text
    assert "not registered adapters unless" in text
    assert "0.9.0rc9.dev0" in text
    assert "v0.9.0rc8" in text
    assert "PyPI remains unpublished" in text
    assert "TestPyPI contains the `0.9.0rc6.dev0` development package" in text
    assert "TestPyPI upload for `0.9.0rc9.dev0` has not been performed" in text


def test_v1_evidence_docs_and_examples_are_offline_and_unpublished():
    paths = [
        ROOT / "examples" / "README.md",
        ROOT / "docs" / "release_readiness_current.md",
        ROOT / "docs" / "schema_compatibility_policy.md",
        ROOT / "docs" / "testpypi_dry_run_gate.md",
        ROOT / "docs" / "v1_0_stability_gate.md",
        ROOT / "docs" / "validation_gate.md",
        ROOT / "docs" / "packaging_gate.md",
    ]
    combined = "\n".join(path.read_text(encoding="utf-8") for path in paths)
    required = [
        "offline by default",
        "no external solver",
        "external LLM",
        "proprietary",
        "PyPI remains unpublished",
        "TestPyPI contains the `0.9.0rc6.dev0` development package",
        "0.9.0rc9.dev0",
        "GitHub release",
        "v0.9.0rc8",
        "not created",
    ]
    for phrase in required:
        assert phrase in combined


def test_offline_user_journey_release_artifacts_are_tracked():
    manifest = json.loads((ROOT / "examples" / "examples_manifest.json").read_text(encoding="utf-8"))
    paths = {item["path"] for item in manifest["examples"]}
    assert "examples/e2e/local_optical_workflow.json" in paths
    assert "examples/e2e/README.md" in paths
    for item in manifest["examples"]:
        assert item["requires_network"] is False
        assert item["requires_external_solver"] is False
        assert item["requires_external_llm"] is False
        assert item["requires_proprietary_solver"] is False

    journey = (ROOT / "docs" / "offline_user_journey.md").read_text(encoding="utf-8")
    assert "no external solver" in journey
    assert "no external LLM" in journey
    assert "no proprietary software" in journey
    assert "PyPI/TestPyPI: PyPI not published / TestPyPI uploaded for 0.9.0rc6.dev0" in journey
    assert "Current main development version: `0.9.0rc9.dev0`" in journey
    assert "Current public prerelease: v0.9.0rc8" in journey


def test_public_contract_freeze_artifacts_are_tracked():
    freeze = (ROOT / "docs" / "v1_0_public_contract_freeze.md").read_text(encoding="utf-8")
    manifest = json.loads((ROOT / "docs" / "public_contract_manifest.json").read_text(encoding="utf-8"))
    checklist = (ROOT / "docs" / "public_contract_change_checklist.md").read_text(encoding="utf-8")
    assert "v1.0.0 not released" in freeze
    assert "v0.9.0rc9 tag not created" in freeze
    assert "TestPyPI uploaded and verified for `0.9.0rc6.dev0`" in freeze
    assert "PyPI published: no" in freeze
    assert "Public contract freeze: approved" in freeze
    assert manifest["version_scope"] == "0.9.0rc9.dev0"
    assert manifest["current_public_prerelease"] == "v0.9.0rc8"
    assert manifest["release_state"]["pypi_published"] is False
    assert manifest["release_state"]["testpypi_uploaded"] is True
    assert manifest["release_state"]["testpypi_uploaded_version"] == "0.9.0rc6.dev0"
    assert manifest["release_state"]["testpypi_upload_for_0_9_0rc6_performed"] is False
    assert manifest["release_state"]["testpypi_upload_for_0_9_0rc7_dev0_performed"] is False
    assert (
        manifest["release_state"]["testpypi_status_doc"]
        == "docs/testpypi_status_v0.9.0rc6.dev0.md"
    )
    assert "external solver" in checklist
    assert "external LLM" in checklist
    assert "proprietary solver" in checklist


def test_external_solver_policy_keeps_solver_validation_optional():
    text = (ROOT / "docs" / "external_solver_policy.md").read_text(encoding="utf-8")
    assert "External solvers are not run by default" in text
    assert "Optional solver validation may be run manually" in text
    assert "No production-grade physical validation is claimed" in text
    assert "open-source-solver-first" in text
    assert "Proprietary commercial tools" in text
    assert "No proprietary license is required" in text


def test_external_llm_policy_keeps_network_llm_optional_and_tokens_safe():
    text = (ROOT / "docs" / "external_llm_policy.md").read_text(encoding="utf-8")
    assert "External LLM access is not required by default" in text
    assert "Default tests must not require network LLM calls" in text
    assert "Do not print, commit, or store provider tokens" in text


def test_bilingual_readme_contract_present():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    readme_zh = (ROOT / "README.zh-CN.md").read_text(encoding="utf-8")
    assert "README.zh-CN.md" in readme
    assert "README.md" in readme_zh
    assert "0.9.0rc1" in readme_zh
    assert "不是求解器" in readme_zh
    assert "不提供 production-grade physical validation" in readme_zh
    assert "MVP/scaffold" in readme_zh
    assert "workflow" in readme_zh
    assert "本地同步" in readme_zh


def test_docs_consistency_detects_missing_chinese_readme(tmp_path, monkeypatch):
    module = _load_docs_check_module()
    docs = tmp_path / "docs"
    src = tmp_path / "src" / "optical_spec_agent"
    docs.mkdir()
    src.mkdir(parents=True)
    (tmp_path / "README.md").write_text(
        """
# optical-spec-agent

Release status: current package version is 0.9.0rc1 release candidate.

## Current scope
## What works
## What does NOT work yet
## Quick start
## Roadmap
## License
""".strip(),
        encoding="utf-8",
    )
    (tmp_path / "pyproject.toml").write_text(
        """
[project]
name = "optical-spec-agent"
version = "0.9.0rc1"
""".strip(),
        encoding="utf-8",
    )
    (docs / "versioning_policy.md").write_text("policy\n", encoding="utf-8")
    (docs / "release_readiness_current.md").write_text("0.9.0rc1\n", encoding="utf-8")

    monkeypatch.setattr(module, "ROOT", tmp_path)
    monkeypatch.setattr(module, "README", tmp_path / "README.md")
    monkeypatch.setattr(module, "README_ZH", tmp_path / "README.zh-CN.md")
    monkeypatch.setattr(module, "DOCS", docs)
    monkeypatch.setattr(module, "SRC", src)

    report = module.build_report()
    assert report["status"] == "blocked"
    assert "README.zh-CN.md is missing." in report["errors"]


def test_release_readiness_report_schema(tmp_path):
    report_path = tmp_path / "release_readiness_report.json"
    result = _run(["scripts/check_release_readiness.py", "--report", str(report_path), "--json"])
    assert result.returncode == 0, result.stdout + result.stderr
    report = json.loads(report_path.read_text(encoding="utf-8"))
    assert report["schema_version"] == "release_readiness_report.v0.1"
    assert "status" in report
    assert "blockers" in report
    assert "warnings" in report
    assert "recommended_actions" in report


def test_release_readiness_intentional_preview_mismatch_is_warning(tmp_path):
    _write_minimal_release_repo(
        tmp_path,
        version="0.5.0",
        readme=(
            "Release status: packaged baseline is 0.5.0. "
            "Main branch includes v0.9 preview capability, not a formal release."
        ),
    )
    result = _run(["scripts/check_release_readiness.py", "--root", str(tmp_path), "--json"])
    assert result.returncode == 0, result.stdout + result.stderr
    report = json.loads(result.stdout)
    assert report["status"] == "warning"
    assert report["blockers"] == []
    assert any("intentional" in warning for warning in report["warnings"])


def test_release_readiness_misleading_formal_release_claim_blocks(tmp_path):
    _write_minimal_release_repo(
        tmp_path,
        version="0.5.0",
        readme="Release status: formal GitHub release is v0.9.0.",
    )
    result = _run(["scripts/check_release_readiness.py", "--root", str(tmp_path), "--json"])
    assert result.returncode == 1
    report = json.loads(result.stdout)
    assert report["status"] == "blocked"
    assert any("formal GitHub release" in blocker for blocker in report["blockers"])


def test_release_readiness_missing_policy_docs_blocks(tmp_path):
    _write_minimal_release_repo(
        tmp_path,
        version="0.9.0rc1",
        readme="Release status: packaged candidate is 0.9.0rc1.",
    )
    (tmp_path / "docs" / "versioning_policy.md").unlink()
    result = _run(["scripts/check_release_readiness.py", "--root", str(tmp_path), "--json"])
    assert result.returncode == 1
    report = json.loads(result.stdout)
    assert report["status"] == "blocked"
    assert "docs/versioning_policy.md is missing." in report["blockers"]


def test_release_readiness_clean_rc_version_is_ready(tmp_path):
    _write_minimal_release_repo(
        tmp_path,
        version="0.9.0rc1",
        readme=(
            "Release status: packaged release candidate is 0.9.0rc1. "
            "Capabilities remain preview/scaffold/evaluation work."
        ),
    )
    result = _run(["scripts/check_release_readiness.py", "--root", str(tmp_path), "--json"])
    assert result.returncode == 0, result.stdout + result.stderr
    report = json.loads(result.stdout)
    assert report["status"] == "ready"
    assert report["warnings"] == []


def test_artifact_contract_check_generates_report(tmp_path):
    output_dir = tmp_path / "artifact_contracts"
    report_path = tmp_path / "artifact_contract_report.json"
    result = _run(
        [
            "scripts/check_artifact_contracts.py",
            "--output-dir",
            str(output_dir),
            "--report",
            str(report_path),
            "--json",
        ]
    )
    assert result.returncode == 0, result.stdout + result.stderr
    report = json.loads(report_path.read_text(encoding="utf-8"))
    assert report["schema_version"] == "artifact_contract_check.v0.1"
    assert report["errors"] == []
    assert "execution_diagnostics.json" in report["artifacts"]
    assert "mesh_report.csv" in report["artifacts"]
    assert "flux_report.csv" in report["artifacts"]


def test_regenerate_demo_outputs_runs(tmp_path):
    result = _run(["scripts/regenerate_demo_outputs.py", "--output-dir", str(tmp_path)])
    assert result.returncode == 0, result.stdout + result.stderr
    manifest = tmp_path / "demo_manifest.json"
    assert manifest.exists()
    data = json.loads(manifest.read_text(encoding="utf-8"))
    assert data["schema_version"] == "demo_artifacts.v0.1"
    assert data["generated_outputs"]


def test_pytest_markers_registered():
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    markers = "\n".join(pyproject["tool"]["pytest"]["ini_options"]["markers"])
    assert "meep" in markers
    assert "external_solver" in markers
    assert "external_llm" in markers
    assert "slow" in markers
