"""Workflow preview fixture evidence for deterministic local contracts."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from optical_spec_agent.workflows import WorkflowRunner, WorkflowRunnerConfig, replay_workflow


ROOT = Path(__file__).resolve().parents[1]
REQUEST = ROOT / "examples" / "workflows" / "local_preview_request.json"
EXPECTED = ROOT / "tests" / "fixtures" / "workflow_preview" / "local_preview_expected_keys.json"


def _request() -> dict:
    return json.loads(REQUEST.read_text(encoding="utf-8"))


def test_workflow_plan_fixture_has_stable_public_shape():
    expected = json.loads(EXPECTED.read_text(encoding="utf-8"))
    result = subprocess.run(
        ["optical-spec", "workflow-plan", str(REQUEST.relative_to(ROOT)), "--json"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=120,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    data = json.loads(result.stdout)
    for key in expected["workflow_plan"]:
        assert key in data
    assert data["parser_mode"] == "hybrid"
    assert data["selected_tool"] == "mpb"
    assert data["execute_policy"] == "no_execute_by_default"
    assert any("synchronous/local" in item for item in data["limitations"])


def test_workflow_run_and_replay_fixture_are_deterministic(tmp_path: Path):
    request = _request()
    expected = json.loads(EXPECTED.read_text(encoding="utf-8"))
    run_dir = tmp_path / "workflow"
    workflow = WorkflowRunner(
        WorkflowRunnerConfig(
            parser=request["parser"],
            llm_provider=request["llm_provider"],
            tool=request["tool"],
            output_dir=run_dir,
            allow_execute=False,
            run_diagnostics=True,
        )
    ).run(request["text"])

    run_data = json.loads((run_dir / "workflow_run.json").read_text(encoding="utf-8"))
    for key in expected["workflow_run"]:
        assert key in run_data
    for artifact in expected["required_artifacts"]:
        assert artifact in run_data["artifacts"]
        assert run_data["artifacts"][artifact]["exists"] is True
    assert run_data["selected_tool"] == "mpb"
    assert run_data["status"] in {"success", "warning"}

    replay = replay_workflow(run_dir / "workflow_run.json", output_dir=tmp_path / "replay")
    assert replay.original_run_id == workflow.run_id
    assert replay.deterministic_match is True
    assert replay.differences == []
