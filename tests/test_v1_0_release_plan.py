"""v1.0.0 release plan documentation checks."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_v1_0_release_plan_exists_and_keeps_actions_gated():
    path = ROOT / "docs" / "v1_0_release_plan.md"
    assert path.exists()
    text = path.read_text(encoding="utf-8")
    assert "Proposed release sequence" in text
    assert "Required release artifacts" in text
    assert "Create annotated `v1.0.0` tag only after explicit approval" in text
    assert "Optionally publish PyPI only after separate explicit approval" in text
    assert "No `v1.0.0` tag" in text
    assert "No PyPI publication" in text

