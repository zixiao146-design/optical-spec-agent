import { useEffect, useState } from "react";
import { agentApi } from "../api/client";
import { INITIAL_LOADING_STATE, stateFromPayload, type RemoteState } from "../api/state";
import type { AdaptersResponse, ValidationEvidenceResponse } from "../api/types";
import { AdapterMatrix } from "../components/AdapterMatrix";
import { ApiDisconnectedNotice } from "../components/ApiDisconnectedNotice";
import { BoundaryBadge } from "../components/BoundaryBadge";
import { EmptyState } from "../components/EmptyState";
import { ErrorState } from "../components/ErrorState";
import { LoadingState } from "../components/LoadingState";
import { demoAdapters, demoEvidence } from "../fixtures/demoData";

export function AdapterMatrixPage() {
  const [adapters, setAdapters] = useState<RemoteState<AdaptersResponse>>(INITIAL_LOADING_STATE);
  const [evidence, setEvidence] = useState<RemoteState<ValidationEvidenceResponse>>(INITIAL_LOADING_STATE);

  useEffect(() => {
    let active = true;
    void agentApi.getAdapters().then((payload) => {
      if (active) setAdapters(stateFromPayload(payload, demoAdapters, "Demo adapter fixture shown; this is not live registry data."));
    });
    void agentApi.getValidationEvidence().then((payload) => {
      if (active) setEvidence(stateFromPayload(payload, demoEvidence, "Demo evidence fixture shown; this is not live evidence data."));
    });
    return () => {
      active = false;
    };
  }, []);

  const isLoading = adapters.status === "loading" || evidence.status === "loading";
  const demoMessage = [adapters, evidence].find((item) => item.status === "demo")?.message;
  const error = [adapters, evidence].find((item) => item.status === "error")?.error;
  const adapterRows = adapters.data?.adapters || [];
  const evidenceRows = evidence.data?.validation_evidence || [];

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
        {isLoading ? <LoadingState label="Loading adapter matrix from the local API..." /> : null}
        {demoMessage ? <ApiDisconnectedNotice message={demoMessage} /> : null}
        {error ? <ErrorState message={error.message} actions={error.recommended_next_actions} /> : null}
        {!isLoading && adapterRows.length === 0 && !error ? (
          <EmptyState title="No adapters available" message="Start the local API or use demo fixture mode." />
        ) : null}
        {adapterRows.length > 0 ? <AdapterMatrix adapters={adapterRows} evidence={evidenceRows} /> : null}
      </section>
    </div>
  );
}
