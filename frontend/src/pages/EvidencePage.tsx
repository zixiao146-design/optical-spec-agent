import { useEffect, useState } from "react";
import { agentApi } from "../api/client";
import { INITIAL_LOADING_STATE, stateFromPayload, type RemoteState } from "../api/state";
import type { ValidationEvidenceResponse } from "../api/types";
import { ApiDisconnectedNotice } from "../components/ApiDisconnectedNotice";
import { BoundaryBadge } from "../components/BoundaryBadge";
import { EmptyState } from "../components/EmptyState";
import { ErrorState } from "../components/ErrorState";
import { EvidencePanel } from "../components/EvidencePanel";
import { LoadingState } from "../components/LoadingState";
import { demoEvidence } from "../fixtures/demoData";

export function EvidencePage() {
  const [evidence, setEvidence] = useState<RemoteState<ValidationEvidenceResponse>>(INITIAL_LOADING_STATE);

  useEffect(() => {
    let active = true;
    void agentApi.getValidationEvidence().then((payload) => {
      if (active) setEvidence(stateFromPayload(payload, demoEvidence, "Demo validation evidence shown; this is not live evidence retrieval."));
    });
    return () => {
      active = false;
    };
  }, []);

  const rows = evidence.data?.validation_evidence || [];

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
        {evidence.status === "loading" ? <LoadingState label="Loading validation evidence..." /> : null}
        {evidence.status === "demo" ? <ApiDisconnectedNotice message={evidence.message} /> : null}
        {evidence.status === "error" && evidence.error ? (
          <ErrorState message={evidence.error.message} actions={evidence.error.recommended_next_actions} />
        ) : null}
        {evidence.status !== "loading" && rows.length === 0 && !evidence.error ? (
          <EmptyState title="No validation evidence loaded" message="Start the local API or use demo fixture mode." />
        ) : null}
        {rows.length > 0 ? <EvidencePanel evidence={rows} /> : null}
      </section>
    </div>
  );
}
