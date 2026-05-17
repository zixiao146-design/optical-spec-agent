import { useState } from "react";
import { agentApi } from "../api/client";
import { jsonParseError, stateFromPayload, type RemoteState } from "../api/state";
import type { WorkflowPlanResponse } from "../api/types";
import { ApiDisconnectedNotice } from "../components/ApiDisconnectedNotice";
import { BoundaryBadge } from "../components/BoundaryBadge";
import { DemoModeBanner } from "../components/DemoModeBanner";
import { DiagnosticsPanel } from "../components/DiagnosticsPanel";
import { EmptyState } from "../components/EmptyState";
import { ErrorState } from "../components/ErrorState";
import { JsonPanel } from "../components/JsonPanel";
import { LoadingState } from "../components/LoadingState";
import { RecommendedActions } from "../components/RecommendedActions";
import { WorkflowPlanPanel } from "../components/WorkflowPlanPanel";
import {
  demoWorkflowPlan,
  demoWorkflowRequestText,
} from "../fixtures/demoData";
import { useI18n } from "../i18n/useI18n";

export function WorkflowPlanPage() {
  const { t } = useI18n();
  const [requestText, setRequestText] = useState(demoWorkflowRequestText);
  const [fixtureNotice, setFixtureNotice] = useState(t("state.demoLoadedMessage"));
  const [response, setResponse] = useState<RemoteState<WorkflowPlanResponse>>({ status: "idle" });

  function loadWorkflowFixture() {
    setRequestText(demoWorkflowRequestText);
    setFixtureNotice(t("state.demoLoadedMessage"));
    setResponse({ status: "idle" });
  }

  async function generatePlan() {
    setResponse({ status: "loading", message: t("workflow.loadingMessage") });
    try {
      const body = JSON.parse(requestText) as { path?: string; text?: string; tool?: string };
      const payload = await agentApi.getWorkflowPlan(body);
      setResponse(
        stateFromPayload(payload, demoWorkflowPlan, t("workflow.demo")),
      );
    } catch (error) {
      const apiError = jsonParseError(error);
      setResponse({ status: "error", error: apiError, message: apiError.message });
    }
  }

  return (
    <div className="page-grid">
      <section className="page-panel wide">
        <div className="page-title">
          <span>{t("workflow.kicker")}</span>
          <h2>{t("workflow.title")}</h2>
          <p>{t("workflow.description")}</p>
        </div>
        <div className="boundary-row">
          <BoundaryBadge>{t("workflow.badge.noSolver")}</BoundaryBadge>
          <BoundaryBadge>{t("workflow.badge.previewOnly")}</BoundaryBadge>
        </div>
      </section>
      <DemoModeBanner message={fixtureNotice} />
      <section className="page-panel">
        <h3>{t("workflow.requestTitle")}</h3>
        <label htmlFor="workflow-request">{t("workflow.requestLabel")}</label>
        <textarea
          id="workflow-request"
          value={requestText}
          onChange={(event) => setRequestText(event.target.value)}
          aria-describedby="workflow-status"
        />
        <button
          type="button"
          onClick={() => void generatePlan()}
          disabled={response.status === "loading" || requestText.trim().length === 0}
        >
          {response.status === "loading" ? t("workflow.generating") : t("workflow.generateButton")}
        </button>
        <button type="button" className="secondary-button" onClick={loadWorkflowFixture}>
          {t("workflow.loadFixture")}
        </button>
        <p className="inline-boundary">{t("workflow.inlineBoundary")}</p>
        <div id="workflow-status" className="sr-status" aria-live="polite">
          {t("workflow.status")} {response.status}
        </div>
      </section>
      <section className="page-panel">
        <h3>{t("workflow.planSteps")}</h3>
        {response.status === "idle" ? (
          <EmptyState title={t("workflow.emptyTitle")} message={t("workflow.emptyMessage")} />
        ) : null}
        {response.status === "loading" ? <LoadingState label={t("workflow.loading")} /> : null}
        {response.status === "demo" ? <ApiDisconnectedNotice message={response.message} /> : null}
        {response.status === "error" && response.error ? (
          <ErrorState message={response.error.message} actions={response.error.recommended_next_actions} />
        ) : null}
        <WorkflowPlanPanel response={response.data} />
      </section>
      <DiagnosticsPanel diagnostics={response.data?.diagnostics || response.error?.diagnostics} title={t("workflow.diagnostics")} />
      <RecommendedActions actions={response.data?.recommended_next_actions || response.error?.recommended_next_actions} title={t("workflow.actions")} />
      <JsonPanel title={t("workflow.jsonTitle")} value={response.data || response.error || { status: response.status }} />
    </div>
  );
}
