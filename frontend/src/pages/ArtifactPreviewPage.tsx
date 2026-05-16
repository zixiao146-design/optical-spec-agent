import { useState } from "react";
import { agentApi } from "../api/client";
import { jsonParseError, stateFromPayload, type RemoteState } from "../api/state";
import type { AdapterPreviewResponse } from "../api/types";
import { ApiDisconnectedNotice } from "../components/ApiDisconnectedNotice";
import { ArtifactPreviewPanel } from "../components/ArtifactPreviewPanel";
import { BoundaryBadge } from "../components/BoundaryBadge";
import { EmptyState } from "../components/EmptyState";
import { ErrorState } from "../components/ErrorState";
import { JsonPanel } from "../components/JsonPanel";
import { LoadingState } from "../components/LoadingState";
import { demoAdapterPreview } from "../fixtures/demoData";

const DEFAULT_SPEC_REQUEST = JSON.stringify(
  { path: "examples/specs/minimal_nanoparticle.json", tool: "gmsh" },
  null,
  2,
);

const TOOLS = ["gmsh", "meep", "mpb", "elmer", "optiland"];

export function ArtifactPreviewPage() {
  const [tool, setTool] = useState("gmsh");
  const [requestText, setRequestText] = useState(DEFAULT_SPEC_REQUEST);
  const [response, setResponse] = useState<RemoteState<AdapterPreviewResponse>>({ status: "idle" });

  async function preview() {
    setResponse({ status: "loading", message: "Generating local preview artifact." });
    try {
      const body = JSON.parse(requestText) as { path?: string; spec?: Record<string, unknown> };
      const payload = await agentApi.getAdapterPreview({ ...body, tool });
      setResponse(
        stateFromPayload(payload, demoAdapterPreview, "Demo adapter preview fixture shown; this is not live preview generation."),
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
          <span>Artifact Preview</span>
          <h2>Generate solver-native preview content</h2>
          <p>
            Preview generation produces local scaffold content only. It never runs
            the selected solver by default.
          </p>
        </div>
        <div className="boundary-row">
          <BoundaryBadge>Preview artifact only</BoundaryBadge>
          <BoundaryBadge>No solver was executed</BoundaryBadge>
        </div>
      </section>
      <section className="page-panel">
        <h3>Preview request</h3>
        <label htmlFor="adapter-tool">
          Tool
        </label>
        <select id="adapter-tool" value={tool} onChange={(event) => setTool(event.target.value)}>
          {TOOLS.map((item) => (
            <option key={item} value={item}>
              {item}
            </option>
          ))}
        </select>
        <label htmlFor="adapter-preview-request">Adapter preview request JSON</label>
        <textarea
          id="adapter-preview-request"
          value={requestText}
          onChange={(event) => setRequestText(event.target.value)}
          aria-describedby="adapter-preview-status"
        />
        <button
          type="button"
          onClick={() => void preview()}
          disabled={response.status === "loading" || requestText.trim().length === 0}
        >
          {response.status === "loading" ? "Generating..." : "Generate preview"}
        </button>
        <div id="adapter-preview-status" className="sr-status" aria-live="polite">
          Adapter preview status: {response.status}
        </div>
      </section>
      <section className="page-panel">
        <h3>Preview state</h3>
        {response.status === "idle" ? (
          <EmptyState title="No preview generated yet" message="Choose a tool and generate a local preview." />
        ) : null}
        {response.status === "loading" ? <LoadingState label="Generating preview artifact..." /> : null}
        {response.status === "demo" ? <ApiDisconnectedNotice message={response.message} /> : null}
        {response.status === "error" && response.error ? (
          <ErrorState message={response.error.message} actions={response.error.recommended_next_actions} />
        ) : null}
      </section>
      <ArtifactPreviewPanel response={response.data} />
      <JsonPanel title="Preview response" value={response.data || response.error || { status: response.status }} />
    </div>
  );
}
