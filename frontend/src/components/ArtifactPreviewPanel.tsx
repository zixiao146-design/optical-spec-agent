import type { AdapterPreviewResponse } from "../api/types";
import { BoundaryBadge } from "./BoundaryBadge";

interface ArtifactPreviewPanelProps {
  response?: AdapterPreviewResponse;
}

export function ArtifactPreviewPanel({ response }: ArtifactPreviewPanelProps) {
  if (!response) {
    return <p className="muted">Generate a preview artifact to inspect local scaffold content.</p>;
  }
  return (
    <section className="artifact-preview">
      <div className="boundary-row">
        <BoundaryBadge>Preview artifact only</BoundaryBadge>
        <BoundaryBadge>No solver was executed</BoundaryBadge>
      </div>
      <div className="artifact-meta">
        <span>{response.tool}</span>
        <span>{response.output_language}</span>
        <span>{response.output_extension}</span>
      </div>
      <pre>{response.preview_content || JSON.stringify(response.artifact_summary, null, 2)}</pre>
    </section>
  );
}
