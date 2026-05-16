interface JsonPanelProps {
  title: string;
  value: unknown;
}

export function JsonPanel({ title, value }: JsonPanelProps) {
  return (
    <section className="json-panel" aria-label={title}>
      <div className="panel-heading">
        <h3>{title}</h3>
      </div>
      <pre>{JSON.stringify(value, null, 2)}</pre>
    </section>
  );
}
