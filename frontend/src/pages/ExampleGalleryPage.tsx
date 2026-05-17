import { useEffect, useMemo, useState } from "react";
import { agentApi } from "../api/client";
import { INITIAL_LOADING_STATE, stateFromPayload, type RemoteState } from "../api/state";
import type {
  AgentTraceResponse,
  ExampleDetailResponse,
  ExamplesResponse,
  OpticalDesignExampleSummary,
} from "../api/types";
import { ApiDisconnectedNotice } from "../components/ApiDisconnectedNotice";
import { BoundaryBadge } from "../components/BoundaryBadge";
import { DiagnosticsPanel } from "../components/DiagnosticsPanel";
import { EmptyState } from "../components/EmptyState";
import { ErrorState } from "../components/ErrorState";
import { JsonPanel } from "../components/JsonPanel";
import { LoadingState } from "../components/LoadingState";
import { RecommendedActions } from "../components/RecommendedActions";
import { demoAgentTrace, demoExampleDetail, demoExamples } from "../fixtures/demoData";
import { useI18n } from "../i18n/useI18n";

export function ExampleGalleryPage() {
  const { language, t } = useI18n();
  const [examples, setExamples] = useState<RemoteState<ExamplesResponse>>(INITIAL_LOADING_STATE);
  const [selectedExampleId, setSelectedExampleId] = useState("nanoparticle_plasmonics");
  const [detail, setDetail] = useState<RemoteState<ExampleDetailResponse>>({ status: "idle" });
  const [trace, setTrace] = useState<RemoteState<AgentTraceResponse>>({ status: "idle" });

  useEffect(() => {
    let active = true;
    void agentApi.getExamples().then((payload) => {
      if (active) setExamples(stateFromPayload(payload, demoExamples, t("examples.demo")));
    });
    return () => {
      active = false;
    };
  }, [t]);

  const selectedSummary = useMemo(() => {
    const liveRows = Array.isArray(examples.data?.examples) ? examples.data.examples : [];
    const rows = liveRows.length ? liveRows : demoExamples.examples;
    return rows.find((item) => item.example_id === selectedExampleId);
  }, [examples.data?.examples, examples.status, selectedExampleId]);

  async function loadExample(example: OpticalDesignExampleSummary) {
    setSelectedExampleId(example.example_id);
    setDetail({ status: "loading", message: t("examples.loadingDetail") });
    const payload = await agentApi.getExample(example.example_id);
    setDetail(stateFromPayload(payload, demoExampleDetail, t("examples.detailDemo")));
  }

  async function loadTrace(exampleId = selectedExampleId) {
    setTrace({ status: "loading", message: t("examples.loadingTrace") });
    const payload = await agentApi.getExampleAgentTrace(exampleId);
    setTrace(stateFromPayload(payload, demoAgentTrace, t("examples.traceDemo")));
  }

  const liveExampleRows = Array.isArray(examples.data?.examples) ? examples.data.examples : [];
  const examplesRows = liveExampleRows.length ? liveExampleRows : demoExamples.examples;

  return (
    <div className="page-grid">
      <section className="page-panel wide">
        <div className="page-title">
          <span>{t("examples.kicker")}</span>
          <h2>{t("examples.title")}</h2>
          <p>{t("examples.description")}</p>
        </div>
        <div className="boundary-row">
          <BoundaryBadge>{t("examples.badge.noSolver")}</BoundaryBadge>
          <BoundaryBadge>{t("examples.badge.noLlm")}</BoundaryBadge>
          <BoundaryBadge tone="notice">{t("examples.badge.preview")}</BoundaryBadge>
        </div>
      </section>

      <section className="page-panel wide">
        <h3>{t("examples.galleryTitle")}</h3>
        {examples.status === "loading" ? <LoadingState label={t("examples.loading")} /> : null}
        {examples.status === "demo" ? <ApiDisconnectedNotice message={examples.message} /> : null}
        {examples.status === "error" && examples.error ? (
          <ErrorState message={examples.error.message} actions={examples.error.recommended_next_actions} />
        ) : null}
        {examplesRows.length === 0 && examples.status !== "loading" ? (
          <EmptyState title={t("examples.emptyTitle")} message={t("examples.emptyMessage")} />
        ) : (
          <div className="example-gallery-grid" aria-label={t("examples.galleryTitle")}>
            {examplesRows.map((example) => (
              <article className="example-card" key={example.example_id}>
                <span>{example.category}</span>
                <h3>{language === "zh-CN" ? example.title_zh : example.title}</h3>
                <p>{language === "zh-CN" ? example.design_goal_zh : example.design_goal}</p>
                <dl>
                  <dt>{t("examples.materials")}</dt>
                  <dd>{example.suggested_materials.join(", ")}</dd>
                  <dt>{t("examples.adapter")}</dt>
                  <dd>{example.suggested_adapter}</dd>
                  <dt>{t("examples.focus")}</dt>
                  <dd>{example.workflow_focus.join(" -> ")}</dd>
                </dl>
                <p className="inline-boundary">{example.maturity_note}</p>
                <div className="button-row">
                  <button type="button" onClick={() => void loadExample(example)}>
                    {t("examples.load")}
                  </button>
                  <button type="button" onClick={() => void loadTrace(example.example_id)}>
                    {t("examples.viewTrace")}
                  </button>
                </div>
              </article>
            ))}
          </div>
        )}
      </section>

      <section className="page-panel">
        <h3>{t("examples.selectedTitle")}</h3>
        <label htmlFor="example-selector">{t("examples.selectorLabel")}</label>
        <select
          id="example-selector"
          value={selectedExampleId}
          onChange={(event) => setSelectedExampleId(event.target.value)}
        >
          {examplesRows.map((example) => (
            <option value={example.example_id} key={example.example_id}>
              {language === "zh-CN" ? example.title_zh : example.title}
            </option>
          ))}
        </select>
        <div className="button-row">
          <button
            type="button"
            onClick={() => selectedSummary && void loadExample(selectedSummary)}
            disabled={!selectedSummary || detail.status === "loading"}
          >
            {detail.status === "loading" ? t("examples.loadingShort") : t("examples.viewSpec")}
          </button>
          <button
            type="button"
            onClick={() => void loadTrace()}
            disabled={trace.status === "loading"}
          >
            {trace.status === "loading" ? t("examples.traceLoadingShort") : t("examples.generateTrace")}
          </button>
        </div>
      </section>

      <section className="page-panel">
        <h3>{t("examples.connectionTitle")}</h3>
        <p>{t("examples.connectionFlow")}</p>
        <ul className="compact-list">
          <li>{t("examples.connection.materials")}</li>
          <li>{t("examples.connection.adapters")}</li>
          <li>{t("examples.connection.workflow")}</li>
          <li>{t("examples.connection.evidence")}</li>
        </ul>
      </section>

      <JsonPanel title={t("examples.detailJson")} value={detail.data || detail.error || { status: detail.status }} />
      <JsonPanel title={t("examples.traceJson")} value={trace.data || trace.error || { status: trace.status }} />
      <DiagnosticsPanel diagnostics={examples.data?.diagnostics || examples.error?.diagnostics} title={t("examples.diagnostics")} />
      <RecommendedActions actions={examples.data?.recommended_next_actions || examples.error?.recommended_next_actions} title={t("examples.actions")} />
    </div>
  );
}
