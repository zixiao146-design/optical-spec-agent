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
  DEMO_FIXTURE_LOADED_MESSAGE,
  demoNaturalLanguageSpec,
  demoParseResponse,
  demoValidateRequestText,
  demoValidateResponse,
} from "../fixtures/demoData";

export function SpecInputPage() {
  const [text, setText] = useState(demoNaturalLanguageSpec);
  const [validateJson, setValidateJson] = useState(demoValidateRequestText);
  const [fixtureNotice, setFixtureNotice] = useState(DEMO_FIXTURE_LOADED_MESSAGE);
  const [parseResponse, setParseResponse] = useState<RemoteState<ParseResponse>>({ status: "idle" });
  const [validateResponse, setValidateResponse] = useState<RemoteState<ValidateResponse>>({ status: "idle" });

  function loadExampleSpec() {
    setText(demoNaturalLanguageSpec);
    setValidateJson(demoValidateRequestText);
    setFixtureNotice(DEMO_FIXTURE_LOADED_MESSAGE);
    setParseResponse({ status: "idle" });
    setValidateResponse({ status: "idle" });
  }

  async function parseLocally() {
    setParseResponse({ status: "loading", message: "Parsing with the local deterministic parser." });
    const payload = await agentApi.parseSpec({ text, parser: "heuristic", json: true });
    setParseResponse(
      stateFromPayload(payload, demoParseResponse, "Demo parse fixture shown; this is not live parsing."),
    );
  }

  async function validateSpec() {
    setValidateResponse({ status: "loading", message: "Validating with the local API." });
    try {
      const body = JSON.parse(validateJson) as { spec?: Record<string, unknown>; path?: string };
      const payload = await agentApi.validateSpec(body);
      setValidateResponse(
        stateFromPayload(payload, demoValidateResponse, "Demo validation fixture shown; this is not live validation."),
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
          <span>Spec Input</span>
          <h2>Parse and validate local optical specs</h2>
          <p>
            Use deterministic local parsing by default. External LLM paths are not
            exposed in the MVP.
          </p>
        </div>
        <div className="boundary-row">
          <BoundaryBadge>No external LLM was called</BoundaryBadge>
          <BoundaryBadge>No production-grade physical validation is claimed</BoundaryBadge>
        </div>
      </section>

      <DemoModeBanner message={fixtureNotice} />

      <section className="page-panel">
        <h3>Natural language spec</h3>
        <label htmlFor="spec-text">Natural language optical spec</label>
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
          {parseResponse.status === "loading" ? "Parsing..." : "Parse locally"}
        </button>
        <button type="button" className="secondary-button" onClick={loadExampleSpec}>
          Load example spec
        </button>
        <div id="parse-status" className="sr-status" aria-live="polite">
          Parse status: {parseResponse.status}
        </div>
      </section>

      <section className="page-panel">
        <h3>Validate JSON request</h3>
        <label htmlFor="validate-json">Validation request JSON</label>
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
          {validateResponse.status === "loading" ? "Validating..." : "Validate JSON"}
        </button>
        <button type="button" className="secondary-button" onClick={loadExampleSpec}>
          Load fixture
        </button>
        <div id="validate-status" className="sr-status" aria-live="polite">
          Validation status: {validateResponse.status}
        </div>
      </section>

      <section className="page-panel">
        <h3>Parse state</h3>
        {parseResponse.status === "idle" ? (
          <EmptyState title="No parse run yet" message="Paste or edit text, then choose Parse locally." />
        ) : null}
        {parseResponse.status === "loading" ? <LoadingState label="Parsing local spec text..." /> : null}
        {parseResponse.status === "demo" ? <ApiDisconnectedNotice message={parseResponse.message} /> : null}
        {parseResponse.status === "error" && parseResponse.error ? (
          <ErrorState message={parseResponse.error.message} actions={parseResponse.error.recommended_next_actions} />
        ) : null}
      </section>

      <section className="page-panel">
        <h3>Validation state</h3>
        {validateResponse.status === "idle" ? (
          <EmptyState title="No validation run yet" message="Use the fixture request or paste a spec object." />
        ) : null}
        {validateResponse.status === "loading" ? <LoadingState label="Validating local request..." /> : null}
        {validateResponse.status === "demo" ? <ApiDisconnectedNotice message={validateResponse.message} /> : null}
        {validateResponse.status === "error" && validateResponse.error ? (
          <ErrorState
            message={validateResponse.error.message}
            actions={validateResponse.error.recommended_next_actions}
          />
        ) : null}
      </section>

      <DiagnosticsPanel diagnostics={parseResponse.data?.diagnostics || parseResponse.error?.diagnostics} title="Parse diagnostics" />
      <RecommendedActions actions={parseResponse.data?.recommended_next_actions || parseResponse.error?.recommended_next_actions} title="Parse recommended next actions" />
      <DiagnosticsPanel diagnostics={validateResponse.data?.diagnostics || validateResponse.error?.diagnostics} title="Validation diagnostics" />
      <RecommendedActions actions={validateResponse.data?.recommended_next_actions || validateResponse.error?.recommended_next_actions} title="Validation recommended next actions" />
      <JsonPanel title="Parsed Spec" value={parseResponse.data || { status: parseResponse.status }} />
      <JsonPanel title="Validation Result" value={validateResponse.data || { status: validateResponse.status }} />
    </div>
  );
}
