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
