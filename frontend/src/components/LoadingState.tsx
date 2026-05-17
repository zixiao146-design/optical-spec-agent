import { useI18n } from "../i18n/useI18n";

interface LoadingStateProps {
  label?: string;
}

export function LoadingState({ label }: LoadingStateProps) {
  const { t } = useI18n();
  return (
    <div className="state-box loading-state" role="status" aria-live="polite">
      <span className="spinner" aria-hidden="true" />
      <span>{label || t("state.loading.default")}</span>
    </div>
  );
}
