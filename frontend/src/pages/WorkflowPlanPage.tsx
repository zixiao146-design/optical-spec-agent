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
  DEMO_FIXTURE_LOADED_MESSAGE,
  demoWorkflowPlan,
  demoWorkflowRequestText,
} from "../fixtures/demoData";

export function WorkflowPlanPage() {
  const [requestText, setRequestText] = useState(demoWorkflowRequestText);
  const [fixtureNotice, setFixtureNotice] = useState(DEMO_FIXTURE_LOADED_MESSAGE);
  const [response, setResponse] = useState<RemoteState<WorkflowPlanResponse>>({ status: "idle" });

  function loadWorkflowFixture() {
    setRequestText(demoWorkflowRequestText);
    setFixtureNotice(DEMO_FIXTURE_LOADED_MESSAGE);
    setResponse({ status: "idle" });
  }

  async function generatePlan() {
    setResponse({ status: "loading", message: "Generating local workflow preview." });
    try {
      const body = JSON.parse(requestText) as { path?: string; text?: string; tool?: string };
      const payload = await agentApi.getWorkflowPlan(body);
      setResponse(
        stateFromPayload(payload, demoWorkflowPlan, "Demo workflow fixture shown; this is not live workflow planning."),
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
          <span>Workflow Plan</span>
          <h2>Generate a synchronous local workflow preview</h2>
          <p>Workflow planning is preview-first and keeps solver execution disabled.</p>
        </div>
        <div className="boundary-row">
          <BoundaryBadge>No solver was executed</BoundaryBadge>
          <BoundaryBadge>Preview plan only</BoundaryBadge>
        </div>
      </section>
      <DemoModeBanner message={fixtureNotice} />
      <section className="page-panel">
        <h3>Workflow request</h3>
        <label htmlFor="workflow-request">Workflow request JSON</label>
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
          {response.status === "loading" ? "Generating..." : "Generate workflow plan"}
        </button>
        <button type="button" className="secondary-button" onClick={loadWorkflowFixture}>
          Load workflow fixture
        </button>
        <p className="inline-boundary">No solver is executed by default.</p>
        <div id="workflow-status" className="sr-status" aria-live="polite">
          Workflow status: {response.status}
        </div>
      </section>
      <section className="page-panel">
        <h3>Plan steps</h3>
        {response.status === "idle" ? (
          <EmptyState title="No workflow plan yet" message="Use the fixture request to generate a local preview." />
        ) : null}
        {response.status === "loading" ? <LoadingState label="Generating workflow preview..." /> : null}
        {response.status === "demo" ? <ApiDisconnectedNotice message={response.message} /> : null}
        {response.status === "error" && response.error ? (
          <ErrorState message={response.error.message} actions={response.error.recommended_next_actions} />
        ) : null}
        <WorkflowPlanPanel response={response.data} />
      </section>
      <DiagnosticsPanel diagnostics={response.data?.diagnostics || response.error?.diagnostics} title="Workflow diagnostics" />
      <RecommendedActions actions={response.data?.recommended_next_actions || response.error?.recommended_next_actions} title="Workflow recommended next actions" />
      <JsonPanel title="Workflow Plan" value={response.data || response.error || { status: response.status }} />
    </div>
  );
}
