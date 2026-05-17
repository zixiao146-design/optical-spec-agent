import { useState } from "react";
import { agentApi } from "../api/client";
import { stateFromPayload, type RemoteState } from "../api/state";
import type { AgentTraceResponse } from "../api/types";
import { ApiDisconnectedNotice } from "../components/ApiDisconnectedNotice";
import { BoundaryBadge } from "../components/BoundaryBadge";
import { DiagnosticsPanel } from "../components/DiagnosticsPanel";
import { EmptyState } from "../components/EmptyState";
import { ErrorState } from "../components/ErrorState";
import { JsonPanel } from "../components/JsonPanel";
import { LoadingState } from "../components/LoadingState";
import { RecommendedActions } from "../components/RecommendedActions";
import { demoAgentTrace } from "../fixtures/demoData";
import { useI18n } from "../i18n/useI18n";

export function AgentCollaborationPage() {
  const { t } = useI18n();
  const [trace, setTrace] = useState<RemoteState<AgentTraceResponse>>({ status: "idle" });

  async function loadTrace() {
    setTrace({ status: "loading", message: t("agentTrace.loadingMessage") });
    const payload = await agentApi.getAgentTrace({
      example_id: "nanoparticle_plasmonics",
      text: "nanoparticle plasmonics with Ag/Au preview materials and Meep/Gmsh workflow",
    });
    setTrace(stateFromPayload(payload, demoAgentTrace, t("agentTrace.demo")));
  }

  const agents = trace.data?.agents || [];

  return (
    <div className="page-grid">
      <section className="page-panel wide">
        <div className="page-title">
          <span>{t("agentTrace.kicker")}</span>
          <h2>{t("agentTrace.title")}</h2>
          <p>{t("agentTrace.description")}</p>
        </div>
        <div className="boundary-row">
          <BoundaryBadge>{t("agentTrace.badge.noSolver")}</BoundaryBadge>
          <BoundaryBadge>{t("agentTrace.badge.noLlm")}</BoundaryBadge>
          <BoundaryBadge tone="notice">{t("agentTrace.badge.preview")}</BoundaryBadge>
        </div>
      </section>

      <section className="page-panel">
        <h3>{t("agentTrace.requestTitle")}</h3>
        <button
          type="button"
          onClick={() => void loadTrace()}
          disabled={trace.status === "loading"}
        >
          {trace.status === "loading" ? t("agentTrace.loading") : t("agentTrace.loadNanoparticle")}
        </button>
        <p className="inline-boundary">{t("agentTrace.inlineBoundary")}</p>
      </section>

      <section className="page-panel wide">
        <h3>{t("agentTrace.timelineTitle")}</h3>
        {trace.status === "idle" ? (
          <EmptyState title={t("agentTrace.emptyTitle")} message={t("agentTrace.emptyMessage")} />
        ) : null}
        {trace.status === "loading" ? <LoadingState label={t("agentTrace.loading")} /> : null}
        {trace.status === "demo" ? <ApiDisconnectedNotice message={trace.message} /> : null}
        {trace.status === "error" && trace.error ? (
          <ErrorState message={trace.error.message} actions={trace.error.recommended_next_actions} />
        ) : null}
        {agents.length ? (
          <ol className="agent-trace-list">
            {agents.map((agent) => (
              <li key={agent.agent_name}>
                <div>
                  <h4>{agent.agent_name}</h4>
                  <p>{agent.role}</p>
                  <strong>{agent.output_summary}</strong>
                  <p>{agent.input_summary}</p>
                  <span>{agent.confidence}</span>
                </div>
                <ul>
                  {agent.recommended_next_actions.map((action) => (
                    <li key={action}>{action}</li>
                  ))}
                </ul>
              </li>
            ))}
          </ol>
        ) : null}
      </section>

      <section className="page-panel wide">
        <h3>{t("agentTrace.finalRecommendation")}</h3>
        <p>{trace.data?.final_recommendation || t("agentTrace.noRecommendation")}</p>
      </section>

      <DiagnosticsPanel diagnostics={trace.data?.diagnostics || trace.error?.diagnostics} title={t("agentTrace.diagnostics")} />
      <RecommendedActions actions={trace.data?.recommended_next_actions || trace.error?.recommended_next_actions} title={t("agentTrace.actions")} />
      <JsonPanel title={t("agentTrace.jsonTitle")} value={trace.data || trace.error || { status: trace.status }} />
    </div>
  );
}
