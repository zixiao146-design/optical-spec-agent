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
import { useI18n } from "../i18n/useI18n";

export function EvidencePage() {
  const { t } = useI18n();
  const [evidence, setEvidence] = useState<RemoteState<ValidationEvidenceResponse>>(INITIAL_LOADING_STATE);

  useEffect(() => {
    let active = true;
    void agentApi.getValidationEvidence().then((payload) => {
      if (active) setEvidence(stateFromPayload(payload, demoEvidence, t("evidence.demo")));
    });
    return () => {
      active = false;
    };
  }, [t]);

  const rows = evidence.data?.validation_evidence || [];

  return (
    <div className="page-grid">
      <section className="page-panel wide">
        <div className="page-title">
          <span>{t("evidence.kicker")}</span>
          <h2>{t("evidence.title")}</h2>
          <p>
            {t("evidence.description")}
          </p>
        </div>
        <div className="boundary-row">
          <BoundaryBadge>{t("evidence.badge.noProduction")}</BoundaryBadge>
          <BoundaryBadge>{t("evidence.badge.noConvergence")}</BoundaryBadge>
        </div>
      </section>
      <section className="page-panel wide">
        {evidence.status === "loading" ? <LoadingState label={t("evidence.loading")} /> : null}
        {evidence.status === "demo" ? <ApiDisconnectedNotice message={evidence.message} /> : null}
        {evidence.status === "error" && evidence.error ? (
          <ErrorState message={evidence.error.message} actions={evidence.error.recommended_next_actions} />
        ) : null}
        {evidence.status !== "loading" && rows.length === 0 && !evidence.error ? (
          <EmptyState title={t("evidence.emptyTitle")} message={t("evidence.emptyMessage")} />
        ) : null}
        {rows.length > 0 ? <EvidencePanel evidence={rows} /> : null}
      </section>
    </div>
  );
}
