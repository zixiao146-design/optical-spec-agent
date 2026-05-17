import type { AdapterPreviewResponse } from "../api/types";
import { useI18n } from "../i18n/useI18n";
import { BoundaryBadge } from "./BoundaryBadge";

interface ArtifactPreviewPanelProps {
  response?: AdapterPreviewResponse;
}

export function ArtifactPreviewPanel({ response }: ArtifactPreviewPanelProps) {
  const { t } = useI18n();
  if (!response) {
    return <p className="muted">{t("preview.panelEmpty")}</p>;
  }
  return (
    <section className="artifact-preview">
      <div className="boundary-row">
        <BoundaryBadge>{t("preview.badge.previewOnly")}</BoundaryBadge>
        <BoundaryBadge>{t("preview.badge.noSolver")}</BoundaryBadge>
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
