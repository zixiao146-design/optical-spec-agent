"""Strict metadata diff tests for adapter-native golden checker."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_adapter_native_golden_checker_reports_metadata_diff_status(tmp_path: Path):
    report_path = tmp_path / "adapter-native-golden-report.json"
    env = {**os.environ, "OSA_ADAPTER_NATIVE_GOLDEN_REPORT": str(report_path)}
    result = subprocess.run(
        [sys.executable, "scripts/check_adapter_native_golden.py"],
        cwd=ROOT,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=180,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "ADAPTER NATIVE METADATA DIFF PASSED" in result.stdout
    assert report_path.exists()
    report = json.loads(report_path.read_text(encoding="utf-8"))
    assert report["case_count"] == 5
    for case in report["cases"]:
        assert case["metadata_match"] is True
        assert case["fragment_match"] is True
        assert case["safety_match"] is True
        assert case["missing_terms"] == []
        assert case["unexpected_claims"] == []
        assert case["status"] == "pass"
