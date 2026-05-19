"""Validation claim audit script tests."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "scripts/audit_validation_claims.py", *args],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=120,
        check=False,
    )


def test_validation_claim_audit_script_runs_for_repo():
    result = _run()
    assert result.returncode == 0, result.stdout + result.stderr
    assert "VALIDATION CLAIM AUDIT PASSED" in result.stdout
    assert "NO SOLVER EXECUTION PERFORMED" in result.stdout
    script = ROOT / "scripts" / "audit_validation_claims.py"
    assert script.exists()


def test_validation_claim_audit_catches_unsafe_phrase(tmp_path: Path):
    unsafe = tmp_path / "unsafe.md"
    unsafe.write_text("This is production-grade physical validation.\n", encoding="utf-8")
    result = _run(str(unsafe))
    assert result.returncode != 0
    assert "VALIDATION CLAIM AUDIT FAILED" in result.stdout
    assert "production-grade physical validation" in result.stdout


def test_validation_claim_audit_allows_negated_safe_phrase(tmp_path: Path):
    safe = tmp_path / "safe.md"
    safe.write_text(
        "No production-grade physical validation is claimed.\n"
        "No formal convergence proof is claimed.\n",
        encoding="utf-8",
    )
    result = _run(str(safe))
    assert result.returncode == 0, result.stdout + result.stderr
    assert "VALIDATION CLAIM AUDIT PASSED" in result.stdout

