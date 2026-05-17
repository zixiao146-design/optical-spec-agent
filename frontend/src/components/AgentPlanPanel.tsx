import type { AgentPlanStep } from "../api/types";
import { useI18n } from "../i18n/useI18n";
import { BoundaryBadge } from "./BoundaryBadge";
import { EmptyState } from "./EmptyState";

interface AgentPlanPanelProps {
  steps: AgentPlanStep[];
}

export function AgentPlanPanel({ steps }: AgentPlanPanelProps) {
  const { language, t } = useI18n();

  return (
    <section className="page-panel wide">
      <h3>{t("commandCenter.agentPlan")}</h3>
      {steps.length === 0 ? (
        <EmptyState title={t("commandCenter.noPlanTitle")} message={t("commandCenter.noPlanMessage")} />
      ) : (
        <ol className="agent-trace-list">
          {steps.map((step) => (
            <li key={`${step.step_index}-${step.agent_name}`} className="timeline-step">
              <div className="timeline-marker">{step.step_index}</div>
              <div className="timeline-content">
                <div className="timeline-heading">
                  <h4>{language === "zh-CN" ? step.title_zh : step.title}</h4>
                  <span>{step.agent_name}</span>
                  <BoundaryBadge tone={step.status === "completed" ? "safe" : "notice"}>
                    {step.status}
                  </BoundaryBadge>
                </div>
                <p>{language === "zh-CN" ? step.description_zh : step.description}</p>
                <dl className="timeline-details">
                  <dt>{t("commandCenter.endpointOrTool")}</dt>
                  <dd>{step.endpoint_or_tool}</dd>
                  <dt>{t("commandCenter.expectedOutput")}</dt>
                  <dd>{step.expected_output}</dd>
                  <dt>{t("commandCenter.safetyNote")}</dt>
                  <dd>{step.safety_note}</dd>
                </dl>
              </div>
            </li>
          ))}
        </ol>
      )}
    </section>
  );
}
