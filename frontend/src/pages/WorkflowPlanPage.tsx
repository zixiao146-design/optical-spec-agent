import { useState } from "react";
import { agentApi } from "../api/client";
import type { WorkflowPlanResponse } from "../api/types";
import { BoundaryBadge } from "../components/BoundaryBadge";
import { JsonPanel } from "../components/JsonPanel";
import { WorkflowPlanPanel } from "../components/WorkflowPlanPanel";

const DEFAULT_REQUEST = JSON.stringify(
  { path: "examples/workflows/local_preview_request.json" },
  null,
  2,
);

export function WorkflowPlanPage() {
  const [requestText, setRequestText] = useState(DEFAULT_REQUEST);
  const [response, setResponse] = useState<WorkflowPlanResponse | undefined>();
  const [rawResponse, setRawResponse] = useState<unknown>();

  async function generatePlan() {
    try {
      const body = JSON.parse(requestText) as { path?: string; text?: string; tool?: string };
      const payload = await agentApi.getWorkflowPlan(body);
      setRawResponse(payload);
      if ("workflow_plan" in payload) setResponse(payload as WorkflowPlanResponse);
    } catch (error) {
      setRawResponse({ status: "error", message: error instanceof Error ? error.message : String(error) });
    }
  }

  return (
    <div className="page-grid">
      <section className="page-panel wide">
        <div className="page-title">
          <span>Workflow Plan</span>
          <h2>Generate a synchronous local workflow preview</h2>
          <p>Workflow planning is preview-first and does not execute solvers.</p>
        </div>
        <div className="boundary-row">
          <BoundaryBadge>No solver was executed</BoundaryBadge>
          <BoundaryBadge>Preview plan only</BoundaryBadge>
        </div>
      </section>
      <section className="page-panel">
        <h3>Workflow request</h3>
        <textarea value={requestText} onChange={(event) => setRequestText(event.target.value)} />
        <button type="button" onClick={() => void generatePlan()}>
          Generate workflow plan
        </button>
      </section>
      <section className="page-panel">
        <h3>Plan steps</h3>
        <WorkflowPlanPanel response={response} />
      </section>
      <JsonPanel title="Workflow response" value={rawResponse || { status: "waiting" }} />
    </div>
  );
}
