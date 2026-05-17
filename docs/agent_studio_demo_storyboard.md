# Agent Studio Demo Storyboard

Narrative: start from readiness, enter or load a spec, validate the spec,
choose an adapter, generate a workflow plan, preview an artifact, review
validation evidence, and end with publication/readiness status. The demo should
feel like an agent-like workflow while staying local-first, open-source-solver-first,
preview-first, and conservative about validation claims.
Use `docs/quickstart.md`, `docs/quickstart.zh-CN.md`, and the frontend
`Start guided demo` panel for the first-time user path.
Each scene includes a safety note for the maintainer to point out.

| Scene | Page | Action | Expected UI | API endpoint used | Speaker note | Safety note |
|---|---|---|---|---|---|---|
| 1 | Dashboard / Readiness | Open the app. | Current public prerelease, main dev version, API contract version, TestPyPI/PyPI status, and next actions appear. | `GET /api/readiness`, `GET /api/version`, `GET /api/health` | "Start from readiness: the agent tells us where the project stands before doing work." | No upload, tag, or release controls are present. |
| 2 | Spec Input | Load an example spec or paste a natural-language request. | Demo fixture loaded copy appears until the user submits. | None until submit; then `POST /api/parse` | "The frontend can stage a request without pretending the fixture is live validation." | No external LLM is called by default. |
| 3 | Spec Input | Validate the JSON spec. | Validation result, diagnostics, and raw JSON appear. | `POST /api/validate` | "The agent checks schema and diagnostics locally." | No production-grade physical validation is claimed. |
| 4 | Adapter Matrix | Review adapter choices. | Gmsh, Meep, MPB, Optiland, and Elmer are visible with maturity/evidence context. | `GET /api/adapters`, `GET /api/validation-evidence` | "The agent shows what it can target and what evidence exists." | Elmer remains deferred; adapters are not executed. |
| 5 | Workflow Plan | Load the workflow fixture and generate a plan. | Workflow plan steps, diagnostics, and safety flags appear. | `POST /api/workflow-plan` | "The agent plans the work before touching any solver." | No solver is executed by default. |
| 6 | Artifact Preview | Choose an adapter and generate preview. | Preview content or artifact summary appears. | `POST /api/adapter-preview` | "The agent previews an artifact for inspection." | Preview artifact only; formal convergence proof is not claimed. |
| 7 | Validation Evidence | Open evidence view. | Validation evidence and limitation boundaries appear. | `GET /api/validation-evidence` | "The agent separates evidence from overclaiming." | Level 3 evidence is manual/optional; not production-grade validation. |
| 8 | System Status | Open system status. | Health, schema, version, and API base are visible. | `GET /api/health`, `GET /api/version`, `GET /api/schema` | "End by confirming the local system state." | PyPI remains unpublished; no publication action is available. |

The demo should highlight local-first operation, no-default solver/LLM behavior,
open-source-solver-first strategy, preview-first artifact generation, and the
absence of production-grade physical validation or formal convergence claims.
