import { useI18n } from "../i18n/useI18n";

interface ApiDisconnectedNoticeProps {
  message?: string;
}

export function ApiDisconnectedNotice({
  message,
}: ApiDisconnectedNoticeProps) {
  const { t } = useI18n();
  return (
    <div className="state-box api-disconnected" role="status" aria-live="polite">
      <strong>{t("state.apiDisconnectedTitle")}</strong>
      <span>{message || t("state.apiDisconnectedMessage")}</span>
      <span>{t("state.apiDisconnectedSafety")}</span>
    </div>
  );
}
