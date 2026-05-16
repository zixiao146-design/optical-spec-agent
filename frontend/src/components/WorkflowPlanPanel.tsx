import type { WorkflowPlanResponse } from "../api/types";
import { BoundaryBadge } from "./BoundaryBadge";

interface WorkflowPlanPanelProps {
  response?: WorkflowPlanResponse;
}

export function WorkflowPlanPanel({ response }: WorkflowPlanPanelProps) {
  if (!response) {
    return <p className="muted">Generate a local workflow preview to inspect steps.</p>;
  }
  const plan = response.workflow_plan;
  const steps = Array.isArray(plan.planned_steps) ? plan.planned_steps : [];
  return (
    <section className="workflow-panel">
      <div className="boundary-row">
        <BoundaryBadge>No solver was executed</BoundaryBadge>
        <BoundaryBadge>No external LLM was called</BoundaryBadge>
      </div>
      <ol className="step-list">
        {steps.map((step) => (
          <li key={String(step)}>{String(step)}</li>
        ))}
      </ol>
    </section>
  );
}
