import { useI18n } from "../i18n/useI18n";
import { BoundaryBadge } from "./BoundaryBadge";

export const GUIDED_DEMO_STEPS = [
  {
    key: "loadExample",
    label: "Load example spec",
    endpoint: "examples/quickstart/nanoparticle_demo_spec.json",
    safety: "Demo fixture only; not live validation until submitted.",
  },
  {
    key: "parse",
    label: "Parse locally",
    endpoint: "POST /api/parse",
    safety: "No external LLM is called by default.",
  },
  {
    key: "validate",
    label: "Validate spec",
    endpoint: "POST /api/validate",
    safety: "Validation checks schema and completeness; it is not production-grade physical validation.",
  },
  {
    key: "adapterMatrix",
    label: "Review adapter matrix",
    endpoint: "GET /api/adapters",
    safety: "Adapter discovery is metadata-only.",
  },
  {
    key: "workflow",
    label: "Generate workflow plan",
    endpoint: "POST /api/workflow-plan",
    safety: "Workflow planning is preview-first with no solver execution.",
  },
  {
    key: "preview",
    label: "Preview artifact",
    endpoint: "POST /api/adapter-preview",
    safety: "Preview artifacts are not production-grade physical validation.",
  },
  {
    key: "evidence",
    label: "Review validation evidence",
    endpoint: "GET /api/validation-evidence",
    safety: "Formal convergence proof is not claimed.",
  },
  {
    key: "readiness",
    label: "Review readiness / next action",
    endpoint: "GET /api/readiness",
    safety: "This UI does not control PyPI/TestPyPI publication or GitHub releases.",
  },
];

export type GuidedDemoPage =
  | "Dashboard"
  | "Spec Input"
  | "Adapter Matrix"
  | "Workflow Plan"
  | "Artifact Preview"
  | "Validation Evidence"
  | "System Status";

interface GuidedDemoStepperProps {
  onNavigate?: (page: GuidedDemoPage) => void;
}

const STEP_PAGE: Record<string, GuidedDemoPage> = {
  "Load example spec": "Spec Input",
  "Parse locally": "Spec Input",
  "Validate spec": "Spec Input",
  "Review adapter matrix": "Adapter Matrix",
  "Generate workflow plan": "Workflow Plan",
  "Preview artifact": "Artifact Preview",
  "Review validation evidence": "Validation Evidence",
  "Review readiness / next action": "Dashboard",
};

const STEP_KEYS = {
  loadExample: {
    label: "guided.step.loadExample",
    safety: "guided.safety.fixture",
  },
  parse: {
    label: "guided.step.parse",
    safety: "guided.safety.parse",
  },
  validate: {
    label: "guided.step.validate",
    safety: "guided.safety.validate",
  },
  adapterMatrix: {
    label: "guided.step.adapterMatrix",
    safety: "guided.safety.adapters",
  },
  workflow: {
    label: "guided.step.workflow",
    safety: "guided.safety.workflow",
  },
  preview: {
    label: "guided.step.preview",
    safety: "guided.safety.preview",
  },
  evidence: {
    label: "guided.step.evidence",
    safety: "guided.safety.evidence",
  },
  readiness: {
    label: "guided.step.readiness",
    safety: "guided.safety.readiness",
  },
};

export function GuidedDemoStepper({ onNavigate }: GuidedDemoStepperProps) {
  const { t } = useI18n();
  return (
    <section className="guided-demo" aria-label={t("guided.title")}>
      <div className="page-title">
        <span>{t("guided.kicker")}</span>
        <h3>{t("guided.title")}</h3>
        <p>
          {t("guided.description")}
        </p>
      </div>
      <div className="boundary-row">
        <BoundaryBadge>{t("guided.badge.noSolver")}</BoundaryBadge>
        <BoundaryBadge>{t("guided.badge.noLlm")}</BoundaryBadge>
        <BoundaryBadge tone="notice">{t("guided.badge.noControls")}</BoundaryBadge>
      </div>
      <ol className="guided-step-list">
        {GUIDED_DEMO_STEPS.map((step) => (
          <li key={step.label}>
            <div>
              <strong>{t(STEP_KEYS[step.key as keyof typeof STEP_KEYS].label)}</strong>
              <code>{step.endpoint}</code>
              <p>{t(STEP_KEYS[step.key as keyof typeof STEP_KEYS].safety)}</p>
            </div>
            {onNavigate ? (
              <button
                type="button"
                className="secondary-button"
                onClick={() => onNavigate(STEP_PAGE[step.label] || "Dashboard")}
              >
                {t("guided.openStep")}
              </button>
            ) : null}
          </li>
        ))}
      </ol>
    </section>
  );
}
