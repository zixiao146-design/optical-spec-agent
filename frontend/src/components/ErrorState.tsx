interface ErrorStateProps {
  title?: string;
  message: string;
  actions?: string[];
}

export function ErrorState({
  title = "Unable to complete this local API action",
  message,
  actions = ["Check the request payload and try again."],
}: ErrorStateProps) {
  return (
    <div className="state-box error-state" role="alert" aria-live="assertive">
      <strong>{title}</strong>
      <span>{message}</span>
      {actions.length > 0 ? (
        <ul>
          {actions.map((action) => (
            <li key={action}>{action}</li>
          ))}
        </ul>
      ) : null}
    </div>
  );
}
