"""v1.0 public contract freeze confirmation package checks."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_freeze_confirmation_tracks_pending_status_and_scope():
    path = ROOT / "docs" / "v1_0_public_contract_freeze_confirmation.md"
    assert path.exists()
    text = path.read_text(encoding="utf-8")

    assert "Current public prerelease: v0.9.0rc5" in text
    assert "Current main development version: 0.9.0rc6.dev0" in text
    assert "TestPyPI uploaded and verified: yes" in text
    assert "PyPI published: no" in text
    assert "v1.0.0 released: no" in text
    assert "Maintainer confirmation: pending" in text
    assert "This document prepares the maintainer-facing confirmation package" in text
    assert "This document does not approve the freeze" in text


def test_freeze_confirmation_lists_frozen_areas_and_gates():
    text = (ROOT / "docs" / "v1_0_public_contract_freeze_confirmation.md").read_text(
        encoding="utf-8"
    )

    for phrase in [
        "`optical-spec` console script",
        "Documented CLI commands",
        "Documented CLI options that are explicitly covered by contract tests",
        "Documented JSON schema public fields",
        "Adapter registry names",
        "`adapter-list --json` top-level shape",
        "`workflow-plan --json` top-level shape",
        "Offline examples and examples manifest",
        "No-network/no-default-solver/no-default-LLM/no-default-proprietary guarantees",
        "Package metadata: name, version semantics, console script",
        "Quality gates pass",
        "CI pass",
        "Pytest/build/make check pass",
        "TestPyPI verified",
        "PyPI publication decision remains explicit",
        "Validation claims reviewed",
        "Maintainer explicitly approves freeze",
    ]:
        assert phrase in text


def test_freeze_confirmation_lists_not_frozen_areas():
    text = (ROOT / "docs" / "v1_0_public_contract_freeze_confirmation.md").read_text(
        encoding="utf-8"
    )

    for phrase in [
        "Generated adapter script internals",
        "Optional solver validation internals",
        "Workflow implementation internals",
        "External LLM-assisted parse internals",
        "Proprietary export-only future targets",
        "Production-grade physical validation",
        "Formal convergence proof",
        "Elmer Level 3 validation",
    ]:
        assert phrase in text

