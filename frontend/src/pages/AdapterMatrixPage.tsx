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
import { useI18n } from "../i18n/useI18n";

export function AdapterMatrixPage() {
  const { t } = useI18n();
  const [adapters, setAdapters] = useState<RemoteState<AdaptersResponse>>(INITIAL_LOADING_STATE);
  const [evidence, setEvidence] = useState<RemoteState<ValidationEvidenceResponse>>(INITIAL_LOADING_STATE);

  useEffect(() => {
    let active = true;
    void agentApi.getAdapters().then((payload) => {
      if (active) setAdapters(stateFromPayload(payload, demoAdapters, t("adapters.demoAdapters")));
    });
    void agentApi.getValidationEvidence().then((payload) => {
      if (active) setEvidence(stateFromPayload(payload, demoEvidence, t("adapters.demoEvidence")));
    });
    return () => {
      active = false;
    };
  }, [t]);

  const isLoading = adapters.status === "loading" || evidence.status === "loading";
  const demoMessage = [adapters, evidence].find((item) => item.status === "demo")?.message;
  const error = [adapters, evidence].find((item) => item.status === "error")?.error;
  const adapterRows = adapters.data?.adapters || [];
  const evidenceRows = evidence.data?.validation_evidence || [];

  return (
    <div className="page-grid">
      <section className="page-panel wide">
        <div className="page-title">
          <span>{t("adapters.kicker")}</span>
          <h2>{t("adapters.title")}</h2>
          <p>
            {t("adapters.description")}
          </p>
        </div>
        <div className="boundary-row">
          <BoundaryBadge>{t("adapters.badge.noSolver")}</BoundaryBadge>
          <BoundaryBadge tone="notice">{t("adapters.badge.elmerDeferred")}</BoundaryBadge>
        </div>
      </section>
      <section className="page-panel wide">
        {isLoading ? <LoadingState label={t("adapters.loading")} /> : null}
        {demoMessage ? <ApiDisconnectedNotice message={demoMessage} /> : null}
        {error ? <ErrorState message={error.message} actions={error.recommended_next_actions} /> : null}
        {!isLoading && adapterRows.length === 0 && !error ? (
          <EmptyState title={t("adapters.noAdaptersTitle")} message={t("adapters.noAdaptersMessage")} />
        ) : null}
        {adapterRows.length > 0 ? <AdapterMatrix adapters={adapterRows} evidence={evidenceRows} /> : null}
      </section>
    </div>
  );
}
