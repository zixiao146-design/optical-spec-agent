"""Documentation index checks."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_docs_index_exists_and_links_major_docs():
    index = ROOT / "docs" / "README.md"
    assert index.exists()
    text = index.read_text(encoding="utf-8")
    required = [
        "Current public prerelease: v0.9.0rc4",
        "Current main development version: 0.9.0rc5.dev0",
        "release_readiness_current.md",
        "release_readiness_v0.9.0rc5.md",
        "post_release_status_v0.9.0rc4.md",
        "quality_gates.md",
        "ci_quality_gate_parity.md",
        "release_dry_run_operations.md",
        "packaging_gate.md",
        "testpypi_dry_run_gate.md",
        "pypi_publication_decision.md",
        "testpypi_upload_approval_v0.9.0rc5.dev0.md",
        "secrets_and_token_hygiene.md",
        "cli_contract.md",
        "schema_contract.md",
        "schema_compatibility_policy.md",
        "v1_0_compatibility_policy.md",
        "v1_0_public_contract_freeze.md",
        "public_contract_change_checklist.md",
        "public_contract_manifest.json",
        "validation_gate.md",
        "validation_boundary.md",
        "validation_evidence_manifest.md",
        "adapter_maturity_model.md",
        "open_source_solver_validation_plan.md",
        "open_solver_validation_harness.md",
        "gmsh_optional_validation_pilot.md",
        "gmsh_level3_readiness.md",
        "manual_solver_validation_report_template.md",
        "manual_solver_validation_reports/gmsh_validation_pilot_template.md",
        "../validation/gmsh/gmsh_validation_pilot_2026-05-14.md",
        "pytest_marker_policy.md",
        "offline_user_journey.md",
        "error_model.md",
        "migration_notes_pre_v1.md",
        "open_source_solver_strategy.md",
        "proprietary_solver_policy.md",
        "external_solver_policy.md",
        "external_llm_policy.md",
        "../examples/README.md",
        "../examples/e2e/README.md",
        "../examples/examples_manifest.json",
        "maintainer_decision_log.md",
        "maintainer_operations_checklist.md",
        "v1_0_readiness_scorecard.md",
    ]
    for phrase in required:
        assert phrase in text
