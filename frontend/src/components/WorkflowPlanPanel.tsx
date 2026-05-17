import type { WorkflowPlanResponse } from "../api/types";
import { useI18n } from "../i18n/useI18n";
import { BoundaryBadge } from "./BoundaryBadge";

interface WorkflowPlanPanelProps {
  response?: WorkflowPlanResponse;
}

export function WorkflowPlanPanel({ response }: WorkflowPlanPanelProps) {
  const { t } = useI18n();
  if (!response) {
    return <p className="muted">{t("workflow.panelEmpty")}</p>;
  }
  const plan = response.workflow_plan;
  const steps = Array.isArray(plan.planned_steps) ? plan.planned_steps : [];
  return (
    <section className="workflow-panel">
      <div className="boundary-row">
        <BoundaryBadge>{t("workflow.badge.noSolver")}</BoundaryBadge>
        <BoundaryBadge>{t("safety.noExternalLlmDefault")}</BoundaryBadge>
      </div>
      <ol className="step-list">
        {steps.map((step) => (
          <li key={String(step)}>{String(step)}</li>
        ))}
      </ol>
    </section>
  );
}
