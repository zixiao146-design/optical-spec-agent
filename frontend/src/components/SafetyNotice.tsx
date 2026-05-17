import { useI18n } from "../i18n/useI18n";

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
  const { t } = useI18n();
  const safetyCopy = [
    t("safety.noSolverDefault"),
    t("safety.noExternalLlmDefault"),
    t("safety.previewNotProduction"),
    t("safety.noConvergenceProof"),
    t("safety.noPublicationControls"),
  ];
  return (
    <section className={compact ? "safety-notice compact" : "safety-notice"} aria-label={t("safety.aria")}>
      <h2>{compact ? t("safety.compactTitle") : t("safety.title")}</h2>
      <ul>
        {safetyCopy.map((item) => (
          <li key={item}>{item}</li>
        ))}
      </ul>
    </section>
  );
}

export { SAFETY_COPY };
