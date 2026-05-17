import { BoundaryBadge } from "./BoundaryBadge";

export function QuickstartPanel() {
  return (
    <section className="quickstart-success" aria-label="Quickstart success criteria">
      <div className="page-title">
        <span>Expected success</span>
        <h3>Quickstart completion checklist</h3>
        <p>
          Use this as the first-run success state. Live API results may replace
          demo fixtures, but the safety boundaries stay the same.
        </p>
      </div>
      <ul className="check-list">
        <li>API connected.</li>
        <li>Package version 0.9.0rc7.dev0.</li>
        <li>api_contract_version 0.1.</li>
        <li>Spec parsed and validated, or demo fixture mode clearly labeled.</li>
        <li>Workflow plan generated as a preview.</li>
        <li>Adapter preview generated without solver execution.</li>
        <li>Validation evidence summary reviewed.</li>
        <li>Recommended next action shown.</li>
      </ul>
      <div className="boundary-row">
        <BoundaryBadge>No solver executed</BoundaryBadge>
        <BoundaryBadge>No external LLM called</BoundaryBadge>
        <BoundaryBadge tone="notice">Preview-only warnings visible</BoundaryBadge>
      </div>
    </section>
  );
}
