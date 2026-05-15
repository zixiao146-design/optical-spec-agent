"""Elmer optional validation pilot safety checks."""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_elmer_optional_validation_pilot_artifacts_exist():
    assert (ROOT / "docs" / "elmer_optional_validation_pilot.md").exists()
    assert (ROOT / "docs" / "elmer_level3_readiness.md").exists()
    assert (
        ROOT
        / "docs"
        / "manual_solver_validation_reports"
        / "elmer_validation_report_schema.json"
    ).exists()
    assert (ROOT / "scripts" / "run_optional_elmer_validation.sh").exists()
    assert (ROOT / "validation" / "elmer" / "README.md").exists()


def test_elmer_optional_validation_script_default_mode_does_not_execute(tmp_path):
    report = tmp_path / "elmer-report.json"
    result = subprocess.run(
        [str(ROOT / "scripts" / "run_optional_elmer_validation.sh")],
        cwd=ROOT,
        env={
            **os.environ,
            "OSA_ELMER_VALIDATION_REPORT": str(report),
            "OSA_RUN_OPTIONAL_ELMER_VALIDATION": "0",
        },
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=60,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "NO ELMER EXECUTION PERFORMED" in result.stdout
    assert "OPTIONAL VALIDATION NOT ENABLED" in result.stdout
    data = json.loads(report.read_text(encoding="utf-8"))
    assert data["optional_validation_enabled"] is False
    assert data["elmer_executed"] is False
    assert data["level3_achieved"] is False
    assert data["production_grade_validation_claimed"] is False
    assert data["formal_convergence_proof_claimed"] is False
    assert data["proprietary_required"] is False
    assert data["solver_installation_status"] in {
        "available",
        "unavailable_or_deferred",
    }
    if not data["elmer_available"]:
        assert data["install_deferred_record"] == (
            "validation/elmer/elmer_install_deferred_2026-05-15.md"
        )


def test_elmer_optional_validation_script_has_no_publish_or_release_commands():
    text = (ROOT / "scripts" / "run_optional_elmer_validation.sh").read_text(
        encoding="utf-8"
    )
    assert "NO ELMER EXECUTION PERFORMED" in text
    assert "OPTIONAL VALIDATION NOT ENABLED" in text
    assert "OSA_RUN_OPTIONAL_ELMER_VALIDATION" in text
    assert "ElmerSolver" in text
    assert "level3_achieved" in text
    assert "formal_convergence_proof_claimed" in text
    forbidden = [
        "twine upload",
        "python -m twine upload",
        "gh release create",
        "git tag",
        "git push",
        "upload.pypi.org",
        "test.pypi.org",
    ]
    lowered = text.lower()
    for phrase in forbidden:
        assert phrase not in lowered
