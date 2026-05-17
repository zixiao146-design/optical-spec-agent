# Agent Studio Frontend MVP User Flows

## User Flow 0: Natural language goal to Agent Task Session

- User action: open Agent Command Center and enter a natural language optical
  design goal.
- API call: `POST /api/agent-session`.
- Expected response: optical intent summary, selected design case, plan steps,
  sub-agent trace, permission gates, artifacts, evidence, and recommended next
  actions.
- UI state: show a command-center task session with plan, blocked gates, local
  artifacts, final recommendation, diagnostics, and raw JSON.
- Safety boundary copy: "No external solver, external LLM, upload, tag, or
  release action is performed."

## User Flow 1: Natural language spec to preview artifact

- User action: paste a natural language optical task.
- API call: `POST /api/parse`.
- Expected response: parsed spec, diagnostics, assumptions, and recommended
  next actions.
- UI state: show parsed spec and diagnostic review panel.
- Safety boundary copy: "No external LLM was called."
- User action: validate parsed or edited spec.
- API call: `POST /api/validate`.
- Expected response: validation status, warnings, errors, and missing fields.
- UI state: show validation state and safe next step.
- Safety boundary copy: "No production-grade physical validation is claimed."
- User action: generate local workflow plan.
- API call: `POST /api/workflow-plan`.
- Expected response: workflow steps, risk flags, limitations, and public keys.
- UI state: show ordered workflow plan.
- Safety boundary copy: "No solver was executed."
- User action: preview adapter artifact.
- API call: `POST /api/adapter-preview`.
- Expected response: preview content and artifact summary.
- UI state: show generated preview in a read-only code pane.
- Safety boundary copy: "Preview artifact only."

## User Flow 2: JSON spec to adapter preview

- User action: paste JSON spec or select a local fixture.
- API call: `POST /api/validate`.
- Expected response: valid/needs-review status and diagnostics.
- UI state: show validation result next to the JSON editor.
- Safety boundary copy: "Formal convergence proof is not claimed."
- User action: inspect available adapters.
- API call: `GET /api/adapters`.
- Expected response: adapter registry summaries and maturity levels.
- UI state: show adapter matrix with status and limitations.
- Safety boundary copy: "No solver was executed."
- User action: preview selected adapter output.
- API call: `POST /api/adapter-preview`.
- Expected response: preview content and artifact summary.
- UI state: show preview content with warnings and limitations.
- Safety boundary copy: "Preview artifact only."

## User Flow 3: Readiness and evidence review

- User action: open dashboard.
- API call: `GET /api/readiness`.
- Expected response: public prerelease, main development version, PyPI/TestPyPI
  status, public contract freeze status, and recommended next actions.
- UI state: show release/readiness summary.
- Safety boundary copy: "No PyPI or TestPyPI upload control is available in
  this MVP."
- User action: inspect validation evidence.
- API call: `GET /api/validation-evidence`.
- Expected response: evidence entries for Gmsh, Meep, MPB, Optiland, and Elmer
  deferred status.
- UI state: show evidence cards and report links.
- Safety boundary copy: "No production-grade physical validation is claimed."
- User action: review publication status.
- API call: `GET /api/readiness`.
- Expected response: PyPI published false, TestPyPI verified only for
  0.9.0rc6.dev0, and v1.0.0 not released.
- UI state: show publication gates as read-only status.
- Safety boundary copy: "No solver was executed."

## User Flow 4: Optical design orientation and sub-agent trace

- User action: open Example Gallery and choose `nanoparticle_plasmonics`.
- API call: `GET /api/examples`, `GET /api/examples/{example_id}`.
- Expected response: local example summary, spec, expected agent trace, material hints, adapter recommendation, workflow focus, and next actions.
- UI state: show example cards and selected detail payload.
- Safety boundary copy: "Examples are local preview workflows; no solver is executed."
- User action: open Material Library and inspect a local preview material.
- API call: `GET /api/materials`.
- Expected response: local preview material catalog and warning that material
  data is not production-grade optical constants.
- UI state: show searchable material cards and preview-only boundary.
- Safety boundary copy: "Material data is a local preview catalog, not production-grade optical constants."
- User action: request materials for nanoparticle plasmonics.
- API call: `POST /api/materials/suggest`.
- Expected response: preview material suggestions such as Au, Ag, SiO2, water, and air.
- UI state: show suggested materials and verification reminder.
- Safety boundary copy: "No external material database lookup was performed."
- User action: open Agent Collaboration and generate the example Agent Trace Timeline.
- API call: `POST /api/examples/{example_id}/agent-trace`.
- Expected response: SpecAgent, MaterialAgent, GeometryAgent, AdapterAgent,
  WorkflowAgent, EvidenceAgent, SafetyAgent, and RecommendationAgent steps with
  input summaries, output summaries, diagnostics, evidence refs, safety notes,
  and recommendations.
- UI state: show Agent Trace Timeline and final recommendation.
- Safety boundary copy: "Sub-agent collaboration is a local deterministic trace."
