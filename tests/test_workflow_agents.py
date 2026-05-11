"""Tests for individual workflow agents."""

from optical_spec_agent.workflows import WorkflowRunnerConfig
from optical_spec_agent.workflows.agents import (
    AdapterSelectionAgent,
    DiagnosticsAgent,
    EvaluationAgent,
    ExecutionPlanAgent,
    GenerationAgent,
    HumanReviewAgent,
    IntakeAgent,
    ParseAgent,
    ReportAgent,
    ValidateAgent,
    WorkflowContext,
)
from optical_spec_agent.workflows.artifacts import ensure_workflow_dirs


def _context(tmp_path, text="用 MPB 计算二维光子晶体 band diagram，输出前 8 条能带。"):
    config = WorkflowRunnerConfig(
        parser="hybrid",
        llm_provider="mock",
        tool="mpb",
        output_dir=tmp_path,
    )
    return WorkflowContext(
        input_text=text,
        output_dir=tmp_path,
        config=config,
        run_id="workflow-test",
        dirs=ensure_workflow_dirs(tmp_path),
    )


def test_core_agents_write_expected_artifacts(tmp_path):
    context = _context(tmp_path)
    assert IntakeAgent().run(context).status in {"success", "warning"}
    assert (tmp_path / "input.txt").exists()

    assert ParseAgent().run(context).status in {"success", "warning"}
    assert (tmp_path / "artifacts/spec.json").exists()

    assert ValidateAgent().run(context).status in {"success", "warning", "error"}
    assert (tmp_path / "artifacts/validation_report.json").exists()

    assert AdapterSelectionAgent().run(context).status in {"success", "warning"}
    assert context.selected_adapter is not None
    assert (tmp_path / "artifacts/adapter_selection.json").exists()

    assert GenerationAgent().run(context).status in {"success", "warning"}
    assert (tmp_path / "artifacts/generated_input.py").exists()

    assert ExecutionPlanAgent().run(context).status in {"success", "warning"}
    assert (tmp_path / "artifacts/execution_plan.json").exists()

    assert DiagnosticsAgent().run(context).status == "skipped"
    assert (tmp_path / "artifacts/diagnostics_not_applicable.json").exists()

    assert EvaluationAgent().run(context).status in {"success", "warning", "error"}
    assert (tmp_path / "artifacts/workflow_evaluation.json").exists()

    assert HumanReviewAgent().run(context).status == "warning"
    assert (tmp_path / "human_review_checklist.md").exists()

    assert ReportAgent().run(context).status in {"success", "warning"}
    assert (tmp_path / "workflow_summary.md").exists()
