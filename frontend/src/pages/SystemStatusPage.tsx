import { useEffect, useState } from "react";
import { agentApi } from "../api/client";
import { INITIAL_LOADING_STATE, stateFromPayload, type RemoteState } from "../api/state";
import type { HealthResponse, SchemaResponse, VersionResponse } from "../api/types";
import { ApiDisconnectedNotice } from "../components/ApiDisconnectedNotice";
import { BoundaryBadge } from "../components/BoundaryBadge";
import { ErrorState } from "../components/ErrorState";
import { JsonPanel } from "../components/JsonPanel";
import { LoadingState } from "../components/LoadingState";
import { StatusCard } from "../components/StatusCard";
import { demoHealth, demoSchema, demoVersion } from "../fixtures/demoData";

export function SystemStatusPage() {
  const [health, setHealth] = useState<RemoteState<HealthResponse>>(INITIAL_LOADING_STATE);
  const [version, setVersion] = useState<RemoteState<VersionResponse>>(INITIAL_LOADING_STATE);
  const [schema, setSchema] = useState<RemoteState<SchemaResponse>>(INITIAL_LOADING_STATE);

  useEffect(() => {
    let active = true;
    void agentApi.getHealth().then((payload) => {
      if (active) setHealth(stateFromPayload(payload, demoHealth, "Demo health fixture shown; this is not live API health."));
    });
    void agentApi.getVersion().then((payload) => {
      if (active) setVersion(stateFromPayload(payload, demoVersion, "Demo version fixture shown; this is not live API version."));
    });
    void agentApi.getSchema().then((payload) => {
      if (active) setSchema(stateFromPayload(payload, demoSchema, "Demo schema fixture shown; this is not live schema metadata."));
    });
    return () => {
      active = false;
    };
  }, []);

  const isLoading = [health, version, schema].some((item) => item.status === "loading");
  const demoMessage = [health, version, schema].find((item) => item.status === "demo")?.message;
  const error = [health, version, schema].find((item) => item.status === "error")?.error;

  return (
    <div className="page-grid">
      <section className="page-panel wide">
        <div className="page-title">
          <span>API / System Status</span>
          <h2>Local API contract and schema</h2>
          <p>
            Use this view to confirm the API process, package version, and schema
            before frontend development.
          </p>
        </div>
        <div className="boundary-row">
          <BoundaryBadge>No upload controls in this UI</BoundaryBadge>
          <BoundaryBadge>No tag or release controls in this UI</BoundaryBadge>
        </div>
      </section>
      {isLoading ? <LoadingState label="Loading system status from the local API..." /> : null}
      {demoMessage ? <ApiDisconnectedNotice message={demoMessage} /> : null}
      {error ? <ErrorState message={error.message} actions={error.recommended_next_actions} /> : null}
      <section className="status-grid wide">
        <StatusCard label="API contract" value={version.data?.api_contract_version || version.status} />
        <StatusCard label="Package" value={version.data?.package_version || version.status} />
        <StatusCard label="Schema" value={schema.data?.schema_name || schema.status} />
      </section>
      <JsonPanel title="Health" value={health.data || health.error || { status: health.status }} />
      <JsonPanel title="Version" value={version.data || version.error || { status: version.status }} />
      <JsonPanel title="Schema" value={schema.data || schema.error || { status: schema.status }} />
    </div>
  );
}
