import { useEffect, useState } from "react";
import { agentApi } from "../api/client";
import type { HealthResponse, ReadinessResponse, VersionResponse } from "../api/types";
import { BoundaryBadge } from "../components/BoundaryBadge";
import { JsonPanel } from "../components/JsonPanel";
import { StatusCard } from "../components/StatusCard";

export function DashboardPage() {
  const [health, setHealth] = useState<HealthResponse | undefined>();
  const [version, setVersion] = useState<VersionResponse | undefined>();
  const [readiness, setReadiness] = useState<ReadinessResponse | undefined>();

  useEffect(() => {
    void agentApi.getHealth().then((payload) => setHealth(payload as HealthResponse));
    void agentApi.getVersion().then((payload) => setVersion(payload as VersionResponse));
    void agentApi.getReadiness().then((payload) => setReadiness(payload as ReadinessResponse));
  }, []);

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

      <section className="status-grid wide">
        <StatusCard label="Service" value={health?.status || "loading"} note={health?.service} />
        <StatusCard
          label="Package"
          value={version?.package_version || "loading"}
          note={version?.api_contract_version ? `API ${version.api_contract_version}` : undefined}
        />
        <StatusCard
          label="Public prerelease"
          value={readiness?.current_public_prerelease || "loading"}
          note="Current public candidate"
        />
        <StatusCard
          label="PyPI"
          value={readiness?.pypi?.published === false ? "not published" : "loading"}
          note="No publication control in UI"
        />
      </section>

      <section className="page-panel wide">
        <h3>Recommended next actions</h3>
        <ul className="action-list">
          {(readiness?.recommended_next_actions || ["Start the local API to load readiness."]).map(
            (item) => (
              <li key={item}>{item}</li>
            ),
          )}
        </ul>
      </section>

      <JsonPanel title="Readiness payload" value={readiness || { status: "loading" }} />
    </div>
  );
}
