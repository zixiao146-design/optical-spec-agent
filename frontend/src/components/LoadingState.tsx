interface LoadingStateProps {
  label?: string;
}

export function LoadingState({ label = "Loading local Agent API response..." }: LoadingStateProps) {
  return (
    <div className="state-box loading-state" role="status" aria-live="polite">
      <span className="spinner" aria-hidden="true" />
      <span>{label}</span>
    </div>
  );
}
