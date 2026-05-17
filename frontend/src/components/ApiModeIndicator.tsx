import { API_BASE_URL } from "../api/client";
import type { RemoteStatus } from "../api/state";
import { useI18n } from "../i18n/useI18n";

interface ApiModeIndicatorProps {
  statuses: RemoteStatus[];
}

export function ApiModeIndicator({ statuses }: ApiModeIndicatorProps) {
  const { t } = useI18n();
  const hasDemo = statuses.includes("demo");
  const hasError = statuses.includes("error");
  const hasLoading = statuses.includes("loading");
  const mode = hasDemo
    ? t("state.apiMode.demo")
    : hasError
      ? t("state.apiMode.error")
      : hasLoading
        ? t("state.apiMode.loading")
        : t("state.apiMode.connected");

  return (
    <section className={`api-mode-indicator ${hasDemo ? "api-mode-demo" : ""}`} aria-live="polite">
      <div>
        <strong>{mode}</strong>
        <span>{t("state.apiMode.baseUrl")} {API_BASE_URL}</span>
      </div>
      {hasDemo ? (
        <p>
          {t("state.apiMode.startApi")} <code>python -m uvicorn optical_spec_agent.api.app:app --reload --host 127.0.0.1 --port 8000</code>
        </p>
      ) : null}
    </section>
  );
}
