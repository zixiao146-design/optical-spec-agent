import { BoundaryBadge } from "./BoundaryBadge";

export const GUIDED_DEMO_STEPS = [
  {
    label: "Load example spec",
    endpoint: "examples/quickstart/nanoparticle_demo_spec.json",
    safety: "Demo fixture only; not live validation until submitted.",
  },
  {
    label: "Parse locally",
    endpoint: "POST /api/parse",
    safety: "No external LLM is called by default.",
  },
  {
    label: "Validate spec",
    endpoint: "POST /api/validate",
    safety: "Validation checks schema and completeness; it is not production-grade physical validation.",
  },
  {
    label: "Review adapter matrix",
    endpoint: "GET /api/adapters",
    safety: "Adapter discovery is metadata-only.",
  },
  {
    label: "Generate workflow plan",
    endpoint: "POST /api/workflow-plan",
    safety: "Workflow planning is preview-first with no solver execution.",
  },
  {
    label: "Preview artifact",
    endpoint: "POST /api/adapter-preview",
    safety: "Preview artifacts are not production-grade physical validation.",
  },
  {
    label: "Review validation evidence",
    endpoint: "GET /api/validation-evidence",
    safety: "Formal convergence proof is not claimed.",
  },
  {
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

export function GuidedDemoStepper({ onNavigate }: GuidedDemoStepperProps) {
  return (
    <section className="guided-demo" aria-label="Guided quickstart demo">
      <div className="page-title">
        <span>Quickstart demo</span>
        <h3>Start guided demo</h3>
        <p>
          Follow the local-first agent workflow from example spec to readiness
          status. Each step points to the API surface used by the frontend and
          keeps preview boundaries visible.
        </p>
      </div>
      <div className="boundary-row">
        <BoundaryBadge>No solver is executed by default</BoundaryBadge>
        <BoundaryBadge>No external LLM is called by default</BoundaryBadge>
        <BoundaryBadge tone="notice">No upload, tag, or release controls</BoundaryBadge>
      </div>
      <ol className="guided-step-list">
        {GUIDED_DEMO_STEPS.map((step) => (
          <li key={step.label}>
            <div>
              <strong>{step.label}</strong>
              <code>{step.endpoint}</code>
              <p>{step.safety}</p>
            </div>
            {onNavigate ? (
              <button
                type="button"
                className="secondary-button"
                onClick={() => onNavigate(STEP_PAGE[step.label] || "Dashboard")}
              >
                Open step
              </button>
            ) : null}
          </li>
        ))}
      </ol>
    </section>
  );
}
