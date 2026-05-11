"""Static workflow agent registry."""

from __future__ import annotations

from optical_spec_agent.workflows.agents import (
    AdapterSelectionAgent,
    DiagnosticsAgent,
    EvaluationAgent,
    ExecutionPlanAgent,
    GenerationAgent,
    HumanReviewAgent,
    IntakeAgent,
    OptionalMeepExecutionAgent,
    ParseAgent,
    ReportAgent,
    ValidateAgent,
    WorkflowAgent,
)


def list_workflow_agents() -> list[str]:
    """Return the default workflow agent order."""
    return [agent.name for agent in default_workflow_agents()]


def default_workflow_agents() -> list[WorkflowAgent]:
    """Instantiate the default v0.9 synchronous workflow agents."""
    return [
        IntakeAgent(),
        ParseAgent(),
        ValidateAgent(),
        AdapterSelectionAgent(),
        GenerationAgent(),
        ExecutionPlanAgent(),
        OptionalMeepExecutionAgent(),
        DiagnosticsAgent(),
        EvaluationAgent(),
        HumanReviewAgent(),
        ReportAgent(),
    ]
