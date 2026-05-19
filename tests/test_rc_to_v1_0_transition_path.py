"""RC to v1.0 transition path checks."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_rc_to_v1_0_transition_path_exists_and_tracks_options():
    path = ROOT / "docs" / "rc_to_v1_0_transition_path.md"
    assert path.exists()
    text = path.read_text(encoding="utf-8")
    assert "`v0.9.0rc6` is the current public prerelease" in text
    assert "`main` is" in text
    assert "`0.9.0rc7`" in text
    assert "v1.0.0 requires separate maintainer approval" in text
    assert "`0.9.0rc7` release draft -> `v0.9.0rc7` tag" in text
    assert "`0.9.0rc7` -> `1.0.0` release draft" in text
