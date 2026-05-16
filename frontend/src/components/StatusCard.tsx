interface StatusCardProps {
  label: string;
  value: string;
  note?: string;
}

export function StatusCard({ label, value, note }: StatusCardProps) {
  return (
    <div className="status-card">
      <span className="status-label">{label}</span>
      <strong>{value}</strong>
      {note ? <span className="status-note">{note}</span> : null}
    </div>
  );
}
