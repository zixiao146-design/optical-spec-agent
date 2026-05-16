import type { ValidationEvidenceItem } from "../api/types";
import { BoundaryBadge } from "./BoundaryBadge";

interface EvidencePanelProps {
  evidence: ValidationEvidenceItem[];
}

export function EvidencePanel({ evidence }: EvidencePanelProps) {
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
            <BoundaryBadge>No production claim</BoundaryBadge>
          </div>
        </article>
      ))}
    </div>
  );
}
