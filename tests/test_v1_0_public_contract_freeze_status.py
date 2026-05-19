"""Approved v1.0 public contract freeze status checks."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_v1_0_public_contract_freeze_status_records_approval_and_scope():
    path = ROOT / "docs" / "v1_0_public_contract_freeze_status.md"
    assert path.exists()
    text = path.read_text(encoding="utf-8")

    assert "Status: approved" in text
    assert "Approval type: maintainer-approved documentation freeze" in text
    assert "Approval date: 2026-05-16" in text
    assert "Current public prerelease: v0.9.0rc7" in text
    assert "Current main development version: 0.9.0rc8.dev0" in text
    assert "Freeze baseline commit: 6e7ddf9c1811685c12db16bffb55cd76455267fe" in text
    assert "TestPyPI uploaded and verified: yes" in text
    assert "PyPI published: no" in text
    assert "PyPI publication approval: not granted" in text
    assert "v1.0.0 released: no" in text


def test_v1_0_public_contract_freeze_status_lists_frozen_and_unfrozen_areas():
    text = (ROOT / "docs" / "v1_0_public_contract_freeze_status.md").read_text(
        encoding="utf-8"
    )

    for phrase in [
        "`optical-spec` console script",
        "Documented CLI commands",
        "Documented CLI options covered by tests",
        "Schema public fields",
        "Adapter registry names",
        "`adapter-list --json` top-level shape",
        "`workflow-plan --json` top-level shape",
        "Examples manifest",
        "Package metadata/versioning semantics",
        "No-default solver/LLM/proprietary guarantees",
    ]:
        assert phrase in text

    for phrase in [
        "Generated adapter internals",
        "Workflow internals",
        "Optional solver validation internals",
        "External LLM-assisted parsing internals",
        "Proprietary export-only targets",
        "Production-grade physical validation",
        "Formal convergence proof",
        "Elmer Level 3 validation",
    ]:
        assert phrase in text

    assert "This freeze does not publish PyPI" in text
    assert "This freeze does not create `v1.0.0`" in text
    assert "This freeze does not create any tag or GitHub release" in text
