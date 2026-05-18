"""Backend report smoke script tests."""

from __future__ import annotations

import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_smoke_backend_report_script_exists_and_has_safety_markers():
    script = ROOT / "scripts" / "smoke_backend_report.sh"
    assert script.exists()
    text = script.read_text(encoding="utf-8")
    assert "generate_backend_capability_report.py" in text
    assert "/api/backend-capability-report" in text
    assert "/api/design-case-cross-checks" in text
    assert "/api/design-requirements" in text
    assert "/api/design-requirements/match" in text
    assert "BACKEND CAPABILITY REPORT PASSED" in text
    assert "DESIGN CASE CROSS-CHECKS PASSED" in text
    assert "DESIGN REQUIREMENT MATCHING PASSED" in text
    assert "NO SOLVER EXECUTION PERFORMED" in text
    assert "NO EXTERNAL LLM CALLED" in text
    assert "NO UPLOAD PERFORMED" in text
    assert "NO TAG CREATED" in text
    assert "NO RELEASE CREATED" in text
    for forbidden in ["twine upload", "gh release create", "git tag"]:
        assert forbidden not in text


def test_smoke_backend_report_script_runs_successfully():
    result = subprocess.run(
        ["./scripts/smoke_backend_report.sh"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=180,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "BACKEND CAPABILITY REPORT PASSED" in result.stdout
    assert "DESIGN CASE CROSS-CHECKS PASSED" in result.stdout
