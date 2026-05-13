"""Workflow-to-adapter planning evidence without external execution."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_workflow_plan_includes_adapter_no_execute_evidence():
    result = subprocess.run(
        [
            "optical-spec",
            "workflow-plan",
            "examples/workflows/local_preview_request.json",
            "--json",
        ],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=120,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    data = json.loads(result.stdout)
    assert data["selected_tool"] == "mpb"
    assert data["execute_policy"] == "no_execute_by_default"
    assert "generation" in data["planned_steps"]
    assert "optional_execution" in data["planned_steps"]
    assert "artifacts/adapter_selection.json" in data["expected_artifacts"]
    assert "artifacts/generated_input.*" in data["expected_artifacts"]
    assert "artifacts/diagnostics_not_applicable.json" in data["expected_artifacts"]
    assert any("No external solver execution" in item for item in data["limitations"])

