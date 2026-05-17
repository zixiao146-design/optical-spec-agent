interface JsonPanelProps {
  title: string;
  value: unknown;
  initiallyOpen?: boolean;
}

function hasJsonValue(value: unknown): boolean {
  if (value === null || value === undefined) return false;
  if (typeof value === "object" && Object.keys(value as Record<string, unknown>).length === 0) return false;
  return true;
}

export function JsonPanel({ title, value, initiallyOpen = true }: JsonPanelProps) {
  if (!hasJsonValue(value)) {
    return (
      <section className="json-panel" aria-label={title}>
        <div className="panel-heading">
          <h3>{title}</h3>
        </div>
        <p className="muted">No JSON payload is available yet.</p>
      </section>
    );
  }

  return (
    <section className="json-panel" aria-label={title}>
      <details open={initiallyOpen}>
        <summary className="panel-heading">
          <h3>{title}</h3>
        </summary>
        <pre>{JSON.stringify(value, null, 2)}</pre>
      </details>
    </section>
  );
}
