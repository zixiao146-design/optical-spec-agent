import type { ValidationEvidenceItem } from "../api/types";
import { useI18n } from "../i18n/useI18n";
import { BoundaryBadge } from "./BoundaryBadge";

interface EvidencePanelProps {
  evidence: ValidationEvidenceItem[];
}

export function EvidencePanel({ evidence }: EvidencePanelProps) {
  const { t } = useI18n();
  return (
    <div className="evidence-list">
      {evidence.map((item) => (
        <article className="evidence-row" key={item.tool_name}>
          <div>
            <h3>{item.display_name}</h3>
            <p>{item.status_note}</p>
            {item.evidence ? <code>{item.evidence}</code> : null}
          </div>
          <div className="evidence-badges">
            <BoundaryBadge tone={item.tool_name === "elmer" ? "notice" : "safe"}>
              {item.maturity_level}
            </BoundaryBadge>
            <BoundaryBadge>{t("evidence.noProductionClaim")}</BoundaryBadge>
          </div>
        </article>
      ))}
    </div>
  );
}
