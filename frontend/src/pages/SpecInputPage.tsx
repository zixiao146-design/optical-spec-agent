import { useState } from "react";
import { agentApi } from "../api/client";
import type { ParseResponse, ValidateResponse } from "../api/types";
import { BoundaryBadge } from "../components/BoundaryBadge";
import { JsonPanel } from "../components/JsonPanel";

const DEFAULT_TEXT =
  "Use Meep FDTD to simulate an 80 nm gold nanoparticle on a 100 nm gold film with a 5 nm SiO2 gap, normal-incidence plane wave from 400-900 nm, and report the scattering spectrum.";

const DEFAULT_VALIDATE_REQUEST = JSON.stringify(
  { path: "examples/specs/minimal_nanoparticle.json" },
  null,
  2,
);

export function SpecInputPage() {
  const [text, setText] = useState(DEFAULT_TEXT);
  const [validateJson, setValidateJson] = useState(DEFAULT_VALIDATE_REQUEST);
  const [parseResponse, setParseResponse] = useState<unknown>();
  const [validateResponse, setValidateResponse] = useState<unknown>();

  async function parseLocally() {
    const payload = await agentApi.parseSpec({ text, parser: "heuristic", json: true });
    setParseResponse(payload as ParseResponse);
  }

  async function validateSpec() {
    try {
      const body = JSON.parse(validateJson) as { spec?: Record<string, unknown>; path?: string };
      const payload = await agentApi.validateSpec(body);
      setValidateResponse(payload as ValidateResponse);
    } catch (error) {
      setValidateResponse({
        status: "error",
        message: error instanceof Error ? error.message : String(error),
      });
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

      <section className="page-panel">
        <h3>Natural language spec</h3>
        <textarea value={text} onChange={(event) => setText(event.target.value)} />
        <button type="button" onClick={() => void parseLocally()}>
          Parse locally
        </button>
      </section>

      <section className="page-panel">
        <h3>Validate JSON request</h3>
        <textarea value={validateJson} onChange={(event) => setValidateJson(event.target.value)} />
        <button type="button" onClick={() => void validateSpec()}>
          Validate JSON
        </button>
      </section>

      <JsonPanel title="Parse response" value={parseResponse || { status: "waiting" }} />
      <JsonPanel title="Validation response" value={validateResponse || { status: "waiting" }} />
    </div>
  );
}
