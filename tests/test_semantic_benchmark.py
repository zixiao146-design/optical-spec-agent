"""Smoke test for the semantic benchmark runner."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def test_semantic_benchmark_runner_passes():
    repo_root = Path(__file__).resolve().parents[1]
    result = subprocess.run(
        [sys.executable, "benchmarks/run_semantic_benchmark.py"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert result.returncode == 0, result.stdout + result.stderr
