import { useEffect, useState } from "react";
import { agentApi } from "../api/client";
import { INITIAL_LOADING_STATE, stateFromPayload, type RemoteState } from "../api/state";
import type { HealthResponse, ReadinessResponse, VersionResponse } from "../api/types";
import { ApiDisconnectedNotice } from "../components/ApiDisconnectedNotice";
import { ApiModeIndicator } from "../components/ApiModeIndicator";
import { BoundaryBadge } from "../components/BoundaryBadge";
import { ChineseGuidedTutorial } from "../components/ChineseGuidedTutorial";
import { ErrorState } from "../components/ErrorState";
import { GuidedDemoStepper } from "../components/GuidedDemoStepper";
import { JsonPanel } from "../components/JsonPanel";
import { LoadingState } from "../components/LoadingState";
import { QuickstartPanel } from "../components/QuickstartPanel";
import { RecommendedActions } from "../components/RecommendedActions";
import { StatusCard } from "../components/StatusCard";
import { demoHealth, demoReadiness, demoVersion } from "../fixtures/demoData";
import { useI18n } from "../i18n/useI18n";

interface DashboardPageProps {
  onNavigate?: (page: "Dashboard" | "Spec Input" | "Adapter Matrix" | "Workflow Plan" | "Artifact Preview" | "Validation Evidence" | "System Status") => void;
}

export function DashboardPage({ onNavigate }: DashboardPageProps) {
  const { t } = useI18n();
  const [health, setHealth] = useState<RemoteState<HealthResponse>>(INITIAL_LOADING_STATE);
  const [version, setVersion] = useState<RemoteState<VersionResponse>>(INITIAL_LOADING_STATE);
  const [readiness, setReadiness] = useState<RemoteState<ReadinessResponse>>(INITIAL_LOADING_STATE);

  useEffect(() => {
    let active = true;
    void agentApi.getHealth().then((payload) => {
      if (active) setHealth(stateFromPayload(payload, demoHealth, t("dashboard.healthDemo")));
    });
    void agentApi.getVersion().then((payload) => {
      if (active) setVersion(stateFromPayload(payload, demoVersion, t("dashboard.versionDemo")));
    });
    void agentApi.getReadiness().then((payload) => {
      if (active) setReadiness(stateFromPayload(payload, demoReadiness, t("dashboard.readinessDemo")));
    });
    return () => {
      active = false;
    };
  }, [t]);

  const isLoading = [health, version, readiness].some((item) => item.status === "loading");
  const demoMessage = [health, version, readiness].find((item) => item.status === "demo")?.message;
  const error = [health, version, readiness].find((item) => item.status === "error")?.error;

  return (
    <div className="page-grid">
      <section className="page-panel wide">
        <div className="page-title">
          <span>{t("dashboard.kicker")}</span>
          <h2>{t("dashboard.title")}</h2>
          <p>
            {t("dashboard.description")}
          </p>
        </div>
        <div className="boundary-row">
          <BoundaryBadge>{t("dashboard.badge.noSolver")}</BoundaryBadge>
          <BoundaryBadge>{t("dashboard.badge.noLlm")}</BoundaryBadge>
          <BoundaryBadge tone="notice">{t("dashboard.badge.noPypi")}</BoundaryBadge>
          <BoundaryBadge>{t("dashboard.badge.noConvergence")}</BoundaryBadge>
        </div>
      </section>

      <GuidedDemoStepper onNavigate={onNavigate} />
      <ChineseGuidedTutorial />
      <QuickstartPanel />

      {isLoading ? <LoadingState label={t("dashboard.loading")} /> : null}
      <ApiModeIndicator statuses={[health.status, version.status, readiness.status]} />
      {demoMessage ? <ApiDisconnectedNotice message={demoMessage} /> : null}
      {error ? (
        <ErrorState
          message={error.message}
          actions={error.recommended_next_actions}
        />
      ) : null}

      <section className="status-grid wide">
        <StatusCard label={t("dashboard.card.service")} value={health.data?.status || health.status} note={health.data?.service} />
        <StatusCard
          label={t("dashboard.card.package")}
          value={version.data?.package_version || version.status}
          note={version.data?.api_contract_version ? `API ${version.data.api_contract_version}` : undefined}
        />
        <StatusCard
          label={t("dashboard.card.publicPrerelease")}
          value={readiness.data?.current_public_prerelease || readiness.status}
          note={t("dashboard.card.currentCandidate")}
        />
        <StatusCard
          label={t("dashboard.card.pypi")}
          value={readiness.data?.pypi?.published === false ? t("dashboard.card.notPublished") : readiness.status}
          note={t("dashboard.card.noPublicationControl")}
        />
      </section>

      <section className="page-panel wide">
        <p className="first-time-prompt">{t("quickstart.firstTimePrompt")}</p>
        <RecommendedActions
          actions={readiness.data?.recommended_next_actions || [
            t("dashboard.startApiAction"),
            t("quickstart.loadChineseNanoparticleExample"),
            t("guidedTutorial.step.parse.title"),
            t("guidedTutorial.step.validate.title"),
            t("guidedTutorial.step.workflow.title"),
          ]}
        />
      </section>

      <JsonPanel title={t("dashboard.readinessPayload")} value={readiness.data || { status: readiness.status }} />
    </div>
  );
}
