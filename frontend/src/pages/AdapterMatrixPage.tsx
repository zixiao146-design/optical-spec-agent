import { useEffect, useState } from "react";
import { agentApi } from "../api/client";
import type { AdapterSummary, ValidationEvidenceItem } from "../api/types";
import { AdapterMatrix } from "../components/AdapterMatrix";
import { BoundaryBadge } from "../components/BoundaryBadge";

export function AdapterMatrixPage() {
  const [adapters, setAdapters] = useState<AdapterSummary[]>([]);
  const [evidence, setEvidence] = useState<ValidationEvidenceItem[]>([]);

  useEffect(() => {
    void agentApi.getAdapters().then((payload) => {
      if ("adapters" in payload) setAdapters(payload.adapters);
    });
    void agentApi.getValidationEvidence().then((payload) => {
      if ("validation_evidence" in payload) setEvidence(payload.validation_evidence);
    });
  }, []);

  return (
    <div className="page-grid">
      <section className="page-panel wide">
        <div className="page-title">
          <span>Adapter Matrix</span>
          <h2>Adapter maturity and evidence</h2>
          <p>
            The matrix shows registry metadata and validation evidence without
            running external solvers.
          </p>
        </div>
        <div className="boundary-row">
          <BoundaryBadge>No solver was executed</BoundaryBadge>
          <BoundaryBadge tone="notice">Elmer Level 3 remains deferred</BoundaryBadge>
        </div>
      </section>
      <section className="page-panel wide">
        <AdapterMatrix adapters={adapters} evidence={evidence} />
      </section>
    </div>
  );
}
