import { useState } from "react";
import { agentApi } from "../api/client";
import { jsonParseError, stateFromPayload, type RemoteState } from "../api/state";
import type { ParseResponse, ValidateResponse } from "../api/types";
import { ApiDisconnectedNotice } from "../components/ApiDisconnectedNotice";
import { BoundaryBadge } from "../components/BoundaryBadge";
import { DemoModeBanner } from "../components/DemoModeBanner";
import { DiagnosticsPanel } from "../components/DiagnosticsPanel";
import { EmptyState } from "../components/EmptyState";
import { ErrorState } from "../components/ErrorState";
import { JsonPanel } from "../components/JsonPanel";
import { LoadingState } from "../components/LoadingState";
import { RecommendedActions } from "../components/RecommendedActions";
import {
  demoChineseNaturalLanguageSpec,
  demoNaturalLanguageSpec,
  demoParseResponse,
  demoValidateRequestText,
  demoValidateResponse,
} from "../fixtures/demoData";
import { useI18n } from "../i18n/useI18n";

export function SpecInputPage() {
  const { language, t } = useI18n();
  const localizedDemoSpec = language === "zh-CN" ? demoChineseNaturalLanguageSpec : demoNaturalLanguageSpec;
  const [text, setText] = useState(localizedDemoSpec);
  const [validateJson, setValidateJson] = useState(demoValidateRequestText);
  const [fixtureNotice, setFixtureNotice] = useState(
    language === "zh-CN" ? t("quickstart.exampleLoaded") : t("state.demoLoadedMessage"),
  );
  const [parseResponse, setParseResponse] = useState<RemoteState<ParseResponse>>({ status: "idle" });
  const [validateResponse, setValidateResponse] = useState<RemoteState<ValidateResponse>>({ status: "idle" });

  function loadExampleSpec() {
    setText(localizedDemoSpec);
    setValidateJson(demoValidateRequestText);
    setFixtureNotice(language === "zh-CN" ? t("quickstart.exampleLoaded") : t("state.demoLoadedMessage"));
    setParseResponse({ status: "idle" });
    setValidateResponse({ status: "idle" });
  }

  async function parseLocally() {
    setParseResponse({ status: "loading", message: t("spec.parseLoadingMessage") });
    const payload = await agentApi.parseSpec({ text, parser: "heuristic", json: true });
    setParseResponse(
      stateFromPayload(payload, demoParseResponse, t("spec.parseDemo")),
    );
  }

  async function validateSpec() {
    setValidateResponse({ status: "loading", message: t("spec.validateLoadingMessage") });
    try {
      const body = JSON.parse(validateJson) as { spec?: Record<string, unknown>; path?: string };
      const payload = await agentApi.validateSpec(body);
      setValidateResponse(
        stateFromPayload(payload, demoValidateResponse, t("spec.validateDemo")),
      );
    } catch (error) {
      const apiError = jsonParseError(error);
      setValidateResponse({ status: "error", error: apiError, message: apiError.message });
    }
  }

  return (
    <div className="page-grid">
      <section className="page-panel wide">
        <div className="page-title">
          <span>{t("spec.kicker")}</span>
          <h2>{t("spec.title")}</h2>
          <p>
            {t("spec.description")}
          </p>
        </div>
        <div className="boundary-row">
          <BoundaryBadge>{t("spec.badge.noLlm")}</BoundaryBadge>
          <BoundaryBadge>{t("spec.badge.noProduction")}</BoundaryBadge>
        </div>
      </section>

      <DemoModeBanner message={fixtureNotice} />

      <section className="page-panel">
        <h3>{t("spec.nlTitle")}</h3>
        <label htmlFor="spec-text">{t("spec.nlLabel")}</label>
        <textarea
          id="spec-text"
          value={text}
          onChange={(event) => setText(event.target.value)}
          aria-describedby="parse-status"
        />
        <button
          type="button"
          onClick={() => void parseLocally()}
          disabled={parseResponse.status === "loading" || text.trim().length === 0}
        >
          {parseResponse.status === "loading" ? t("spec.parseLoading") : t("spec.parseButton")}
        </button>
        <button type="button" className="secondary-button" onClick={loadExampleSpec}>
          {language === "zh-CN" ? t("quickstart.loadChineseNanoparticleExample") : t("spec.loadExample")}
        </button>
        <div id="parse-status" className="sr-status" aria-live="polite">
          {t("spec.parseStatus")} {parseResponse.status}
        </div>
      </section>

      <section className="page-panel">
        <h3>{t("spec.validateTitle")}</h3>
        <label htmlFor="validate-json">{t("spec.validateLabel")}</label>
        <textarea
          id="validate-json"
          value={validateJson}
          onChange={(event) => setValidateJson(event.target.value)}
          aria-describedby="validate-status"
        />
        <button
          type="button"
          onClick={() => void validateSpec()}
          disabled={validateResponse.status === "loading" || validateJson.trim().length === 0}
        >
          {validateResponse.status === "loading" ? t("spec.validateLoading") : t("spec.validateButton")}
        </button>
        <button type="button" className="secondary-button" onClick={loadExampleSpec}>
          {t("spec.loadFixture")}
        </button>
        <div id="validate-status" className="sr-status" aria-live="polite">
          {t("spec.validationStatus")} {validateResponse.status}
        </div>
      </section>

      <section className="page-panel">
        <h3>{t("spec.parseState")}</h3>
        {parseResponse.status === "idle" ? (
          <EmptyState title={t("spec.noParseTitle")} message={t("spec.noParseMessage")} />
        ) : null}
        {parseResponse.status === "loading" ? <LoadingState label={t("spec.parsingLabel")} /> : null}
        {parseResponse.status === "demo" ? <ApiDisconnectedNotice message={parseResponse.message} /> : null}
        {parseResponse.status === "error" && parseResponse.error ? (
          <ErrorState message={parseResponse.error.message} actions={parseResponse.error.recommended_next_actions} />
        ) : null}
      </section>

      <section className="page-panel">
        <h3>{t("spec.validationState")}</h3>
        {validateResponse.status === "idle" ? (
          <EmptyState title={t("spec.noValidationTitle")} message={t("spec.noValidationMessage")} />
        ) : null}
        {validateResponse.status === "loading" ? <LoadingState label={t("spec.validatingLabel")} /> : null}
        {validateResponse.status === "demo" ? <ApiDisconnectedNotice message={validateResponse.message} /> : null}
        {validateResponse.status === "error" && validateResponse.error ? (
          <ErrorState
            message={validateResponse.error.message}
            actions={validateResponse.error.recommended_next_actions}
          />
        ) : null}
      </section>

      <DiagnosticsPanel diagnostics={parseResponse.data?.diagnostics || parseResponse.error?.diagnostics} title={t("spec.parseDiagnostics")} />
      <RecommendedActions actions={parseResponse.data?.recommended_next_actions || parseResponse.error?.recommended_next_actions} title={t("spec.parseActions")} />
      <DiagnosticsPanel diagnostics={validateResponse.data?.diagnostics || validateResponse.error?.diagnostics} title={t("spec.validationDiagnostics")} />
      <RecommendedActions actions={validateResponse.data?.recommended_next_actions || validateResponse.error?.recommended_next_actions} title={t("spec.validationActions")} />
      <JsonPanel title={t("spec.parsedSpec")} value={parseResponse.data || { status: parseResponse.status }} />
      <JsonPanel title={t("spec.validationResult")} value={validateResponse.data || { status: validateResponse.status }} />
    </div>
  );
}
