import { useEffect, useMemo, useState } from "react";
import { agentApi } from "../api/client";
import { INITIAL_LOADING_STATE, stateFromPayload, type RemoteState } from "../api/state";
import type { AgentTaskSessionResponse, ExamplesResponse } from "../api/types";
import { AgentArtifactPanel } from "../components/AgentArtifactPanel";
import { AgentPlanPanel } from "../components/AgentPlanPanel";
import { AgentTaskSummary } from "../components/AgentTaskSummary";
import { ApiDisconnectedNotice } from "../components/ApiDisconnectedNotice";
import { BoundaryBadge } from "../components/BoundaryBadge";
import { DiagnosticsPanel } from "../components/DiagnosticsPanel";
import { ErrorState } from "../components/ErrorState";
import { JsonPanel } from "../components/JsonPanel";
import { LoadingState } from "../components/LoadingState";
import { PermissionGatePanel } from "../components/PermissionGatePanel";
import { RecommendedActions } from "../components/RecommendedActions";
import { demoAgentSession, demoChineseNaturalLanguageSpec, demoExamples, demoNaturalLanguageSpec } from "../fixtures/demoData";
import { useI18n } from "../i18n/useI18n";

export function AgentCommandCenterPage() {
  const { language, t } = useI18n();
  const [goal, setGoal] = useState(
    language === "zh-CN" ? demoChineseNaturalLanguageSpec : demoNaturalLanguageSpec,
  );
  const [selectedExampleId, setSelectedExampleId] = useState("nanoparticle_plasmonics");
  const [examples, setExamples] = useState<RemoteState<ExamplesResponse>>(INITIAL_LOADING_STATE);
  const [session, setSession] = useState<RemoteState<AgentTaskSessionResponse>>({ status: "idle" });

  useEffect(() => {
    let active = true;
    void agentApi.getExamples().then((payload) => {
      if (active) setExamples(stateFromPayload(payload, demoExamples, t("examples.demo")));
    });
    return () => {
      active = false;
    };
  }, [t]);

  const exampleRows = useMemo(() => {
    const liveRows = Array.isArray(examples.data?.examples) ? examples.data.examples : [];
    return liveRows.length ? liveRows : demoExamples.examples;
  }, [examples.data?.examples]);

  async function startTask() {
    setSession({ status: "loading", message: t("commandCenter.loading") });
    const payload = await agentApi.getAgentSession({
      goal,
      example_id: selectedExampleId || undefined,
      language,
    });
    setSession(stateFromPayload(payload, demoAgentSession, t("commandCenter.demo")));
  }

  const task = session.data;

  return (
    <div className="page-grid">
      <section className="page-panel wide command-hero">
        <div className="page-title">
          <span>{t("commandCenter.kicker")}</span>
          <h2>{t("commandCenter.title")}</h2>
          <p>{t("commandCenter.subtitle")}</p>
        </div>
        <div className="boundary-row">
          <BoundaryBadge>{t("commandCenter.badge.local")}</BoundaryBadge>
          <BoundaryBadge>{t("commandCenter.badge.noSolver")}</BoundaryBadge>
          <BoundaryBadge>{t("commandCenter.badge.noLlm")}</BoundaryBadge>
          <BoundaryBadge tone="notice">{t("commandCenter.badge.noRelease")}</BoundaryBadge>
        </div>
      </section>

      <section className="page-panel wide">
        <h3>{t("commandCenter.goalTitle")}</h3>
        <label htmlFor="agent-command-goal">{t("commandCenter.goalLabel")}</label>
        <textarea
          id="agent-command-goal"
          rows={7}
          value={goal}
          onChange={(event) => setGoal(event.target.value)}
          placeholder={t("commandCenter.goalPlaceholder")}
        />
        <label htmlFor="agent-command-example">{t("commandCenter.exampleLabel")}</label>
        <select
          id="agent-command-example"
          value={selectedExampleId}
          onChange={(event) => setSelectedExampleId(event.target.value)}
        >
          <option value="">{t("commandCenter.autoSelectExample")}</option>
          {exampleRows.map((example) => (
            <option value={example.example_id} key={example.example_id}>
              {language === "zh-CN" ? example.title_zh : example.title}
            </option>
          ))}
        </select>
        <button
          type="button"
          onClick={() => void startTask()}
          disabled={session.status === "loading"}
        >
          {session.status === "loading" ? t("commandCenter.loadingShort") : t("commandCenter.startTask")}
        </button>
        <p className="inline-boundary">{t("commandCenter.formBoundary")}</p>
      </section>

      {session.status === "loading" ? <LoadingState label={t("commandCenter.loading")} /> : null}
      {session.status === "demo" ? <ApiDisconnectedNotice message={session.message} /> : null}
      {session.status === "error" && session.error ? (
        <ErrorState message={session.error.message} actions={session.error.recommended_next_actions} />
      ) : null}

      <AgentTaskSummary session={task} />
      <AgentPlanPanel steps={task?.plan_steps || []} />

      <section className="page-panel wide">
        <h3>{t("commandCenter.subAgentTrace")}</h3>
        <p className="inline-boundary">{task?.agent_trace.timeline_summary || t("commandCenter.traceIntro")}</p>
        {task?.agent_trace.agents.length ? (
          <ol className="agent-trace-list">
            {task.agent_trace.agents.map((agent) => (
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
                  <p>{agent.output_summary}</p>
                  <dl className="timeline-details">
                    <dt>{t("agentTrace.inputSummary")}</dt>
                    <dd>{agent.input_summary}</dd>
                    <dt>{t("agentTrace.diagnosticsLabel")}</dt>
                    <dd>{agent.diagnostics.length ? agent.diagnostics.join(" ") : t("state.diagnostics.empty")}</dd>
                    <dt>{t("agentTrace.nextActionsLabel")}</dt>
                    <dd>{agent.recommended_next_actions.join(" ")}</dd>
                  </dl>
                </div>
              </li>
            ))}
          </ol>
        ) : (
          <p>{t("commandCenter.traceEmpty")}</p>
        )}
      </section>

      <PermissionGatePanel gates={task?.permission_gates || []} />
      <AgentArtifactPanel artifacts={task?.artifacts || []} />
      <RecommendedActions actions={task?.recommended_next_actions || session.error?.recommended_next_actions} title={t("commandCenter.nextActions")} />
      <DiagnosticsPanel diagnostics={task?.diagnostics || session.error?.diagnostics} title={t("commandCenter.diagnostics")} />
      <JsonPanel title={t("commandCenter.rawJson")} value={task || session.error || { status: session.status }} />
    </div>
  );
}
