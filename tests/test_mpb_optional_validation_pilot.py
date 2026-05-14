"""MPB optional validation pilot safety checks."""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_mpb_optional_validation_pilot_artifacts_exist():
    assert (ROOT / "docs" / "mpb_optional_validation_pilot.md").exists()
    assert (ROOT / "docs" / "mpb_level3_readiness.md").exists()
    assert (
        ROOT
        / "docs"
        / "manual_solver_validation_reports"
        / "mpb_validation_report_schema.json"
    ).exists()
    assert (ROOT / "scripts" / "run_optional_mpb_validation.sh").exists()
    assert (ROOT / "validation" / "mpb" / "README.md").exists()


def test_mpb_optional_validation_script_default_mode_does_not_execute(tmp_path):
    report = tmp_path / "mpb-report.json"
    result = subprocess.run(
        [str(ROOT / "scripts" / "run_optional_mpb_validation.sh")],
        cwd=ROOT,
        env={
            **os.environ,
            "OSA_MPB_VALIDATION_REPORT": str(report),
            "OSA_RUN_OPTIONAL_MPB_VALIDATION": "0",
        },
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=60,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "NO MPB EXECUTION PERFORMED" in result.stdout
    assert "OPTIONAL VALIDATION NOT ENABLED" in result.stdout
    data = json.loads(report.read_text(encoding="utf-8"))
    assert data["optional_validation_enabled"] is False
    assert data["mpb_executed"] is False
    assert data["level3_achieved"] is False
    assert data["production_grade_validation_claimed"] is False
    assert data["formal_convergence_proof_claimed"] is False
    assert data["proprietary_required"] is False
    assert "mpb_cli_available" in data


def test_mpb_optional_validation_script_has_no_publish_or_release_commands():
    text = (ROOT / "scripts" / "run_optional_mpb_validation.sh").read_text(encoding="utf-8")
    assert "NO MPB EXECUTION PERFORMED" in text
    assert "OPTIONAL VALIDATION NOT ENABLED" in text
    assert "OSA_RUN_OPTIONAL_MPB_VALIDATION" in text
    assert "from meep import mpb" in text
    assert "mpb.ModeSolver" in text
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
