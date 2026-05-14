"""Gmsh optional validation pilot safety checks."""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_gmsh_optional_validation_pilot_artifacts_exist():
    assert (ROOT / "docs" / "gmsh_optional_validation_pilot.md").exists()
    assert (
        ROOT
        / "docs"
        / "manual_solver_validation_reports"
        / "gmsh_validation_pilot_template.md"
    ).exists()
    assert (ROOT / "scripts" / "run_optional_gmsh_validation.sh").exists()


def test_gmsh_optional_validation_script_default_mode_does_not_execute(tmp_path):
    report = tmp_path / "gmsh-report.json"
    result = subprocess.run(
        [
            str(ROOT / "scripts" / "run_optional_gmsh_validation.sh"),
        ],
        cwd=ROOT,
        env={
            **os.environ,
            "OSA_GMSH_VALIDATION_REPORT": str(report),
            "OSA_RUN_OPTIONAL_GMSH_VALIDATION": "0",
        },
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=60,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "NO GMSH EXECUTION PERFORMED" in result.stdout
    assert "OPTIONAL VALIDATION NOT ENABLED" in result.stdout
    data = json.loads(report.read_text(encoding="utf-8"))
    assert data["optional_validation_enabled"] is False
    assert data["gmsh_executed"] is False
    assert data["level3_achieved"] is False
    assert data["production_grade_validation_claimed"] is False
    assert data["formal_convergence_proof_claimed"] is False
    assert data["proprietary_required"] is False


def test_gmsh_optional_validation_script_has_no_publish_or_release_commands():
    text = (ROOT / "scripts" / "run_optional_gmsh_validation.sh").read_text(encoding="utf-8")
    assert "NO GMSH EXECUTION PERFORMED" in text
    assert "OPTIONAL VALIDATION NOT ENABLED" in text
    assert "OSA_RUN_OPTIONAL_GMSH_VALIDATION" in text
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
