"""Workflow replay support."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from optical_spec_agent.workflows.artifacts import write_json
from optical_spec_agent.workflows.models import ReplayReport, WorkflowRunnerConfig
from optical_spec_agent.workflows.reports import load_workflow_run
from optical_spec_agent.workflows.runner import WorkflowRunner


def replay_workflow(workflow_run_path: Path, *, output_dir: Path) -> ReplayReport:
    """Replay a workflow run with deterministic local settings and compare key fields."""
    original = load_workflow_run(workflow_run_path)
    config = WorkflowRunnerConfig(
        parser=original.parser_mode,
        llm_provider=original.llm_provider,
        tool=original.selected_tool,
        output_dir=output_dir,
        allow_execute=False,
        run_diagnostics=True,
        strict=False,
    )
    replayed = WorkflowRunner(config).run(original.input_text)
    compared = [
        "input_text",
        "parser_mode",
        "llm_provider",
        "selected_tool",
        "status",
    ]
    differences: list[dict[str, Any]] = []
    for field in compared:
        before = getattr(original, field)
        after = getattr(replayed, field)
        if before != after:
            differences.append({"field": field, "original": before, "replay": after})
    report = ReplayReport(
        original_run_id=original.run_id,
        replay_run_id=replayed.run_id,
        deterministic_match=not differences,
        compared_fields=compared,
        differences=differences,
        warnings=[] if not differences else ["Replay differed in non-time key fields."],
        replay_workflow_run=str(output_dir / "workflow_run.json"),
    )
    replay_report_path = output_dir / "replay" / "replay_report.json"
    write_json(replay_report_path, report)
    return report
