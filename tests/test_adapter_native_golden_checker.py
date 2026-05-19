"""Adapter-native golden checker tests."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_adapter_native_golden_checker_runs_and_keeps_safety_boundaries():
    script = ROOT / "scripts" / "check_adapter_native_golden.py"
    assert script.exists()
    result = subprocess.run(
        [sys.executable, str(script)],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=180,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    for phrase in [
        "ADAPTER NATIVE GOLDEN CHECKS PASSED",
        "ADAPTER NATIVE METADATA DIFF PASSED",
        "NO SOLVER EXECUTION PERFORMED",
        "NO EXTERNAL LLM CALLED",
        "NO UPLOAD PERFORMED",
        "NO TAG CREATED",
        "NO RELEASE CREATED",
    ]:
        assert phrase in result.stdout
    text = script.read_text(encoding="utf-8")
    assert "twine upload" not in text
    assert "gh release create" not in text
    assert "git tag" not in text
