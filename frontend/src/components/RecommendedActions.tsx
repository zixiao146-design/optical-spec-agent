import { EmptyState } from "./EmptyState";

interface RecommendedActionsProps {
  actions?: string[];
  title?: string;
}

export function RecommendedActions({ actions, title = "Recommended next actions" }: RecommendedActionsProps) {
  if (!actions || actions.length === 0) {
    return <EmptyState title={title} message="No recommended next actions were returned." />;
  }

  return (
    <section className="recommended-actions" aria-label={title}>
      <h3>{title}</h3>
      <ul className="action-list">
        {actions.map((item) => (
          <li key={item}>{item}</li>
        ))}
      </ul>
    </section>
  );
}
