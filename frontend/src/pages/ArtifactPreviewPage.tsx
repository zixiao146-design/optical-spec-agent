import { useState } from "react";
import { agentApi } from "../api/client";
import { jsonParseError, stateFromPayload, type RemoteState } from "../api/state";
import type { AdapterPreviewResponse } from "../api/types";
import { ApiDisconnectedNotice } from "../components/ApiDisconnectedNotice";
import { ArtifactPreviewPanel } from "../components/ArtifactPreviewPanel";
import { BoundaryBadge } from "../components/BoundaryBadge";
import { DemoModeBanner } from "../components/DemoModeBanner";
import { DiagnosticsPanel } from "../components/DiagnosticsPanel";
import { EmptyState } from "../components/EmptyState";
import { ErrorState } from "../components/ErrorState";
import { JsonPanel } from "../components/JsonPanel";
import { LoadingState } from "../components/LoadingState";
import { RecommendedActions } from "../components/RecommendedActions";
import {
  demoAdapterPreview,
  demoAdapterPreviewRequestText,
} from "../fixtures/demoData";
import { useI18n } from "../i18n/useI18n";

const TOOLS = ["gmsh", "meep", "mpb", "elmer", "optiland"];

export function ArtifactPreviewPage() {
  const { t } = useI18n();
  const [tool, setTool] = useState("gmsh");
  const [requestText, setRequestText] = useState(demoAdapterPreviewRequestText);
  const [fixtureNotice, setFixtureNotice] = useState(t("state.demoLoadedMessage"));
  const [response, setResponse] = useState<RemoteState<AdapterPreviewResponse>>({ status: "idle" });

  function loadMinimalSpec() {
    setTool("gmsh");
    setRequestText(demoAdapterPreviewRequestText);
    setFixtureNotice(t("state.demoLoadedMessage"));
    setResponse({ status: "idle" });
  }

  async function preview() {
    setResponse({ status: "loading", message: t("preview.loadingMessage") });
    try {
      const body = JSON.parse(requestText) as { path?: string; spec?: Record<string, unknown> };
      const payload = await agentApi.getAdapterPreview({ ...body, tool });
      setResponse(
        stateFromPayload(payload, demoAdapterPreview, t("preview.demo")),
      );
    } catch (error) {
      const apiError = jsonParseError(error);
      setResponse({ status: "error", error: apiError, message: apiError.message });
    }
  }

  return (
    <div className="page-grid">
      <section className="page-panel wide">
        <div className="page-title">
          <span>{t("preview.kicker")}</span>
          <h2>{t("preview.title")}</h2>
          <p>
            {t("preview.description")}
          </p>
        </div>
        <div className="boundary-row">
          <BoundaryBadge>{t("preview.badge.previewOnly")}</BoundaryBadge>
          <BoundaryBadge>{t("preview.badge.noSolver")}</BoundaryBadge>
        </div>
      </section>
      <DemoModeBanner message={fixtureNotice} />
      <section className="page-panel">
        <h3>{t("preview.requestTitle")}</h3>
        <label htmlFor="adapter-tool">
          {t("preview.toolLabel")}
        </label>
        <select id="adapter-tool" value={tool} onChange={(event) => setTool(event.target.value)}>
          {TOOLS.map((item) => (
            <option key={item} value={item}>
              {item}
            </option>
          ))}
        </select>
        <label htmlFor="adapter-preview-request">{t("preview.requestLabel")}</label>
        <textarea
          id="adapter-preview-request"
          value={requestText}
          onChange={(event) => setRequestText(event.target.value)}
          aria-describedby="adapter-preview-status"
        />
        <button
          type="button"
          onClick={() => void preview()}
          disabled={response.status === "loading" || requestText.trim().length === 0}
        >
          {response.status === "loading" ? t("preview.generating") : t("preview.generateButton")}
        </button>
        <button type="button" className="secondary-button" onClick={loadMinimalSpec}>
          {t("preview.loadMinimal")}
        </button>
        <p className="inline-boundary">{t("preview.inlineBoundary")}</p>
        <div id="adapter-preview-status" className="sr-status" aria-live="polite">
          {t("preview.status")} {response.status}
        </div>
      </section>
      <section className="page-panel">
        <h3>{t("preview.stateTitle")}</h3>
        {response.status === "idle" ? (
          <EmptyState title={t("preview.emptyTitle")} message={t("preview.emptyMessage")} />
        ) : null}
        {response.status === "loading" ? <LoadingState label={t("preview.loading")} /> : null}
        {response.status === "demo" ? <ApiDisconnectedNotice message={response.message} /> : null}
        {response.status === "error" && response.error ? (
          <ErrorState message={response.error.message} actions={response.error.recommended_next_actions} />
        ) : null}
      </section>
      <ArtifactPreviewPanel response={response.data} />
      <DiagnosticsPanel diagnostics={response.data?.diagnostics || response.error?.diagnostics} title={t("preview.diagnostics")} />
      <RecommendedActions actions={response.data?.recommended_next_actions || response.error?.recommended_next_actions} title={t("preview.actions")} />
      <JsonPanel title={t("preview.jsonTitle")} value={response.data || response.error || { status: response.status }} />
    </div>
  );
}
