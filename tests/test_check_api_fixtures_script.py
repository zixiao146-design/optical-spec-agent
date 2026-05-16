"""Live API fixture consistency script checks."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_check_api_fixtures_script_exists_and_is_local_only():
    path = ROOT / "scripts" / "check_api_fixtures.py"
    assert path.exists()
    text = path.read_text(encoding="utf-8")
    assert "frontend_fixture_manifest.json" in text
    assert "TestClient(app)" in text
    assert "NO SOLVER EXECUTION PERFORMED" in text
    assert "NO EXTERNAL LLM CALLED" in text
    assert "NO UPLOAD PERFORMED" in text
    lowered = text.lower()
    for phrase in ["requests.", "urllib", "httpx", "twine upload", "gh release create", "git tag"]:
        assert phrase not in lowered


def test_check_api_fixtures_script_runs_successfully():
    result = subprocess.run(
        [sys.executable, "scripts/check_api_fixtures.py"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=120,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "Checked" in result.stdout
    assert "NO SOLVER EXECUTION PERFORMED" in result.stdout
    assert "NO EXTERNAL LLM CALLED" in result.stdout
