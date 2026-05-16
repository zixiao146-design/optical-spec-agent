interface ApiDisconnectedNoticeProps {
  message?: string;
}

export function ApiDisconnectedNotice({
  message = "The local Agent API is not reachable. Demo fixture mode is showing bundled frontend fixtures; this is not live validation.",
}: ApiDisconnectedNoticeProps) {
  return (
    <div className="state-box api-disconnected" role="status" aria-live="polite">
      <strong>API disconnected: demo fixture mode</strong>
      <span>{message}</span>
      <span>No solver is executed, no external LLM is called, and no live validation is performed in demo mode.</span>
    </div>
  );
}
