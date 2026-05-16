const SAFETY_COPY = [
  "No solver is executed by default.",
  "No external LLM is called by default.",
  "Preview artifacts are not production-grade physical validation.",
  "Formal convergence proof is not claimed.",
  "This UI does not control PyPI/TestPyPI publication or GitHub releases.",
];

interface SafetyNoticeProps {
  compact?: boolean;
}

export function SafetyNotice({ compact = false }: SafetyNoticeProps) {
  return (
    <section className={compact ? "safety-notice compact" : "safety-notice"} aria-label="Safety boundaries">
      <h2>{compact ? "Safety boundaries" : "Agent Studio safety boundaries"}</h2>
      <ul>
        {SAFETY_COPY.map((item) => (
          <li key={item}>{item}</li>
        ))}
      </ul>
    </section>
  );
}

export { SAFETY_COPY };
