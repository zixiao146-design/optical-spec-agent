import { useMemo, useState } from "react";
import { useI18n } from "../i18n/useI18n";
import { BoundaryBadge } from "./BoundaryBadge";

export const CHINESE_GUIDED_TUTORIAL_STEPS = [
  {
    key: "open",
    endpoint: "GET /api/health",
    title: "guidedTutorial.step.open.title",
    action: "guidedTutorial.step.open.action",
    expected: "guidedTutorial.step.open.expected",
    safety: "guidedTutorial.step.open.safety",
  },
  {
    key: "status",
    endpoint: "GET /api/readiness, GET /api/version, GET /api/health",
    title: "guidedTutorial.step.status.title",
    action: "guidedTutorial.step.status.action",
    expected: "guidedTutorial.step.status.expected",
    safety: "guidedTutorial.step.status.safety",
  },
  {
    key: "loadChinese",
    endpoint: "examples/quickstart/zh_nanoparticle_prompt.txt",
    title: "guidedTutorial.step.loadChinese.title",
    action: "guidedTutorial.step.loadChinese.action",
    expected: "guidedTutorial.step.loadChinese.expected",
    safety: "guidedTutorial.step.loadChinese.safety",
  },
  {
    key: "parse",
    endpoint: "POST /api/parse",
    title: "guidedTutorial.step.parse.title",
    action: "guidedTutorial.step.parse.action",
    expected: "guidedTutorial.step.parse.expected",
    safety: "guidedTutorial.step.parse.safety",
  },
  {
    key: "validate",
    endpoint: "POST /api/validate",
    title: "guidedTutorial.step.validate.title",
    action: "guidedTutorial.step.validate.action",
    expected: "guidedTutorial.step.validate.expected",
    safety: "guidedTutorial.step.validate.safety",
  },
  {
    key: "adapters",
    endpoint: "GET /api/adapters, GET /api/validation-evidence",
    title: "guidedTutorial.step.adapters.title",
    action: "guidedTutorial.step.adapters.action",
    expected: "guidedTutorial.step.adapters.expected",
    safety: "guidedTutorial.step.adapters.safety",
  },
  {
    key: "workflow",
    endpoint: "POST /api/workflow-plan",
    title: "guidedTutorial.step.workflow.title",
    action: "guidedTutorial.step.workflow.action",
    expected: "guidedTutorial.step.workflow.expected",
    safety: "guidedTutorial.step.workflow.safety",
  },
  {
    key: "preview",
    endpoint: "POST /api/adapter-preview",
    title: "guidedTutorial.step.preview.title",
    action: "guidedTutorial.step.preview.action",
    expected: "guidedTutorial.step.preview.expected",
    safety: "guidedTutorial.step.preview.safety",
  },
  {
    key: "evidence",
    endpoint: "GET /api/validation-evidence, GET /api/readiness",
    title: "guidedTutorial.step.evidence.title",
    action: "guidedTutorial.step.evidence.action",
    expected: "guidedTutorial.step.evidence.expected",
    safety: "guidedTutorial.step.evidence.safety",
  },
] as const;

export function ChineseGuidedTutorial() {
  const { t } = useI18n();
  const [completed, setCompleted] = useState<string[]>([]);
  const completedSet = useMemo(() => new Set(completed), [completed]);

  function toggleCompleted(stepKey: string) {
    setCompleted((current) => (
      current.includes(stepKey)
        ? current.filter((key) => key !== stepKey)
        : [...current, stepKey]
    ));
  }

  return (
    <section
      className="guided-tutorial page-panel wide"
      aria-label={t("guidedTutorial.title")}
      data-tutorial-name="中文手把手教程"
    >
      <div className="page-title">
        <span>{t("guidedTutorial.kicker")}</span>
        <h3>{t("guidedTutorial.title")}</h3>
        <p>{t("guidedTutorial.description")}</p>
      </div>

      <div className="tutorial-progress" aria-live="polite">
        <strong>{t("guidedTutorial.progress")}:</strong>{" "}
        {completed.length}/{CHINESE_GUIDED_TUTORIAL_STEPS.length}
      </div>

      <ol className="tutorial-step-list">
        {CHINESE_GUIDED_TUTORIAL_STEPS.map((step, index) => {
          const isComplete = completedSet.has(step.key);
          return (
            <li key={step.key} className={isComplete ? "complete" : ""}>
              <div className="tutorial-step-heading">
                <span>{index + 1}</span>
                <h4>{t(step.title)}</h4>
              </div>
              <dl>
                <dt>{t("guidedTutorial.actionLabel")}</dt>
                <dd>{t(step.action)}</dd>
                <dt>{t("guidedTutorial.expectedLabel")}</dt>
                <dd>{t(step.expected)}</dd>
                <dt>{t("guidedTutorial.endpointLabel")}</dt>
                <dd><code>{step.endpoint}</code></dd>
                <dt>{t("guidedTutorial.safetyLabel")}</dt>
                <dd>{t(step.safety)}</dd>
              </dl>
              <button
                type="button"
                className="secondary-button"
                onClick={() => toggleCompleted(step.key)}
                aria-pressed={isComplete}
              >
                {isComplete ? t("guidedTutorial.completed") : t("guidedTutorial.markComplete")}
              </button>
            </li>
          );
        })}
      </ol>

      <div className="boundary-row">
        <BoundaryBadge>{t("safety.noSolverDefault")}</BoundaryBadge>
        <BoundaryBadge>{t("safety.noExternalLlmDefault")}</BoundaryBadge>
        <BoundaryBadge tone="notice">{t("safety.noPublicationControls")}</BoundaryBadge>
        <BoundaryBadge>{t("safety.previewNotProduction")}</BoundaryBadge>
        <BoundaryBadge>{t("safety.noConvergenceProof")}</BoundaryBadge>
      </div>
    </section>
  );
}
