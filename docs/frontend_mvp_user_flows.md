# Agent Studio Frontend MVP User Flows

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
