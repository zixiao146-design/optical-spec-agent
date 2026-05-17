"""Sub-agent audit script tests."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_sub_agent_audit_script_runs_and_reports_reality(tmp_path: Path):
    report_path = tmp_path / "sub_agent_audit.json"
    env = {**os.environ, "OSA_SUB_AGENT_AUDIT_JSON": str(report_path)}
    result = subprocess.run(
        [sys.executable, "scripts/audit_sub_agents.py"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env,
        timeout=120,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "SpecAgent" in result.stdout
    assert "NO SOLVER EXECUTION PERFORMED" in result.stdout
    assert "NO EXTERNAL LLM CALLED" in result.stdout
    assert "NO UPLOAD PERFORMED" in result.stdout
    assert "NO TAG CREATED" in result.stdout
    assert "NO RELEASE CREATED" in result.stdout

    report = json.loads(report_path.read_text(encoding="utf-8"))
    agent_names = {entry["agent_name"] for entry in report["agents"]}
    assert {
        "SpecAgent",
        "MaterialAgent",
        "GeometryAgent",
        "AdapterAgent",
        "WorkflowAgent",
        "EvidenceAgent",
        "SafetyAgent",
        "RecommendationAgent",
    }.issubset(agent_names)
    for entry in report["agents"]:
        assert "importable_class" in entry
        assert entry["callable_function"] is True
        assert entry["executed_in_sample_session"] is True
    assert report["sample_session"]["external_solver_executed"] is False
    assert report["sample_session"]["external_llm_required"] is False


def test_sub_agent_audit_script_has_no_forbidden_operations():
    text = (ROOT / "scripts" / "audit_sub_agents.py").read_text(encoding="utf-8")
    assert "twine upload" not in text
    assert "gh release create" not in text
    assert "git tag" not in text

