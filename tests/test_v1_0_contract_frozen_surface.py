"""v1.0 frozen surface candidate checks."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_frozen_surface_candidate_lists_public_surface_and_evidence():
    path = ROOT / "docs" / "v1_0_contract_frozen_surface.md"
    assert path.exists()
    text = path.read_text(encoding="utf-8")

    assert "v1.0 Contract Frozen Surface" in text
    assert "Status: maintainer-approved" in text
    assert "Approval date: 2026-05-16" in text
    assert "Freeze baseline commit: 6e7ddf9c1811685c12db16bffb55cd76455267fe" in text
    assert "PyPI publication approval: not granted" in text
    assert "v1.0.0 released: no" in text
    for phrase in [
        "CLI command names",
        "CLI examples",
        "Schema fields",
        "Adapter registry names",
        "`adapter-list --json` shape",
        "`workflow-plan --json` keys",
        "Examples manifest",
        "Project name, version semantics, console script",
        "No-default solver/LLM/proprietary guarantees",
        "tests/test_cli_contract.py",
        "tests/test_schema_contract.py",
        "tests/test_adapter_registry.py",
        "tests/test_workflow_preview_contract.py",
        "tests/test_examples_manifest.py",
    ]:
        assert phrase in text


def test_frozen_surface_candidate_excludes_preview_and_validation_claims():
    text = (ROOT / "docs" / "v1_0_contract_frozen_surface.md").read_text(
        encoding="utf-8"
    )

    for phrase in [
        "generated adapter internals",
        "workflow\nimplementation internals",
        "optional solver validation internals",
        "production-grade\nphysical validation",
        "formal convergence proof",
        "Elmer Level 3 validation",
    ]:
        assert phrase in text
