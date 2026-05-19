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
    assert tools["source_monitor_inference"]["executed_in_sample"] is True
    assert tools["missing_input_diagnostics"]["executed_in_sample"] is True
    assert tools["observable_diagnostics"]["executed_in_sample"] is True
    assert tools["adapter_native_mapping"]["executed_in_sample"] is True
    assert tools["adapter_native_golden_coverage"]["executed_in_sample"] is True
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
    assert all(item["matched_by_heuristic"] for item in report["requirements_templates"])
    assert all(action["executed"] is False for action in report["blocked_external_actions"])
    text = markdown_out.read_text(encoding="utf-8")
    assert "Backend Capability Report" in text
    assert "Adapter-Native Golden Coverage" in text
    assert "Maintainer Evidence Pack" in text
    assert "NO UPLOAD PERFORMED" in text


def test_backend_capability_report_script_does_not_contain_release_commands():
    text = (ROOT / "scripts" / "generate_backend_capability_report.py").read_text(
        encoding="utf-8"
    )
    forbidden = ["twine upload", "gh release create", "git tag", "TESTPYPI_TOKEN", "PYPI_TOKEN"]
    for phrase in forbidden:
        assert phrase not in text
