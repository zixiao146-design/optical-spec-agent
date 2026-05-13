"""Validation evidence manifest checks."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_validation_evidence_manifest_exists_and_maps_evidence_files():
    path = ROOT / "docs" / "validation_evidence_manifest.md"
    assert path.exists()
    text = path.read_text(encoding="utf-8")
    for phrase in [
        "examples/",
        "tests/fixtures/adapter_golden/",
        "tests/fixtures/workflow_preview/",
        "tests/test_documented_examples.py",
        "tests/test_adapter_family_evidence.py",
        "tests/test_workflow_evidence_fixtures.py",
        "tests/test_schema_compatibility_policy.py",
        "tests/test_failure_mode_regression.py",
        "scripts/smoke_release.sh",
    ]:
        assert phrase in text


def test_validation_evidence_manifest_keeps_claims_conservative():
    text = (ROOT / "docs" / "validation_evidence_manifest.md").read_text(encoding="utf-8")
    for phrase in [
        "No production-grade physical validation",
        "No formal convergence proof",
        "No solver-backed correctness claim by default",
        "No proprietary commercial solver validation",
        "No PyPI publication claim",
    ]:
        assert phrase in text
