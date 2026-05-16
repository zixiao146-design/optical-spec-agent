import { useState } from "react";
import { agentApi } from "../api/client";
import type { AdapterPreviewResponse } from "../api/types";
import { ArtifactPreviewPanel } from "../components/ArtifactPreviewPanel";
import { BoundaryBadge } from "../components/BoundaryBadge";
import { JsonPanel } from "../components/JsonPanel";

const DEFAULT_SPEC_REQUEST = JSON.stringify(
  { path: "examples/specs/minimal_nanoparticle.json", tool: "gmsh" },
  null,
  2,
);

const TOOLS = ["gmsh", "meep", "mpb", "elmer", "optiland"];

export function ArtifactPreviewPage() {
  const [tool, setTool] = useState("gmsh");
  const [requestText, setRequestText] = useState(DEFAULT_SPEC_REQUEST);
  const [response, setResponse] = useState<AdapterPreviewResponse | undefined>();
  const [rawResponse, setRawResponse] = useState<unknown>();

  async function preview() {
    try {
      const body = JSON.parse(requestText) as { path?: string; spec?: Record<string, unknown> };
      const payload = await agentApi.getAdapterPreview({ ...body, tool });
      setRawResponse(payload);
      if ("preview_content" in payload) setResponse(payload as AdapterPreviewResponse);
    } catch (error) {
      setRawResponse({ status: "error", message: error instanceof Error ? error.message : String(error) });
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
        <label>
          Tool
          <select value={tool} onChange={(event) => setTool(event.target.value)}>
            {TOOLS.map((item) => (
              <option key={item} value={item}>
                {item}
              </option>
            ))}
          </select>
        </label>
        <textarea value={requestText} onChange={(event) => setRequestText(event.target.value)} />
        <button type="button" onClick={() => void preview()}>
          Generate preview
        </button>
      </section>
      <ArtifactPreviewPanel response={response} />
      <JsonPanel title="Preview response" value={rawResponse || { status: "waiting" }} />
    </div>
  );
}
