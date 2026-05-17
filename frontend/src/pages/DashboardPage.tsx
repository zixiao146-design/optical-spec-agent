import { useEffect, useState } from "react";
import { agentApi } from "../api/client";
import { INITIAL_LOADING_STATE, stateFromPayload, type RemoteState } from "../api/state";
import type { HealthResponse, ReadinessResponse, VersionResponse } from "../api/types";
import { ApiDisconnectedNotice } from "../components/ApiDisconnectedNotice";
import { ApiModeIndicator } from "../components/ApiModeIndicator";
import { BoundaryBadge } from "../components/BoundaryBadge";
import { ErrorState } from "../components/ErrorState";
import { JsonPanel } from "../components/JsonPanel";
import { LoadingState } from "../components/LoadingState";
import { RecommendedActions } from "../components/RecommendedActions";
import { StatusCard } from "../components/StatusCard";
import { demoHealth, demoReadiness, demoVersion } from "../fixtures/demoData";

export function DashboardPage() {
  const [health, setHealth] = useState<RemoteState<HealthResponse>>(INITIAL_LOADING_STATE);
  const [version, setVersion] = useState<RemoteState<VersionResponse>>(INITIAL_LOADING_STATE);
  const [readiness, setReadiness] = useState<RemoteState<ReadinessResponse>>(INITIAL_LOADING_STATE);

  useEffect(() => {
    let active = true;
    void agentApi.getHealth().then((payload) => {
      if (active) setHealth(stateFromPayload(payload, demoHealth, "Demo health fixture shown; this is not live API health."));
    });
    void agentApi.getVersion().then((payload) => {
      if (active) setVersion(stateFromPayload(payload, demoVersion, "Demo version fixture shown; this is not a live API version check."));
    });
    void agentApi.getReadiness().then((payload) => {
      if (active) setReadiness(stateFromPayload(payload, demoReadiness, "Demo readiness fixture shown; this is not live validation."));
    });
    return () => {
      active = false;
    };
  }, []);

  const isLoading = [health, version, readiness].some((item) => item.status === "loading");
  const demoMessage = [health, version, readiness].find((item) => item.status === "demo")?.message;
  const error = [health, version, readiness].find((item) => item.status === "error")?.error;

  return (
    <div className="page-grid">
      <section className="page-panel wide">
        <div className="page-title">
          <span>Dashboard / Readiness</span>
          <h2>Local Agent API workbench</h2>
          <p>
            Agent Studio MVP visualizes the local API state, release boundaries,
            and recommended next actions without running solvers or publishing packages.
          </p>
        </div>
        <div className="boundary-row">
          <BoundaryBadge>No solver execution by default</BoundaryBadge>
          <BoundaryBadge>No external LLM by default</BoundaryBadge>
          <BoundaryBadge tone="notice">PyPI not controlled here</BoundaryBadge>
          <BoundaryBadge>Formal convergence proof not claimed</BoundaryBadge>
        </div>
      </section>

      {isLoading ? <LoadingState label="Loading dashboard from the local Agent API..." /> : null}
      <ApiModeIndicator statuses={[health.status, version.status, readiness.status]} />
      {demoMessage ? <ApiDisconnectedNotice message={demoMessage} /> : null}
      {error ? (
        <ErrorState
          message={error.message}
          actions={error.recommended_next_actions}
        />
      ) : null}

      <section className="status-grid wide">
        <StatusCard label="Service" value={health.data?.status || health.status} note={health.data?.service} />
        <StatusCard
          label="Package"
          value={version.data?.package_version || version.status}
          note={version.data?.api_contract_version ? `API ${version.data.api_contract_version}` : undefined}
        />
        <StatusCard
          label="Public prerelease"
          value={readiness.data?.current_public_prerelease || readiness.status}
          note="Current public candidate"
        />
        <StatusCard
          label="PyPI"
          value={readiness.data?.pypi?.published === false ? "not published" : readiness.status}
          note="No publication control in UI"
        />
      </section>

      <section className="page-panel wide">
        <RecommendedActions
          actions={readiness.data?.recommended_next_actions || ["Start the local API to load readiness."]}
        />
      </section>

      <JsonPanel title="Readiness payload" value={readiness.data || { status: readiness.status }} />
    </div>
  );
}
