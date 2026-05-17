import type { AgentTaskSessionResponse } from "../api/types";
import { useI18n } from "../i18n/useI18n";
import { BoundaryBadge } from "./BoundaryBadge";

interface AgentTaskSummaryProps {
  session?: AgentTaskSessionResponse;
}

export function AgentTaskSummary({ session }: AgentTaskSummaryProps) {
  const { t } = useI18n();

  if (!session) {
    return null;
  }

  return (
    <section className="page-panel wide">
      <h3>{t("commandCenter.taskSummary")}</h3>
      <div className="status-grid compact-grid">
        <div>
          <span>{t("commandCenter.sessionId")}</span>
          <strong>{session.session_id}</strong>
        </div>
        <div>
          <span>{t("commandCenter.opticalIntent")}</span>
          <strong>{session.optical_intent_summary}</strong>
        </div>
        <div>
          <span>{t("commandCenter.designCase")}</span>
          <strong>{session.design_case_summary}</strong>
        </div>
        <div>
          <span>{t("commandCenter.status")}</span>
          <BoundaryBadge tone={session.status === "ok" ? "safe" : "notice"}>
            {session.status}
          </BoundaryBadge>
        </div>
      </div>
      <p>{session.final_recommendation}</p>
    </section>
  );
}
