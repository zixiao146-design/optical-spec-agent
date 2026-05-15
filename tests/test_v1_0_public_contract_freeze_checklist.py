"""v1.0 public contract freeze checklist checks."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_v1_0_public_contract_freeze_checklist_tracks_scope_and_decisions():
    path = ROOT / "docs" / "v1_0_public_contract_freeze_checklist.md"
    assert path.exists()
    text = path.read_text(encoding="utf-8")

    assert "Current public prerelease: v0.9.0rc5" in text
    assert "Current main development version: 0.9.0rc6.dev0" in text
    assert "v1.0.0: not released" in text
    assert "Candidate-stable contract areas" in text
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
    assert "TestPyPI decision | pending" in text
    assert "PyPI publication decision | not granted" in text
    assert "Elmer Level 3 | deferred/non-blocking" in text
    assert "Production-grade physical validation | non-goal unless explicitly claimed" in text
    assert "Formal convergence proof | non-goal unless explicitly claimed" in text


def test_public_contract_manifest_tracks_rc6_state_without_publish_or_upload():
    text = (ROOT / "docs" / "public_contract_manifest.json").read_text(encoding="utf-8")
    assert '"version_scope": "0.9.0rc6.dev0"' in text
    assert '"current_public_prerelease": "v0.9.0rc5"' in text
    assert '"v0_9_0rc5_tag_created": true' in text
    assert '"v0_9_0rc6_tag_created": false' in text
    assert '"pypi_published": false' in text
    assert '"testpypi_uploaded": false' in text
