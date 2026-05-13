"""v1.0 compatibility policy checks."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_v1_0_compatibility_policy_exists_and_scopes_contracts():
    path = ROOT / "docs" / "v1_0_compatibility_policy.md"
    assert path.exists()
    text = path.read_text(encoding="utf-8")
    for phrase in [
        "CLI command names",
        "JSON output top-level keys",
        "Schema public fields",
        "Adapter registry names",
        "Workflow preview output shape",
        "Package metadata",
    ]:
        assert phrase in text


def test_v1_0_compatibility_policy_documents_preview_and_migration_boundary():
    text = (ROOT / "docs" / "v1_0_compatibility_policy.md").read_text(encoding="utf-8")
    for phrase in [
        "Preview / non-stable scopes",
        "Adapter generated script internals may evolve",
        "Migration policy before v1.0",
        "Breaking changes before `v1.0` are allowed",
        "Release notes should mention user-visible contract changes",
    ]:
        assert phrase in text


def test_v1_0_compatibility_policy_entry_criteria_are_offline_by_default():
    text = (ROOT / "docs" / "v1_0_compatibility_policy.md").read_text(encoding="utf-8")
    for phrase in [
        "v1.0 entry criteria",
        "CLI contract tests pass",
        "Schema compatibility tests pass",
        "Adapter matrix consistency tests pass",
        "Workflow preview contract tests pass",
        "Documented examples pass",
        "Packaging gates pass",
        "No external solver or LLM is required by default",
    ]:
        assert phrase in text
