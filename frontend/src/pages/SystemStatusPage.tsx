import { useEffect, useState } from "react";
import { agentApi } from "../api/client";
import { INITIAL_LOADING_STATE, stateFromPayload, type RemoteState } from "../api/state";
import type { HealthResponse, SchemaResponse, VersionResponse } from "../api/types";
import { ApiDisconnectedNotice } from "../components/ApiDisconnectedNotice";
import { ApiModeIndicator } from "../components/ApiModeIndicator";
import { BoundaryBadge } from "../components/BoundaryBadge";
import { ErrorState } from "../components/ErrorState";
import { JsonPanel } from "../components/JsonPanel";
import { LoadingState } from "../components/LoadingState";
import { StatusCard } from "../components/StatusCard";
import { demoHealth, demoSchema, demoVersion } from "../fixtures/demoData";
import { useI18n } from "../i18n/useI18n";

export function SystemStatusPage() {
  const { t } = useI18n();
  const [health, setHealth] = useState<RemoteState<HealthResponse>>(INITIAL_LOADING_STATE);
  const [version, setVersion] = useState<RemoteState<VersionResponse>>(INITIAL_LOADING_STATE);
  const [schema, setSchema] = useState<RemoteState<SchemaResponse>>(INITIAL_LOADING_STATE);

  useEffect(() => {
    let active = true;
    void agentApi.getHealth().then((payload) => {
      if (active) setHealth(stateFromPayload(payload, demoHealth, t("system.healthDemo")));
    });
    void agentApi.getVersion().then((payload) => {
      if (active) setVersion(stateFromPayload(payload, demoVersion, t("system.versionDemo")));
    });
    void agentApi.getSchema().then((payload) => {
      if (active) setSchema(stateFromPayload(payload, demoSchema, t("system.schemaDemo")));
    });
    return () => {
      active = false;
    };
  }, [t]);

  const isLoading = [health, version, schema].some((item) => item.status === "loading");
  const demoMessage = [health, version, schema].find((item) => item.status === "demo")?.message;
  const error = [health, version, schema].find((item) => item.status === "error")?.error;

  return (
    <div className="page-grid">
      <section className="page-panel wide">
        <div className="page-title">
          <span>{t("system.kicker")}</span>
          <h2>{t("system.title")}</h2>
          <p>
            {t("system.description")}
          </p>
        </div>
        <div className="boundary-row">
          <BoundaryBadge>{t("system.badge.noUpload")}</BoundaryBadge>
          <BoundaryBadge>{t("system.badge.noRelease")}</BoundaryBadge>
        </div>
      </section>
      {isLoading ? <LoadingState label={t("system.loading")} /> : null}
      <ApiModeIndicator statuses={[health.status, version.status, schema.status]} />
      {demoMessage ? <ApiDisconnectedNotice message={demoMessage} /> : null}
      {error ? <ErrorState message={error.message} actions={error.recommended_next_actions} /> : null}
      <section className="status-grid wide">
        <StatusCard label={t("system.card.apiContract")} value={version.data?.api_contract_version || version.status} />
        <StatusCard label={t("system.card.package")} value={version.data?.package_version || version.status} />
        <StatusCard label={t("system.card.schema")} value={schema.data?.schema_name || schema.status} />
      </section>
      <JsonPanel title={t("system.health")} value={health.data || health.error || { status: health.status }} />
      <JsonPanel title={t("system.version")} value={version.data || version.error || { status: version.status }} />
      <JsonPanel title={t("system.schema")} value={schema.data || schema.error || { status: schema.status }} />
    </div>
  );
}
