import type { ApiDiagnostic } from "../api/types";
import { useI18n } from "../i18n/useI18n";
import { EmptyState } from "./EmptyState";

interface DiagnosticsPanelProps {
  diagnostics?: ApiDiagnostic;
  title?: string;
}

function hasEntries(items?: string[]): boolean {
  return Array.isArray(items) && items.length > 0;
}

export function DiagnosticsPanel({ diagnostics, title = "Diagnostics" }: DiagnosticsPanelProps) {
  const { t } = useI18n();
  if (
    !diagnostics ||
    (!hasEntries(diagnostics.errors) &&
      !hasEntries(diagnostics.warnings) &&
      !hasEntries(diagnostics.missing_fields) &&
      !hasEntries(diagnostics.assumptions) &&
      !hasEntries(diagnostics.limitations))
  ) {
    return <EmptyState title={title} message={t("state.diagnostics.empty")} />;
  }

  const groups = [
    [t("state.diagnostics.errors"), diagnostics.errors],
    [t("state.diagnostics.warnings"), diagnostics.warnings],
    [t("state.diagnostics.missingFields"), diagnostics.missing_fields],
    [t("state.diagnostics.assumptions"), diagnostics.assumptions],
    [t("state.diagnostics.limitations"), diagnostics.limitations],
  ] as const;

  return (
    <section className="diagnostics-panel" aria-label={title}>
      <h3>{title}</h3>
      {groups.map(([label, items]) =>
        hasEntries(items) ? (
          <div className="diagnostic-group" key={label}>
            <strong>{label}</strong>
            <ul>
              {items.map((item) => (
                <li key={item}>{item}</li>
              ))}
            </ul>
          </div>
        ) : null,
      )}
    </section>
  );
}
