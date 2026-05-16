"""v1.0 breaking change policy checks."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_breaking_change_policy_covers_pre_and_post_freeze_rules():
    path = ROOT / "docs" / "v1_0_breaking_change_policy.md"
    assert path.exists()
    text = path.read_text(encoding="utf-8")

    assert "Breaking changes may still occur" in text
    assert "Breaking changes must be documented in migration notes" in text
    assert "public contract manifest should be updated" in text
    assert "Changes to the frozen public surface require maintainer approval" in text
    assert "Breaking changes require explicit migration notes" in text
    assert "Generated internals may change unless documented as frozen" in text
    assert "Preview/scaffold outputs may change" in text


def test_breaking_change_policy_tracks_versioning_and_non_authorization():
    text = (ROOT / "docs" / "v1_0_breaking_change_policy.md").read_text(
        encoding="utf-8"
    )

    assert "Release candidates use `rcN`" in text
    assert "Post-release main uses `rcN+1.dev0`" in text
    assert "Final `v1.0.0` requires separate approval" in text
    assert "does not authorize a v1.0 freeze" in text
    assert "PyPI publication" in text
    assert "tag creation" in text
    assert "GitHub release creation" in text
