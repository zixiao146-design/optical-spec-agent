"""v1.0 public contract freeze checklist checks."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_v1_0_public_contract_freeze_checklist_tracks_scope_and_decisions():
    path = ROOT / "docs" / "v1_0_public_contract_freeze_checklist.md"
    assert path.exists()
    text = path.read_text(encoding="utf-8")

    assert "Current public prerelease: v0.9.0rc7" in text
    assert "Current main release draft: 0.9.0rc8" in text
    assert "v0.9.0rc8 tag: not created" in text
    assert "v1.0.0: not released" in text
    assert "TestPyPI: uploaded for 0.9.0rc6.dev0" in text
    assert "TestPyPI verified: yes" in text
    assert "Clean install from TestPyPI: passed" in text
    assert "Maintainer confirmation: approved" in text
    assert "Freeze approval date: 2026-05-16" in text
    assert "Freeze baseline commit: 6e7ddf9c1811685c12db16bffb55cd76455267fe" in text
    assert "Approved frozen contract areas" in text
    for phrase in [
        "Console script: `optical-spec`",
        "Documented CLI commands",
        "Documented no-network examples",
        "Examples manifest paths",
        "Schema public fields",
        "Adapter registry names",
        "`adapter-list --json` top-level shape",
        "`workflow-plan --json` public top-level keys",
        "Package metadata",
        "No-default external solver",
    ]:
        assert phrase in text
    assert "Areas still preview / not frozen" in text
    assert "Adapter generated-script internals" in text
    assert "Optional solver validation internals" in text
    assert "TestPyPI decision | completed for 0.9.0rc6.dev0" in text
    assert "docs/testpypi_status_v0.9.0rc6.dev0.md" in text
    assert "PyPI publication decision | not granted" in text
    assert "Elmer Level 3 | deferred/non-blocking" in text
    assert "Production-grade physical validation | non-goal unless explicitly claimed" in text
    assert "Formal convergence proof | non-goal unless explicitly claimed" in text
    assert "Remaining hard blockers" in text
    assert "PyPI publication decision" in text
    for phrase in [
        "docs/v1_0_public_contract_freeze_confirmation.md",
        "docs/v1_0_contract_frozen_surface.md",
        "docs/v1_0_contract_non_goals.md",
        "docs/v1_0_breaking_change_policy.md",
        "docs/v1_0_public_contract_freeze_status.md",
    ]:
        assert phrase in text


def test_public_contract_manifest_tracks_post_rc7_state_without_publish_or_upload():
    text = (ROOT / "docs" / "public_contract_manifest.json").read_text(encoding="utf-8")
    assert '"version_scope": "0.9.0rc8"' in text
    assert '"current_public_prerelease": "v0.9.0rc7"' in text
    assert '"v0_9_0rc5_tag_created": true' in text
    assert '"v0_9_0rc6_tag_created": true' in text
    assert '"v0_9_0rc7_tag_created": true' in text
    assert '"v0_9_0rc8_tag_created": false' in text
    assert '"pypi_published": false' in text
    assert '"testpypi_uploaded": true' in text
    assert '"testpypi_uploaded_version": "0.9.0rc6.dev0"' in text
    assert '"testpypi_status_doc": "docs/testpypi_status_v0.9.0rc6.dev0.md"' in text
    assert '"testpypi_upload_for_0_9_0rc6_performed": false' in text
    assert '"testpypi_upload_for_0_9_0rc7_dev0_performed": false' in text
    assert '"testpypi_upload_for_0_9_0rc8_dev0_performed": false' in text
    assert '"public_contract_freeze"' in text
    assert '"status": "approved"' in text
    assert '"approval_date": "2026-05-16"' in text
    assert '"freeze_baseline_commit": "6e7ddf9c1811685c12db16bffb55cd76455267fe"' in text
    assert '"status_doc": "docs/v1_0_public_contract_freeze_status.md"' in text
