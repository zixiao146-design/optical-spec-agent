"""Workflow planning helpers."""

from __future__ import annotations

from pathlib import Path

from optical_spec_agent.adapters.registry import AdapterRegistryError, dispatch_adapter
from optical_spec_agent.parsers.llm import LLMParserConfig
from optical_spec_agent.services.spec_service import SpecService
from optical_spec_agent.workflows.artifacts import write_json
from optical_spec_agent.workflows.models import WorkflowPlan


DEFAULT_PLANNED_STEPS = [
    "intake",
    "parse",
    "validate",
    "adapter_selection",
    "generation",
    "execution_plan",
    "optional_execution",
    "diagnostics",
    "evaluation",
    "human_review",
    "report",
]


def plan_workflow(
    input_text: str,
    *,
    parser: str = "rule",
    llm_provider: str = "mock",
    tool: str = "auto",
    output: Path | None = None,
) -> WorkflowPlan:
    """Create a lightweight workflow plan using parser/adapter intent only."""
    warnings: list[str] = []
    risk_flags: list[str] = []
    selected_tool = tool
    try:
        config = LLMParserConfig(
            provider=llm_provider,
            parser_mode="hybrid" if parser == "hybrid" else "llm",
        )
        spec = SpecService(parser=parser, llm_config=config).process(input_text)
        adapter = dispatch_adapter(spec, preferred_tool=tool)
        selected_tool = adapter.tool_name
        limitations = adapter.metadata().limitations
    except Exception as exc:  # noqa: BLE001 - planning should return explainable warnings.
        warnings.append(f"Could not fully infer adapter plan: {exc}")
        limitations = [
            "Plan is approximate because adapter dispatch did not resolve cleanly.",
            "Workflow planning does not run solvers or prove physical correctness.",
        ]
        if isinstance(exc, AdapterRegistryError):
            risk_flags.append("adapter_auto_selection_unresolved")

    expected_artifacts = [
        "input.txt",
        "workflow_plan.json",
        "workflow_run.json",
        "workflow_summary.md",
        "workflow_summary.json",
        "human_review_checklist.md",
        "steps/*.json",
        "artifacts/spec.json",
        "artifacts/validation_report.json",
        "artifacts/adapter_selection.json",
        "artifacts/generated_input.*",
        "artifacts/execution_plan.json",
        "artifacts/workflow_evaluation.json",
    ]
    if selected_tool == "meep":
        expected_artifacts.extend(
            [
                "artifacts/mesh_report.csv",
                "artifacts/flux_report.csv",
                "artifacts/execution_diagnostics.json",
                "artifacts/diagnostic_preview.png",
            ]
        )
    else:
        expected_artifacts.append("artifacts/diagnostics_not_applicable.json")

    plan = WorkflowPlan(
        input_text=input_text,
        planned_steps=DEFAULT_PLANNED_STEPS,
        parser_mode=parser,
        selected_tool=selected_tool,
        execute_policy="no_execute_by_default",
        expected_artifacts=expected_artifacts,
        risk_flags=risk_flags or ["human_review_required"],
        limitations=[
            *limitations,
            "Workflow v0.9 is synchronous/local orchestration only.",
            "No external solver execution is planned by default.",
        ],
        warnings=warnings,
    )
    if output:
        write_json(output, plan)
    return plan
