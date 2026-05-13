"""Workflow preview contract tests: local, synchronous, no solver by default."""

from __future__ import annotations

import json
from pathlib import Path

from optical_spec_agent.workflows import WorkflowRunner, WorkflowRunnerConfig
from optical_spec_agent.workflows.planner import plan_workflow


def test_workflow_plan_documents_no_execute_policy():
    manifest = json.loads(
        (Path(__file__).resolve().parents[1] / "docs" / "public_contract_manifest.json").read_text(
            encoding="utf-8"
        )
    )
    plan = plan_workflow(
        "用 MPB 计算二维光子晶体 band diagram。",
        parser="hybrid",
        llm_provider="mock",
        tool="mpb",
    )
    assert plan.schema_version == "workflow_plan.v0.9"
    assert plan.selected_tool == "mpb"
    assert plan.execute_policy == "no_execute_by_default"
    assert manifest["workflow"]["execute_policy_default"] == "no_execute_by_default"
    assert manifest["workflow"]["external_solver_required_by_default"] is False
    assert manifest["workflow"]["external_llm_required_by_default"] is False
    assert "artifacts/diagnostics_not_applicable.json" in plan.expected_artifacts
    assert any("No external solver execution" in item for item in plan.limitations)
    contract = (Path(__file__).resolve().parents[1] / "docs" / "workflow_preview_contract.md").read_text(
        encoding="utf-8"
    )
    assert "workflow-plan" in contract
    assert "No external solver is run by default" in contract

    plan_dict = json.loads(plan.model_dump_json())
    assert set(manifest["workflow"]["workflow_plan_public_keys"]) <= set(plan_dict)


def test_workflow_run_no_execute_artifact_contract(tmp_path: Path):
    workflow = WorkflowRunner(
        WorkflowRunnerConfig(
            parser="hybrid",
            llm_provider="mock",
            tool="mpb",
            output_dir=tmp_path,
            allow_execute=False,
            run_diagnostics=True,
        )
    ).run("用 MPB 计算二维光子晶体 band diagram。")

    assert workflow.selected_tool == "mpb"
    assert workflow.status in {"success", "warning"}

    execution_plan = json.loads((tmp_path / "artifacts/execution_plan.json").read_text(encoding="utf-8"))
    assert execution_plan["allow_execute"] is False
    assert execution_plan["will_execute"] is False
    assert execution_plan["default_policy"] == "no external solver execution by default"

    execution_skip = json.loads((tmp_path / "artifacts/execution_skip.json").read_text(encoding="utf-8"))
    assert execution_skip["skipped"] is True

    diagnostics = json.loads((tmp_path / "artifacts/diagnostics_not_applicable.json").read_text(encoding="utf-8"))
    assert diagnostics["applicable"] is False
    assert "not mpb" in diagnostics["reason"].lower() or "not" in diagnostics["reason"].lower()

    run_data = json.loads((tmp_path / "workflow_run.json").read_text(encoding="utf-8"))
    assert {"schema_version", "status", "selected_tool", "artifacts"} <= set(run_data)
    assert run_data["artifacts"]["execution_skip.json"]["exists"] is True
    assert run_data["artifacts"]["diagnostics_not_applicable.json"]["exists"] is True
