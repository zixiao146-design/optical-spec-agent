# Tool-call Reality Matrix

Current public prerelease: v0.9.0rc6. Current main development version:
`0.9.0rc7.dev0`.

This matrix records what the backend actually imports, calls, skips, or blocks.
It is intended to answer whether the Agent Studio sub-agents are real backend
functions or only frontend labels.

## Sub-agent Status

The current sub-agent roles are deterministic local roles represented in the
AgentTrace and AgentTaskSession builders:

| Role | Importable class? | Callable backend? | Executed in sample session? | Notes |
| --- | --- | --- | --- | --- |
| SpecAgent | no | yes, through `build_agent_task_session` / `build_agent_trace` | yes | Deterministic role, not an autonomous class. |
| MaterialAgent | no | yes, through local material catalog calls | yes | Uses `material_catalog.suggest`. |
| GeometryAgent | no | yes, through deterministic trace logic | yes | Produces scaffold-level geometry review. |
| AdapterAgent | no | yes, through adapter registry / preview planning | yes | Recommends open-source-first adapter paths. |
| WorkflowAgent | no | yes, through workflow-plan preview and calculators | yes | Does not execute solvers by default. |
| EvidenceAgent | no | yes, through validation evidence references | yes | Does not claim production-grade validation. |
| SafetyAgent | no | yes, through permission gates and ledger blocking | yes | Blocks solver/LLM/upload/tag/release by default. |
| RecommendationAgent | no | yes, through task-session recommendations | yes | Produces local next actions. |

Run `python scripts/audit_sub_agents.py` for the live audit. If
`OSA_SUB_AGENT_AUDIT_JSON=/tmp/audit.json` is set, the script writes a JSON
report.

For the fuller backend capability report, run
`python scripts/generate_backend_capability_report.py` or call
`GET /api/backend-capability-report`. That report records sub-agent execution,
internal tool calls, calculator reference-case status, design-case
cross-checks, and blocked external actions in one structured payload.

## Internal Python Tools

| Tool | Called? | Default allowed? | Status |
| --- | --- | --- | --- |
| `requirements.match_template` | yes | yes | Maps natural-language goals to deterministic design requirement templates. |
| `requirements.extract_optical_intent` | yes | yes | Produces optical language summary fields without external LLM calls. |
| `material_catalog.suggest` | yes | yes | Executes local preview material suggestions. |
| `example_registry.load` | yes when an example matches | yes | Loads repo-local JSON examples. |
| `agent_trace.build` | yes | yes | Builds deterministic eight-role trace. |
| `workflow_plan.preview` | yes | yes | Builds local no-execute workflow preview. |
| `adapter_preview.generate` | yes | yes | Generates preview scaffold metadata/content only. |
| `optics.thin_film.calculate` | yes through API | yes | Single-wavelength transfer-matrix preview. |
| `optics.thin_film.spectrum` | yes for coating goals | yes | Wavelength sweep and quarter-wave AR preview. |
| `optics.paraxial.thin_lens` | yes through API | yes | Single thin-lens preview. |
| `optics.paraxial.two_lens_relay` | yes for lens goals | yes | Two-lens relay / ABCD preview. |
| `optics.gaussian_beam.propagate` | yes through API | yes | Single-distance Gaussian beam preview. |
| `optics.gaussian_beam.series` | yes for Gaussian beam goals | yes | Propagation series and focus preview. |
| `optics.waveguide.v_number` | yes through API | yes | Single slab V-number estimate. |
| `optics.waveguide.sweep` | yes for waveguide goals | yes | V-number sweep and single-mode range preview. |
| `backend_capability_report.generate` | yes through smoke/report script and API | yes | Reports importable/callable/executed backend reality. |
| `design_case_cross_checks.run` | yes through smoke/report script and API | yes | Verifies examples map to expected calculator or adapter trace behavior. |

## External Solvers

External solvers may be detected for availability, but they are not executed by
default.

| Tool | Availability detection | Executed by default? |
| --- | --- | --- |
| Meep | Python import detection only | no |
| Gmsh | Python import / executable detection only | no |
| MPB | executable detection only | no |
| ElmerSolver | executable detection only | no |
| Optiland | Python import detection only | no |

## Blocked Controls

The following are not exposed as backend Agent Studio actions:

- TestPyPI upload
- PyPI publication
- git tag creation
- GitHub release creation
- external LLM calls
- external solver execution

## Safety Contract

- No solver is executed by default.
- No external LLM is called by default.
- No upload is performed.
- No tag is created.
- No release is created.
- Optical calculators are preview/design-assist only.
- Calculator quality fields and reference cases are sanity checks only.
- Backend capability reports and design case cross-checks are preview/design-assist evidence only.
- Source/monitor inference and missing-input diagnostics are internal Python
  calls: `optical_language.infer_source_monitor` and
  `optical_language.diagnose_missing_inputs`.
- Monitor definitions are preview metadata, not executed external solver monitor
  results.
- Production-grade physical validation is not claimed.
- Formal convergence proof is not claimed.
