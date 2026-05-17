import { API_BASE_URL } from "../api/client";
import type { RemoteStatus } from "../api/state";

interface ApiModeIndicatorProps {
  statuses: RemoteStatus[];
}

export function ApiModeIndicator({ statuses }: ApiModeIndicatorProps) {
  const hasDemo = statuses.includes("demo");
  const hasError = statuses.includes("error");
  const hasLoading = statuses.includes("loading");
  const mode = hasDemo
    ? "API disconnected - Demo fixture mode"
    : hasError
      ? "API error"
      : hasLoading
        ? "Checking API connection"
        : "API connected";

  return (
    <section className={`api-mode-indicator ${hasDemo ? "api-mode-demo" : ""}`} aria-live="polite">
      <div>
        <strong>{mode}</strong>
        <span>API base URL: {API_BASE_URL}</span>
      </div>
      {hasDemo ? (
        <p>
          Start local API with: <code>python -m uvicorn optical_spec_agent.api.app:app --reload --host 127.0.0.1 --port 8000</code>
        </p>
      ) : null}
    </section>
  );
}
