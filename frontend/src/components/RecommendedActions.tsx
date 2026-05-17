import { useI18n } from "../i18n/useI18n";
import { EmptyState } from "./EmptyState";

interface RecommendedActionsProps {
  actions?: string[];
  title?: string;
}

export function RecommendedActions({ actions, title = "Recommended next actions" }: RecommendedActionsProps) {
  const { t } = useI18n();
  const visibleTitle = title === "Recommended next actions" ? t("state.actions.title") : title;
  if (!actions || actions.length === 0) {
    return <EmptyState title={visibleTitle} message={t("state.actions.empty")} />;
  }

  return (
    <section className="recommended-actions" aria-label={visibleTitle}>
      <h3>{visibleTitle}</h3>
      <ul className="action-list">
        {actions.map((item) => (
          <li key={item}>{item}</li>
        ))}
      </ul>
    </section>
  );
}
