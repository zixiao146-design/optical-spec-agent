"""Backend evidence pack smoke script tests."""

from __future__ import annotations

import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "smoke_backend_evidence_pack.sh"


def test_smoke_backend_evidence_pack_script_exists_and_has_safety_markers():
    assert SCRIPT.exists()
    text = SCRIPT.read_text(encoding="utf-8")
    assert "generate_backend_evidence_pack.py" in text
    assert "BACKEND EVIDENCE PACK PASSED" in text
    assert "NO SOLVER EXECUTION PERFORMED" in text
    assert "NO EXTERNAL LLM CALLED" in text
    assert "NO UPLOAD PERFORMED" in text
    assert "NO TAG CREATED" in text
    assert "NO RELEASE CREATED" in text
    assert "twine upload" not in text
    assert "gh release create" not in text
    assert "git tag" not in text


def test_smoke_backend_evidence_pack_script_runs_successfully():
    result = subprocess.run(
        [str(SCRIPT)],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=180,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "BACKEND EVIDENCE PACK PASSED" in result.stdout
    assert "NO SOLVER EXECUTION PERFORMED" in result.stdout
    assert "NO EXTERNAL LLM CALLED" in result.stdout
    assert "NO UPLOAD PERFORMED" in result.stdout
    assert "NO TAG CREATED" in result.stdout
    assert "NO RELEASE CREATED" in result.stdout
