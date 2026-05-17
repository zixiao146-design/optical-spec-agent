import type { AgentArtifact } from "../api/types";
import { useI18n } from "../i18n/useI18n";
import { BoundaryBadge } from "./BoundaryBadge";
import { EmptyState } from "./EmptyState";

interface AgentArtifactPanelProps {
  artifacts: AgentArtifact[];
}

export function AgentArtifactPanel({ artifacts }: AgentArtifactPanelProps) {
  const { language, t } = useI18n();

  return (
    <section className="page-panel wide">
      <h3>{t("commandCenter.artifacts")}</h3>
      {artifacts.length === 0 ? (
        <EmptyState title={t("commandCenter.noArtifactsTitle")} message={t("commandCenter.noArtifactsMessage")} />
      ) : (
        <div className="artifact-grid">
          {artifacts.map((artifact) => (
            <article className="artifact-card" key={artifact.artifact_id}>
              <div className="timeline-heading">
                <h4>{language === "zh-CN" ? artifact.label_zh : artifact.label}</h4>
                <BoundaryBadge tone={artifact.production_grade ? "notice" : "safe"}>
                  {artifact.production_grade ? t("commandCenter.productionGrade") : t("commandCenter.previewOnly")}
                </BoundaryBadge>
              </div>
              <p>{artifact.summary}</p>
              <dl className="timeline-details">
                <dt>{t("commandCenter.artifactType")}</dt>
                <dd>{artifact.artifact_type}</dd>
                <dt>{t("commandCenter.sourceEndpoint")}</dt>
                <dd>{artifact.source_endpoint}</dd>
                <dt>{t("commandCenter.generatedBy")}</dt>
                <dd>{artifact.generated_by_agent}</dd>
              </dl>
              {artifact.preview_content ? <code>{artifact.preview_content}</code> : null}
            </article>
          ))}
        </div>
      )}
    </section>
  );
}
