import type { ApiDiagnostic } from "../api/types";
import { EmptyState } from "./EmptyState";

interface DiagnosticsPanelProps {
  diagnostics?: ApiDiagnostic;
  title?: string;
}

function hasEntries(items?: string[]): boolean {
  return Array.isArray(items) && items.length > 0;
}

export function DiagnosticsPanel({ diagnostics, title = "Diagnostics" }: DiagnosticsPanelProps) {
  if (
    !diagnostics ||
    (!hasEntries(diagnostics.errors) &&
      !hasEntries(diagnostics.warnings) &&
      !hasEntries(diagnostics.missing_fields) &&
      !hasEntries(diagnostics.assumptions) &&
      !hasEntries(diagnostics.limitations))
  ) {
    return <EmptyState title={title} message="No diagnostics reported for this response." />;
  }

  const groups = [
    ["Errors", diagnostics.errors],
    ["Warnings", diagnostics.warnings],
    ["Missing fields", diagnostics.missing_fields],
    ["Assumptions", diagnostics.assumptions],
    ["Limitations", diagnostics.limitations],
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
