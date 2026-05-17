import { useEffect, useState } from "react";
import { agentApi } from "../api/client";
import { INITIAL_LOADING_STATE, stateFromPayload, type RemoteState } from "../api/state";
import type { AgentTraceResponse, ExamplesResponse } from "../api/types";
import { ApiDisconnectedNotice } from "../components/ApiDisconnectedNotice";
import { BoundaryBadge } from "../components/BoundaryBadge";
import { DiagnosticsPanel } from "../components/DiagnosticsPanel";
import { EmptyState } from "../components/EmptyState";
import { ErrorState } from "../components/ErrorState";
import { JsonPanel } from "../components/JsonPanel";
import { LoadingState } from "../components/LoadingState";
import { RecommendedActions } from "../components/RecommendedActions";
import { demoAgentTrace, demoExamples } from "../fixtures/demoData";
import { useI18n } from "../i18n/useI18n";

export function AgentCollaborationPage() {
  const { language, t } = useI18n();
  const [examples, setExamples] = useState<RemoteState<ExamplesResponse>>(INITIAL_LOADING_STATE);
  const [selectedExampleId, setSelectedExampleId] = useState("nanoparticle_plasmonics");
  const [trace, setTrace] = useState<RemoteState<AgentTraceResponse>>({ status: "idle" });

  useEffect(() => {
    let active = true;
    void agentApi.getExamples().then((payload) => {
      if (active) setExamples(stateFromPayload(payload, demoExamples, t("examples.demo")));
    });
    return () => {
      active = false;
    };
  }, [t]);

  async function loadTrace() {
    setTrace({ status: "loading", message: t("agentTrace.loadingMessage") });
    const payload = await agentApi.getExampleAgentTrace(selectedExampleId);
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
        <label htmlFor="agent-trace-example">{t("agentTrace.exampleSelector")}</label>
        <select
          id="agent-trace-example"
          value={selectedExampleId}
          onChange={(event) => setSelectedExampleId(event.target.value)}
        >
          {(examples.data?.examples || demoExamples.examples).map((example) => (
            <option value={example.example_id} key={example.example_id}>
              {language === "zh-CN" ? example.title_zh : example.title}
            </option>
          ))}
        </select>
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
        <p className="inline-boundary">{trace.data?.timeline_summary || t("agentTrace.timelineSummary")}</p>
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
              <li key={`${agent.step_index}-${agent.agent_name}`} className="timeline-step">
                <div className="timeline-marker">{agent.step_index}</div>
                <div className="timeline-content">
                  <div className="timeline-heading">
                    <h4>{agent.agent_name}</h4>
                    <span>{agent.stage}</span>
                    <BoundaryBadge tone={agent.status === "ok" ? "safe" : "notice"}>
                      {agent.confidence}
                    </BoundaryBadge>
                  </div>
                  <p>{agent.role}</p>
                  <dl className="timeline-details">
                    <dt>{t("agentTrace.inputSummary")}</dt>
                    <dd>{agent.input_summary}</dd>
                    <dt>{t("agentTrace.outputSummary")}</dt>
                    <dd>{agent.output_summary}</dd>
                    <dt>{t("agentTrace.diagnosticsLabel")}</dt>
                    <dd>{agent.diagnostics.length ? agent.diagnostics.join(" ") : t("state.diagnostics.empty")}</dd>
                    <dt>{t("agentTrace.evidenceRefs")}</dt>
                    <dd>{agent.evidence_refs.length ? agent.evidence_refs.join(", ") : t("agentTrace.noEvidenceRefs")}</dd>
                    <dt>{t("agentTrace.safetyNotes")}</dt>
                    <dd>{agent.safety_notes.length ? agent.safety_notes.join(" ") : t("agentTrace.defaultSafetyNote")}</dd>
                  </dl>
                  <strong>{t("agentTrace.nextActionsLabel")}</strong>
                  <ul>
                    {agent.recommended_next_actions.map((action) => (
                      <li key={action}>{action}</li>
                    ))}
                  </ul>
                </div>
              </li>
            ))}
          </ol>
        ) : null}
      </section>

      <section className="page-panel wide">
        <h3>{t("agentTrace.finalRecommendation")}</h3>
        <p><strong>{t("agentTrace.materialSuggestions")}:</strong> {(trace.data?.material_suggestions || []).join(", ") || t("agentTrace.none")}</p>
        <p><strong>{t("agentTrace.adapterRecommendation")}:</strong> {trace.data?.adapter_recommendation || t("agentTrace.none")}</p>
        <p>{trace.data?.final_recommendation || t("agentTrace.noRecommendation")}</p>
      </section>

      <DiagnosticsPanel diagnostics={trace.data?.diagnostics || trace.error?.diagnostics} title={t("agentTrace.diagnostics")} />
      <RecommendedActions actions={trace.data?.recommended_next_actions || trace.error?.recommended_next_actions} title={t("agentTrace.actions")} />
      <JsonPanel title={t("agentTrace.jsonTitle")} value={trace.data || trace.error || { status: trace.status }} />
    </div>
  );
}
