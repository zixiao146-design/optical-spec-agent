import { useEffect, useState } from "react";
import { agentApi } from "../api/client";
import type { ValidationEvidenceItem } from "../api/types";
import { BoundaryBadge } from "../components/BoundaryBadge";
import { EvidencePanel } from "../components/EvidencePanel";

export function EvidencePage() {
  const [evidence, setEvidence] = useState<ValidationEvidenceItem[]>([]);

  useEffect(() => {
    void agentApi.getValidationEvidence().then((payload) => {
      if ("validation_evidence" in payload) setEvidence(payload.validation_evidence);
    });
  }, []);

  return (
    <div className="page-grid">
      <section className="page-panel wide">
        <div className="page-title">
          <span>Validation Evidence</span>
          <h2>Evidence and limitations</h2>
          <p>
            Evidence levels document local readiness signals. They do not imply
            production-grade physical validation or formal convergence proof.
          </p>
        </div>
        <div className="boundary-row">
          <BoundaryBadge>No production-grade physical validation is claimed</BoundaryBadge>
          <BoundaryBadge>Formal convergence proof is not claimed</BoundaryBadge>
        </div>
      </section>
      <section className="page-panel wide">
        <EvidencePanel evidence={evidence} />
      </section>
    </div>
  );
}
