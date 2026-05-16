import { useEffect, useState } from "react";
import { agentApi } from "../api/client";
import { BoundaryBadge } from "../components/BoundaryBadge";
import { JsonPanel } from "../components/JsonPanel";
import { StatusCard } from "../components/StatusCard";

export function SystemStatusPage() {
  const [health, setHealth] = useState<unknown>();
  const [version, setVersion] = useState<unknown>();
  const [schema, setSchema] = useState<unknown>();

  useEffect(() => {
    void agentApi.getHealth().then(setHealth);
    void agentApi.getVersion().then(setVersion);
    void agentApi.getSchema().then(setSchema);
  }, []);

  const versionPayload = version as { api_contract_version?: string; package_version?: string };
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
      <section className="status-grid wide">
        <StatusCard label="API contract" value={versionPayload.api_contract_version || "loading"} />
        <StatusCard label="Package" value={versionPayload.package_version || "loading"} />
        <StatusCard label="Schema" value={(schema as { schema_name?: string })?.schema_name || "loading"} />
      </section>
      <JsonPanel title="Health" value={health || { status: "loading" }} />
      <JsonPanel title="Version" value={version || { status: "loading" }} />
      <JsonPanel title="Schema" value={schema || { status: "loading" }} />
    </div>
  );
}
