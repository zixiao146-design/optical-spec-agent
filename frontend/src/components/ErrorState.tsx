import { useI18n } from "../i18n/useI18n";

interface ErrorStateProps {
  title?: string;
  message: string;
  actions?: string[];
}

export function ErrorState({
  title,
  message,
  actions,
}: ErrorStateProps) {
  const { t } = useI18n();
  const visibleActions = actions || [t("state.error.defaultAction")];
  return (
    <div className="state-box error-state" role="alert" aria-live="assertive">
      <strong>{title || t("state.error.defaultTitle")}</strong>
      <span>{message}</span>
      {visibleActions.length > 0 ? (
        <ul>
          {visibleActions.map((action) => (
            <li key={action}>{action}</li>
          ))}
        </ul>
      ) : null}
    </div>
  );
}
