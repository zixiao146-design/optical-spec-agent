# optical-spec-agent

[English](README.md) | [简体中文](README.zh-CN.md)

[![CI](https://github.com/zixiao146-design/optical-spec-agent/actions/workflows/ci.yml/badge.svg)](https://github.com/zixiao146-design/optical-spec-agent/actions/workflows/ci.yml)

> Open-source-solver-first optical simulation workflow agent: convert optical
> simulation requests into validated spec JSON and generate inspectable,
> solver-native input scaffolds.

**optical-spec-agent** is an open-source-solver-first compilation layer between human language and optical solvers. You describe a simulation task in plain text (Chinese or English), and it produces a single structured, validated JSON spec — with typed fields, provenance tracking, and completeness checks. Its strongest workflow is still Meep nanoparticle-on-film script generation, and v0.7 adds a small multi-solver adapter foundation for MPB, Gmsh, Elmer, and Optiland preview scaffolds.

```
"用Meep FDTD仿真金纳米球-金膜gap plasmon，扫gap从5到25nm，提取共振波长和FWHM"
                                    ↓
                        OpticalSpec (JSON)
                     ┌─────────────────────┐
                     │ task, physics,       │
                     │ geometry_material,   │
                     │ simulation, output   │
                     │ + validation status  │
                     └─────────────────────┘
```

It is **not** a solver. By default it generates specs and scripts. v0.5 adds
an optional harness that can run an existing generated Meep script when Meep is
installed and write auditable execution artifacts, but this is not full solver
automation or production-grade physical validation.

Default quickstart and release validation do not require Zemax, Lumerical,
COMSOL, or proprietary Ansys tools. External solvers are optional and not run by
default. External LLM access is optional and not required by default.

## Quickstart

For a polished first-run local Agent Studio walkthrough, use
[`docs/quickstart.md`](docs/quickstart.md):

```bash
./scripts/bootstrap_demo_env.sh
source /tmp/osa-agent-studio-demo/bin/activate
./scripts/run_quickstart_demo.sh
```

The quickstart opens Agent Studio at `http://127.0.0.1:5173` and the Local
Agent API docs at `http://127.0.0.1:8000/docs`. It guides a first-time user
through loading an example spec, parsing locally, validating, viewing the
adapter matrix, generating a workflow plan, previewing an artifact, reviewing
validation evidence, and reading readiness / next actions. It remains
local-first and does not upload packages, create tags/releases, execute solvers
by default, call external LLMs by default, claim production-grade physical
validation, or claim formal convergence proof.

Agent Studio now supports English / Chinese UI switching. Chinese browser
environments default to Chinese, and users can switch languages in the sidebar.
The API JSON field names, adapter tool names, package metadata, and
`api_contract_version` remain stable English contract fields. See
[`docs/frontend_i18n_zh_CN.md`](docs/frontend_i18n_zh_CN.md) and the Chinese
quickstart prompt at
[`examples/quickstart/zh_nanoparticle_prompt.txt`](examples/quickstart/zh_nanoparticle_prompt.txt).
The Chinese step-by-step tutorial is tracked in
[`docs/agent_studio_chinese_guided_tutorial.md`](docs/agent_studio_chinese_guided_tutorial.md),
with terminology in
[`docs/frontend_chinese_terminology.md`](docs/frontend_chinese_terminology.md).

The current domain expansion adds an Agent Studio
[`Example Gallery`](docs/example_gallery.md), a local preview
[`material library`](docs/material_library.md), richer
[`optical design examples`](examples/optical_design/), and a deterministic
[`Agent Trace Timeline`](docs/agent_trace_timeline.md) /
[`sub-agent collaboration trace`](docs/sub_agent_architecture.md) that makes
SpecAgent, MaterialAgent, GeometryAgent, AdapterAgent, WorkflowAgent,
EvidenceAgent, SafetyAgent, and RecommendationAgent visible in Agent Studio.
The new [`Agent Command Center`](docs/agent_command_center.md) turns a natural
language optical design goal into a deterministic local task session with
optical intent, design case, agent plan, permission gates, artifacts, evidence,
and recommended next actions.
The backend now also records a
[`tool-call reality matrix`](docs/tool_call_reality_matrix.md), live
[`backend functionality status`](docs/backend_functionality_status.md),
generated [`backend capability report`](docs/backend_capability_report.md),
maintainer [`backend evidence review pack`](docs/backend_evidence_review_pack.md),
[`backend validation maturity matrix`](docs/backend_validation_maturity_matrix.md),
[`preview boundary policy`](docs/preview_boundary_policy.md),
[`optional solver-backed micro-benchmark plan`](docs/solver_validation_micro_benchmarks.md),
[`design case cross-checks`](docs/design_case_cross_checks.md), and
local preview [`optical calculators`](docs/optical_calculators.md) for
thin-film stacks, paraxial lenses, Gaussian beams, waveguide V-number,
fiber coupling mode overlap, and Jones-calculus polarization
estimates. The calculator layer now includes case-oriented helpers for thin-film
spectra, quarter-wave AR coatings, Gaussian beam series/focus estimates,
paraxial systems and two-lens relays, and waveguide sweeps/single-mode range
estimates, plus
[`fiber coupling`](docs/fiber_coupling_preview_calculator.md) and
[`polarization`](docs/polarization_preview_calculator.md) preview helpers; see
[`optical calculator case integration`](docs/optical_calculator_case_integration.md).
Reference sanity cases and response quality fields are documented in
[`optical calculator reference cases`](docs/optical_calculator_reference_cases.md),
with dedicated
[`fiber/polarization reference cases`](docs/fiber_polarization_reference_cases.md)
covering Gaussian mode overlap and Jones-calculus sanity checks.
These calculators are design-assist previews only; they do not run external
solvers, call external LLMs, or claim production-grade validation.
The capability report proves which sub-agents and internal tools execute in
sample sessions, which calculators are sanity-checked previews, and which
external solver/LLM/upload/tag/release actions remain blocked.
The validation maturity matrix classifies calculators, materials, application
domains, adapter metadata, sub-agent sessions, and the frontend UI/demo surface
without upgrading any of them into production-grade physical validation or
formal convergence claims.
The optional solver-backed micro-benchmark plan provides a disciplined manual
path for tiny open-source solver checks, but `scripts/run_optional_solver_micro_benchmarks.sh`
is default no-execute and requires explicit `OSA_RUN_OPTIONAL_*_VALIDATION=1`
approval before any solver-backed run.
The readiness layer adds
[`optional solver approval matrix`](docs/optional_solver_micro_benchmark_approval_matrix.md),
[`approval record template`](docs/optional_solver_micro_benchmark_approval_record_template.md),
[`execution approval packet`](docs/optional_solver_micro_benchmark_execution_packet.md),
[`execution sequence`](docs/optional_solver_execution_sequence.md), and
`scripts/check_optional_solver_readiness.py` so maintainers can review
availability, expected artifacts, risks, and the required approval phrase
before any solver execution. This readiness check does not authorize
PyPI/TestPyPI upload, tag creation, or GitHub release creation.
Per-solver approval records live under
[`docs/optional_solver_approval_records/`](docs/optional_solver_approval_records/);
the approved Gmsh-only 2026-05-20 run is recorded there and summarized in
[`validation/gmsh/gmsh_micro_benchmark_2026-05-20.md`](validation/gmsh/gmsh_micro_benchmark_2026-05-20.md).
The maintainer review accepted it only as optional manual mesh-generation smoke
evidence; it did not authorize any further solver execution. The separately
approved Optiland-only 2026-05-20 run is recorded in
[`validation/optiland/optiland_micro_benchmark_2026-05-20.md`](validation/optiland/optiland_micro_benchmark_2026-05-20.md)
and reviewed in
[`docs/optional_solver_approval_records/optiland_micro_benchmark_review_2026-05-20.md`](docs/optional_solver_approval_records/optiland_micro_benchmark_review_2026-05-20.md)
as optional manual ray/path smoke evidence only. Meep, MPB, and Elmer remain
not executed by these tasks and require separate approval; Gmsh and Optiland
reruns also require separate approval.
The Meep decision packet
[`meep_micro_benchmark_decision_packet.md`](docs/optional_solver_approval_records/meep_micro_benchmark_decision_packet.md)
records the required `OSA_SOLVER_PYTHON` profile, approval phrase, expected
future command, artifacts, and non-claims while keeping Meep pending/not run.
Readiness is environment-aware: the default profile uses the current Python and
current `PATH`, while `OSA_SOLVER_PYTHON` can probe a dedicated solver Python
such as `osa-solvers` for PyMeep and `meep.mpb`; see
[`optional solver environment profiles`](docs/optional_solver_environment_profiles.md).
The evidence pack can be generated with
`python scripts/generate_backend_evidence_pack.py --json-out /tmp/osa-backend-evidence-pack.json --markdown-out /tmp/osa-backend-evidence-pack.md`
or smoke-checked with `./scripts/smoke_backend_evidence_pack.sh`; it is a
maintainer review artifact only, not a release, upload, tag, or publication
action.
The maintainer
[`backend evidence review decision`](docs/backend_evidence_review_decision.md)
recorded backend evidence as sufficient for the `v0.9.0rc7` release draft,
which has now been published as the current GitHub prerelease. PyPI
publication, TestPyPI upload for `0.9.0rc8.dev0`, a future `v0.9.0rc8` tag,
and `v1.0.0` approval remain separate and not granted.
The backend also includes
[`design requirement templates`](docs/design_requirement_templates.md) and a
[`natural language to optical language`](docs/natural_language_to_optical_language.md)
mapping layer. These deterministic templates connect first-run goals to optical
intent, required inputs, default assumptions, material/geometry choices,
expected calculators or adapters, tool-call ledger entries, and preview
artifacts without using an external LLM.
The rc8.dev0 backend now makes material provenance and ambiguous requirement
handling explicit through
[`material provenance policy`](docs/material_provenance_policy.md),
[`ambiguous requirement matching`](docs/ambiguous_requirement_matching.md), and
[`missing-input diagnostics`](docs/missing_input_diagnostics.md). Material
records expose provenance, suitability warnings, and user-verification flags;
ambiguous goals produce candidate templates and questions rather than unsafe
solver actions. The material catalog remains preview/design-assist only and is
not a production-grade optical constants database.
The backend also records an
[`application domain registry`](docs/application_domain_registry.md) and
[`material-template cross-checks`](docs/material_template_cross_checks.md),
connecting ten optical domains to local materials, requirement templates,
calculators/adapters, missing-input questions, and preview-only evidence
boundaries.
Those domains are now benchmarked by
[`application domain benchmarks`](docs/application_domain_benchmarks.md), a
local scenario suite covering positive, ambiguous, underconstrained,
unsupported, and unsafe/blocked optical-design requests. The evaluator checks
expected domain/template matching, material/calculator/adapter behavior,
missing-input questions, and blocked actions without running solvers or calling
external LLMs. The former fiber coupling and polarization warning scenarios now
pass through deterministic preview calculators, while real coupling validation
and vector EM polarization validation remain outside the default backend path.
The gallery connects examples to material suggestions, adapter recommendations,
workflow planning, artifact preview, evidence, and next actions.
These additions remain preview-first: no solver is executed by default, no
external LLM is called by default, material values are not production-grade
optical constants, and PyPI/TestPyPI upload or GitHub tag/release controls are
not exposed.

Release status: the current public release candidate is `v0.9.0rc7`, while the
current `main` development version is `0.9.0rc8.dev0`. The `v0.9.0rc8` tag has
not been created, no `v0.9.0rc8` GitHub release exists, and `0.9.0rc8.dev0` is
not a public release.
It includes v0.6 local/manual diagnostics, v0.7 multi-solver adapter MVP
scaffolds, v0.8 LLM parser foundation work, and v0.9 synchronous workflow
orchestration foundation work as preview/scaffold/evaluation capabilities.
The `v0.9.0rc7` git tag and GitHub prerelease were created after maintainer
review and supersede `v0.9.0rc6` as the current release candidate. PyPI remains
unpublished. TestPyPI upload completed for `0.9.0rc6.dev0` through manual
Trusted Publishing, but TestPyPI upload for `0.9.0rc8.dev0` has not been performed;
this repository state is not a final stable `1.0` release, and PyPI
publication remains separately gated.
See [`docs/versioning_policy.md`](docs/versioning_policy.md) and
[`docs/release_readiness_current.md`](docs/release_readiness_current.md) for the
current release policy and release-readiness matrix. Use
[`docs/release_engineering_playbook.md`](docs/release_engineering_playbook.md)
for the repeatable RC procedure and
[`docs/v1_0_readiness_plan.md`](docs/v1_0_readiness_plan.md) for the path from
the current RC line toward `v1.0`.
Current rc8 development readiness and publication gates are tracked in
[`docs/release_readiness_v0.9.0rc8.md`](docs/release_readiness_v0.9.0rc8.md),
[`docs/rc8_backend_roadmap.md`](docs/rc8_backend_roadmap.md),
[`docs/rc8_capability_gap_audit.md`](docs/rc8_capability_gap_audit.md),
[`docs/rc8_to_v1_0_decision_path.md`](docs/rc8_to_v1_0_decision_path.md),
[`docs/testpypi_upload_approval_v0.9.0rc8.dev0.md`](docs/testpypi_upload_approval_v0.9.0rc8.dev0.md),
while rc7 release records remain in
[`docs/release_readiness_v0.9.0rc7.md`](docs/release_readiness_v0.9.0rc7.md),
[`docs/testpypi_upload_approval_v0.9.0rc7.md`](docs/testpypi_upload_approval_v0.9.0rc7.md),
[`docs/post_release_status_v0.9.0rc7.md`](docs/post_release_status_v0.9.0rc7.md),
and the historical rc6 release documents:
[`docs/release_readiness_v0.9.0rc6.md`](docs/release_readiness_v0.9.0rc6.md),
[`docs/github_release_draft_v0.9.0rc6.md`](docs/github_release_draft_v0.9.0rc6.md),
[`docs/release_notes_v0.9.0rc6.md`](docs/release_notes_v0.9.0rc6.md),
[`docs/testpypi_upload_approval_v0.9.0rc6.md`](docs/testpypi_upload_approval_v0.9.0rc6.md),
[`docs/post_release_status_v0.9.0rc6.md`](docs/post_release_status_v0.9.0rc6.md),
[`docs/rc6_development_plan.md`](docs/rc6_development_plan.md),
[`docs/v1_0_gap_audit.md`](docs/v1_0_gap_audit.md),
[`docs/v1_0_decision_matrix.md`](docs/v1_0_decision_matrix.md),
[`docs/testpypi_upload_attempt_v0.9.0rc6.dev0.md`](docs/testpypi_upload_attempt_v0.9.0rc6.dev0.md),
[`docs/testpypi_status_v0.9.0rc6.dev0.md`](docs/testpypi_status_v0.9.0rc6.dev0.md),
[`docs/testpypi_trusted_publishing.md`](docs/testpypi_trusted_publishing.md),
[`docs/testpypi_dry_run_gate.md`](docs/testpypi_dry_run_gate.md), and
[`docs/v1_0_stability_gate.md`](docs/v1_0_stability_gate.md).
PyPI publication readiness and post-publication verification planning are
tracked in
[`docs/pypi_publication_readiness_checklist.md`](docs/pypi_publication_readiness_checklist.md)
and
[`docs/pypi_post_publication_verification_plan.md`](docs/pypi_post_publication_verification_plan.md);
the current recommendation remains not to publish PyPI yet.
The v1.0.0 planning package is documented in
[`docs/v1_0_release_criteria.md`](docs/v1_0_release_criteria.md),
[`docs/v1_0_release_plan.md`](docs/v1_0_release_plan.md),
[`docs/rc_to_v1_0_transition_path.md`](docs/rc_to_v1_0_transition_path.md),
[`docs/v1_0_pypi_decision_gate.md`](docs/v1_0_pypi_decision_gate.md),
[`docs/v1_0_post_release_verification_plan.md`](docs/v1_0_post_release_verification_plan.md),
and
[`docs/agent_studio_frontend_roadmap.md`](docs/agent_studio_frontend_roadmap.md).
The Agent Studio roadmap is local MVP work plus future/Phase 2 planning and is
not a v1.0.0 release blocker.
Local Agent API readiness is now tracked in
[`docs/api_agent_contract.md`](docs/api_agent_contract.md) and
[`docs/cli_api_parity.md`](docs/cli_api_parity.md). The API exposes local
health/version, adapter registry, schema, parse, validate, workflow-plan,
adapter-preview, validation-evidence, and readiness endpoints for Agent Studio.
The local frontend MVP is implemented under [`frontend/`](frontend/), and the
API/frontend stack keeps the same default boundaries: no external solver
execution, no external LLM call, no proprietary solver dependency, no network
requirement for documented local examples, no production-grade physical
validation claim, and no formal convergence proof claim.
API response models are defined in
[`src/optical_spec_agent/api/models.py`](src/optical_spec_agent/api/models.py),
stable error behavior is documented in
[`docs/api_error_model.md`](docs/api_error_model.md), API versioning is
documented in [`docs/api_versioning_policy.md`](docs/api_versioning_policy.md),
request validation is documented in
[`docs/api_request_validation_contract.md`](docs/api_request_validation_contract.md),
and frontend fixture examples live under [`examples/api/`](examples/api/).
Local launch guidance, frontend handoff details, and copyable curl examples are
documented in
[`docs/api_local_launch_guide.md`](docs/api_local_launch_guide.md),
[`docs/frontend_handoff_spec.md`](docs/frontend_handoff_spec.md), and
[`docs/api_curl_examples.md`](docs/api_curl_examples.md). API smoke and fixture
consistency checks live in [`scripts/smoke_agent_api.sh`](scripts/smoke_agent_api.sh)
and [`scripts/check_api_fixtures.py`](scripts/check_api_fixtures.py). The
Agent Studio frontend MVP planning package is documented in
[`docs/frontend_mvp_product_spec.md`](docs/frontend_mvp_product_spec.md),
[`docs/frontend_information_architecture.md`](docs/frontend_information_architecture.md),
[`docs/frontend_api_mapping.md`](docs/frontend_api_mapping.md),
[`docs/frontend_mvp_user_flows.md`](docs/frontend_mvp_user_flows.md),
[`docs/frontend_mvp_acceptance_criteria.md`](docs/frontend_mvp_acceptance_criteria.md),
[`docs/frontend_safety_policy.md`](docs/frontend_safety_policy.md), and
[`docs/frontend_mvp_implementation_plan.md`](docs/frontend_mvp_implementation_plan.md).
The Agent Studio frontend MVP is implemented under [`frontend/`](frontend/) as
a local React + Vite + TypeScript app; run instructions are in
[`docs/frontend_mvp_runbook.md`](docs/frontend_mvp_runbook.md), and local demo
QA is tracked in
[`docs/frontend_mvp_qa_checklist.md`](docs/frontend_mvp_qa_checklist.md).
Live API ergonomics include fixture loading buttons, an API mode indicator,
diagnostics panels, recommended next actions, and collapsible JSON payloads.
Future screenshot checks are planned in
[`docs/frontend_visual_smoke_plan.md`](docs/frontend_visual_smoke_plan.md).
Manual/optional Playwright visual smoke is available through
[`docs/frontend_visual_smoke_runbook.md`](docs/frontend_visual_smoke_runbook.md)
and [`scripts/smoke_frontend_visual.sh`](scripts/smoke_frontend_visual.sh);
it is not part of the default release gate.
The maintainer-facing local demo package is documented in
[`docs/agent_studio_demo_runbook.md`](docs/agent_studio_demo_runbook.md),
[`docs/agent_studio_demo_checklist.md`](docs/agent_studio_demo_checklist.md),
[`docs/agent_studio_demo_storyboard.md`](docs/agent_studio_demo_storyboard.md),
and
[`docs/agent_studio_demo_troubleshooting.md`](docs/agent_studio_demo_troubleshooting.md);
the wrapper is [`scripts/demo_agent_studio.sh`](scripts/demo_agent_studio.sh).
It ties together API launch, frontend launch, smoke checks, optional visual
smoke, and a guided local walkthrough without upload, tag, release, solver, or
external LLM actions.
Local demo review and follow-up hardening are tracked in
[`docs/agent_studio_demo_feedback.md`](docs/agent_studio_demo_feedback.md) and
[`docs/frontend_hardening_backlog.md`](docs/frontend_hardening_backlog.md).
Quickstart onboarding is documented in
[`docs/quickstart.md`](docs/quickstart.md) and
[`docs/quickstart.zh-CN.md`](docs/quickstart.zh-CN.md), with setup/run scripts
[`scripts/bootstrap_demo_env.sh`](scripts/bootstrap_demo_env.sh) and
[`scripts/run_quickstart_demo.sh`](scripts/run_quickstart_demo.sh).
It uses the Local Agent API, defaults to `http://127.0.0.1:8000`, and does not
include upload, publish, tag, release, solver-run, external LLM, login, cloud,
or production deployment controls. If the API is disconnected, the UI falls
back to visibly labeled demo fixture mode; demo mode is not live validation.
Frontend smoke is available through
[`scripts/smoke_frontend_mvp.sh`](scripts/smoke_frontend_mvp.sh).
The current `api_contract_version` is 0.1. The API remains a
frontend-readiness / candidate API, not a separately frozen v1.0 API contract.
This API/frontend work does not trigger PyPI publication and does not change
the current version or release status.
The local one-command quality gate is documented in
[`docs/quality_gates.md`](docs/quality_gates.md), and the docs map,
readiness scorecard, and maintainer decisions are tracked in
[`docs/README.md`](docs/README.md),
[`docs/v1_0_readiness_scorecard.md`](docs/v1_0_readiness_scorecard.md), and
[`docs/maintainer_decision_log.md`](docs/maintainer_decision_log.md).
Operations parity, release dry-run rules, token hygiene, and maintainer
checklists are tracked in
[`docs/ci_quality_gate_parity.md`](docs/ci_quality_gate_parity.md),
[`docs/release_dry_run_operations.md`](docs/release_dry_run_operations.md),
[`docs/secrets_and_token_hygiene.md`](docs/secrets_and_token_hygiene.md), and
[`docs/maintainer_operations_checklist.md`](docs/maintainer_operations_checklist.md).
`ci.yml` is the automatic push/PR gate; benchmark and extended-test workflows
are manual-only. Release dry-run and TestPyPI Trusted Publishing workflows are
manual-only and never publish or create tags/releases from default CI.
Local package publication preflight is available through
[`scripts/testpypi_preflight.sh`](scripts/testpypi_preflight.sh); it performs
build, metadata, wheel install, and CLI checks without uploading anything.
Public contract boundaries are tracked in
[`docs/cli_contract.md`](docs/cli_contract.md),
[`docs/schema_contract.md`](docs/schema_contract.md),
[`docs/adapter_support_matrix.md`](docs/adapter_support_matrix.md),
[`docs/workflow_preview_contract.md`](docs/workflow_preview_contract.md),
[`docs/validation_boundary.md`](docs/validation_boundary.md), and
[`docs/pypi_publication_decision.md`](docs/pypi_publication_decision.md).
The v1.0 public contract freeze is maintainer-approved and recorded in
[`docs/v1_0_public_contract_freeze_status.md`](docs/v1_0_public_contract_freeze_status.md).
The freeze package includes
[`docs/v1_0_public_contract_freeze_confirmation.md`](docs/v1_0_public_contract_freeze_confirmation.md),
[`docs/v1_0_contract_frozen_surface.md`](docs/v1_0_contract_frozen_surface.md),
[`docs/v1_0_contract_non_goals.md`](docs/v1_0_contract_non_goals.md), and
[`docs/v1_0_breaking_change_policy.md`](docs/v1_0_breaking_change_policy.md).
This freeze does not authorize PyPI publication, tag creation, GitHub release
creation, or `v1.0.0` release.
Publication decisions remain pending/not granted and are tracked in
[`docs/publication_decision_record.md`](docs/publication_decision_record.md);
the completed TestPyPI upload does not authorize PyPI publication.
Validation, packaging, and optional-provider policies are tracked in
[`docs/validation_gate.md`](docs/validation_gate.md),
[`docs/packaging_gate.md`](docs/packaging_gate.md),
[`docs/open_source_solver_strategy.md`](docs/open_source_solver_strategy.md),
[`docs/proprietary_solver_policy.md`](docs/proprietary_solver_policy.md),
[`docs/external_solver_policy.md`](docs/external_solver_policy.md), and
[`docs/external_llm_policy.md`](docs/external_llm_policy.md).
v1.0 compatibility and evidence tracking lives in
[`docs/v1_0_compatibility_policy.md`](docs/v1_0_compatibility_policy.md),
[`docs/validation_evidence_manifest.md`](docs/validation_evidence_manifest.md),
[`docs/adapter_maturity_model.md`](docs/adapter_maturity_model.md),
[`docs/open_source_solver_validation_plan.md`](docs/open_source_solver_validation_plan.md),
[`docs/open_solver_validation_harness.md`](docs/open_solver_validation_harness.md),
[`docs/mpb_optional_validation_pilot.md`](docs/mpb_optional_validation_pilot.md),
[`docs/mpb_level3_readiness.md`](docs/mpb_level3_readiness.md),
[`validation/mpb/mpb_validation_pilot_2026-05-14.md`](validation/mpb/mpb_validation_pilot_2026-05-14.md),
[`docs/optiland_optional_validation_pilot.md`](docs/optiland_optional_validation_pilot.md),
[`docs/optiland_level3_readiness.md`](docs/optiland_level3_readiness.md),
[`validation/optiland/optiland_validation_pilot_2026-05-14.md`](validation/optiland/optiland_validation_pilot_2026-05-14.md),
[`docs/elmer_optional_validation_pilot.md`](docs/elmer_optional_validation_pilot.md),
[`docs/elmer_level3_readiness.md`](docs/elmer_level3_readiness.md),
[`validation/elmer/elmer_install_deferred_2026-05-15.md`](validation/elmer/elmer_install_deferred_2026-05-15.md),
[`docs/gmsh_optional_validation_pilot.md`](docs/gmsh_optional_validation_pilot.md),
[`docs/gmsh_level3_readiness.md`](docs/gmsh_level3_readiness.md),
[`validation/gmsh/gmsh_validation_pilot_2026-05-14.md`](validation/gmsh/gmsh_validation_pilot_2026-05-14.md),
[`docs/meep_optional_validation_pilot.md`](docs/meep_optional_validation_pilot.md),
[`docs/meep_level3_readiness.md`](docs/meep_level3_readiness.md),
[`validation/meep/meep_validation_pilot_2026-05-14.md`](validation/meep/meep_validation_pilot_2026-05-14.md),
[`docs/manual_solver_validation_report_template.md`](docs/manual_solver_validation_report_template.md),
[`docs/pytest_marker_policy.md`](docs/pytest_marker_policy.md),
[`docs/offline_user_journey.md`](docs/offline_user_journey.md),
[`docs/error_model.md`](docs/error_model.md),
[`docs/migration_notes_pre_v1.md`](docs/migration_notes_pre_v1.md),
[`docs/v1_0_public_contract_freeze.md`](docs/v1_0_public_contract_freeze.md),
[`docs/v1_0_public_contract_freeze_checklist.md`](docs/v1_0_public_contract_freeze_checklist.md),
[`docs/v1_0_release_criteria.md`](docs/v1_0_release_criteria.md),
[`docs/v1_0_release_plan.md`](docs/v1_0_release_plan.md),
[`docs/rc_to_v1_0_transition_path.md`](docs/rc_to_v1_0_transition_path.md),
[`docs/v1_0_pypi_decision_gate.md`](docs/v1_0_pypi_decision_gate.md),
[`docs/v1_0_post_release_verification_plan.md`](docs/v1_0_post_release_verification_plan.md),
[`docs/agent_studio_frontend_roadmap.md`](docs/agent_studio_frontend_roadmap.md),
[`docs/api_agent_contract.md`](docs/api_agent_contract.md),
[`docs/api_error_model.md`](docs/api_error_model.md),
[`docs/cli_api_parity.md`](docs/cli_api_parity.md),
[`examples/api/README.md`](examples/api/README.md),
[`docs/public_contract_manifest.json`](docs/public_contract_manifest.json),
[`docs/public_contract_change_checklist.md`](docs/public_contract_change_checklist.md),
[`examples/e2e/README.md`](examples/e2e/README.md), and
[`examples/examples_manifest.json`](examples/examples_manifest.json).

## 中文概览

optical-spec-agent 是一个开源仿真工具链优先的光学仿真工作流 agent，也是
一个面向光学仿真的规格编译层：它把中英文自然语言
仿真需求转换为经过校验的 OpticalSpec JSON，并可进一步生成 Meep / MPB /
Gmsh / Elmer / Optiland 的 solver-native input scaffold。当前公开
pre-release 是 `v0.9.0rc7`，当前 `main` package version 是
`0.9.0rc8.dev0` post-rc7 development state。`v0.9.0rc8` tag 尚未创建，
也不是最终稳定版。
本项目不是求解器，也不提供 production-grade physical validation。完整中文文档见
[README.zh-CN.md](README.zh-CN.md)。

## At a glance

| | |
|---|---|
| **Demo outputs** | 3 real parser outputs — [gap plasmon](examples/outputs/demo_gap_plasmon_sweep.json), [gold cross](examples/outputs/demo_asymmetric_cross.json), [waveguide mode](examples/outputs/demo_comsol_waveguide.json) |
| **Adapter** | Meep script generator plus v0.7 MVP preview adapters for MPB, Gmsh, Elmer, and Optiland — see [adapter doc](docs/adapter_mvp_v0.7.md) |
| **Generic adapter CLI** | `optical-spec adapter-list` and `optical-spec adapter-generate` route specs to solver-native input scaffolds; adapters do not run external solvers |
| **Parser modes** | `rule` remains default; v0.8 adds provider-agnostic `llm` and conservative `hybrid` modes with deterministic `mock` provider |
| **Workflow orchestration** | v0.9 adds `workflow-plan`, `workflow-run`, `workflow-replay`, and `workflow-report` for auditable local orchestration |
| **Benchmark** | 16 golden cases + 27 semantic benchmark cases for Meep reliability and v0.7 adapter intent routing — `python benchmarks/run_benchmark.py --mode all`, `python benchmarks/run_semantic_benchmark.py`, and optional `--report` |
| **Release engineering** | Local checks cover CLI surface, docs consistency, artifact contracts, release readiness, LLM mock benchmark, and workflow benchmark |
| **Validation** | `make check` runs deterministic tests, parser benchmarks, semantic benchmark, mock LLM benchmark, workflow benchmark, docs/CLI checks, and artifact contract checks |

Policy docs:
[`open-source strategy`](docs/open_source_solver_strategy.md),
[`proprietary solver policy`](docs/proprietary_solver_policy.md),
[`adapter support matrix`](docs/adapter_support_matrix.md),
[`external solver policy`](docs/external_solver_policy.md), and
[`validation boundary`](docs/validation_boundary.md). Compatibility and evidence:
[`v1.0 compatibility policy`](docs/v1_0_compatibility_policy.md),
[`validation evidence manifest`](docs/validation_evidence_manifest.md),
[`optional open-source solver validation plan`](docs/open_source_solver_validation_plan.md),
and [`examples manifest`](examples/examples_manifest.json).

For `v0.9.0rc7`, maintainers created the GitHub prerelease after release
smoke validation. Do not move the `v0.9.0rc1`, `v0.9.0rc2`, `v0.9.0rc3`,
`v0.9.0rc4`, `v0.9.0rc5`, `v0.9.0rc6`, or `v0.9.0rc7` tags; use a new candidate tag for future
post-release fixes.

## Why this project?

Optical simulation tasks are inherently multi-parameter: geometry, materials, solver settings, sweep plans, post-processing targets. Humans describe these imprecisely; solvers require exact, structured input. This gap makes automation and multi-agent pipelines fragile.

`optical-spec-agent` is the **missing compiler**:
- **Input**: messy natural language
- **Output**: typed, validated spec JSON with per-field provenance (confirmed / inferred / missing)
- **Contract**: every field carries its status and derivation note, so downstream agents know what to trust and what to verify

## Current scope (main `0.9.0rc8.dev0`: post-v0.9.0rc7 development)

`v0.6` diagnostics are post-hoc, local/manual checks around generated Meep run
artifacts. `v0.7` adapters generate annotated solver-input scaffolds for
additional open-source tools. `v0.8` adds a provider-agnostic LLM parser
foundation with deterministic mock evaluation and conservative hybrid fallback.
`v0.9` adds synchronous local workflow orchestration around those existing
capabilities, with auditable step artifacts, replay, reports, human-review
checklists, and workflow benchmarks.
These are reviewable engineering aids, not production-grade physical validation.
External solvers and external LLM providers are optional and not required by
default.

Post-rc7 backend planning now lives in the rc8 roadmap and gap audit:

- [`docs/rc8_backend_roadmap.md`](docs/rc8_backend_roadmap.md) classifies areas
  as done / stable enough, needs backend hardening, deferred / non-blocker,
  future / Phase 2, or not a goal.
- [`docs/rc8_capability_gap_audit.md`](docs/rc8_capability_gap_audit.md)
  identifies remaining backend hardening gaps before any future rc8, PyPI, or
  v1.0.0 decision.
- [`docs/rc8_to_v1_0_decision_path.md`](docs/rc8_to_v1_0_decision_path.md)
  keeps rc8.dev0 engineering separate from release-draft, PyPI, and v1.0.0
  approvals.

The current loop:

```
Natural language  →  Rule-based parser  →  Structured spec JSON  →  Validation
                                                               ↓
                                              adapter-generate / meep-generate
                                                               ↓
                                 Meep / MPB / Gmsh / Elmer / Optiland input
                                                               ↓ (Meep only, optional explicit command)
                                                    Meep execution harness
                                                               ↓
                                      workflow_run.json / report / replay / review checklist
```

**What works:**
- Keyword + regex parsing of Chinese and English optical task descriptions
- Structured sub-models for geometry, materials, sweep plans, source settings, boundary conditions
- Post-hoc inference (gap plasmon → FDTD, FWHM/T2 → Lorentzian fit, nanoparticle_on_film → 3D)
- Per-field provenance tracking: confirmed / inferred / missing
- Pydantic v2 validation with task-type-aware rules
- CLI, FastAPI, and Python SDK interfaces
- Semantic benchmark coverage for 27 reliability-critical parsing cases,
  including material, gap, source, boundary, and waveguide checks
- Meep adapter readiness checks + CLI readiness reporting before script generation
- Meep adapter script modes:
  `preview` for quick structure/script preview,
  `research-preview` for reference/structure runs plus CSV/JSON outputs,
  `smoke` for structural validation only
- Optional Meep execution harness: availability check, explicit script run, known output collection, and auditable artifacts
- Execution artifacts: `stdout.txt`, `stderr.txt`, `execution_result.json`, and `run_manifest.json`
- Nonphysical low-cost diagnostic research-preview profile that closes the CSV/JSON/PNG artifact loop
- Manual v0.6 physical-candidate hardening for one library-Au profile
- Optional local spectrum consistency tooling for candidate-hardening artifacts
- Local observable diagnostics for flux-monitor geometry and per-surface flux sanity
- Mesh sanity diagnostics for under-resolved gaps and monitor presets
- Post-hoc physical diagnostics reports under `outputs/`: mesh CSV, flux CSV,
  execution diagnostics JSON, and a diagnostic preview PNG
- Generic v0.7 adapter registry and CLI:
  `adapter-list` and `adapter-generate`
- Adapter metadata and readiness reporting for strict/non-strict scaffold generation
- MVP preview/scaffold adapters for MPB, Gmsh, Elmer, and Optiland
- v0.8 parser registry with `rule`, `llm`, and `hybrid` parser modes
- Deterministic mock LLM provider for tests, demos, and no-external-API evaluation
- Schema-guided LLM prompt builder, JSON extraction/repair, rule fallback, parser reports, and LLM benchmark report
- v0.9 synchronous workflow orchestration:
  `workflow-plan`, `workflow-run`, `workflow-replay`, and `workflow-report`
- Workflow artifacts: `workflow_run.json`, `workflow_plan.json`,
  step JSON files, generated input, diagnostics, `human_review_checklist.md`,
  and workflow summaries
- Deterministic workflow benchmark for local orchestration completeness checks
- Schema stability policy: 20+ core fields frozen for 0.x

**What does NOT work yet:**
- Async/background orchestration, cloud execution, or long-running worker queues
- Mandatory or production external LLM provider integration
- LLM-based physical correctness validation; LLM parsing only extracts candidate specs
- Full solver automation or production-grade result interpretation
- Physically validated stable Au library research-preview runs; those remain manual diagnostics and may fail with NaN/Inf or timeout
- Formal convergence proof for the v0.6 physical candidate
- Running MPB, Gmsh, Elmer, or Optiland; v0.7 adapters generate input only
- Production-ready MPB/Gmsh/Elmer/Optiland inputs; current outputs are annotated MVP scaffolds
- Production-grade visualization or plotting pipeline
- Solver result interpretation by LLM
- Workflow output is orchestration/scaffolding/evaluation, not scientific proof
- Optiland is scaffold-level because `OpticalSpec` does not yet encode a full sequential lens prescription
- Gmsh/Elmer need richer FEM geometry, material, mesh, and boundary-condition schema before production use

## Install

```bash
cd optical-spec-agent
pip install -e ".[dev]"
```

Requires Python 3.11+.

## Quick start

## Offline examples

For the complete no-network, no-external-solver, no-external-LLM,
no-proprietary-solver flow, see
[`docs/offline_user_journey.md`](docs/offline_user_journey.md) and
[`examples/e2e/README.md`](examples/e2e/README.md).

The checked-in fixtures under [`examples/`](examples/README.md) are the
canonical no-network examples for the current `0.9.0rc8.dev0` main branch and
the public `v0.9.0rc7` RC line:

```bash
optical-spec validate examples/specs/minimal_nanoparticle.json
optical-spec parse examples/specs/minimal_nanoparticle.json --json
optical-spec workflow-plan examples/workflows/local_preview_request.json --json
```

These commands do not run external solvers, do not call external LLM providers,
and do not upload PyPI/TestPyPI artifacts.

### Hero workflow

This is the shortest first-run path through the project’s core value:

```bash
# 1. Natural language optical task -> validated spec JSON
optical-spec parse \
  "用 Meep FDTD 仿真 80 nm 金纳米球放在 100 nm 金膜上，中间 SiO2 gap 为 5 nm，平面波正入射，波长范围 400-900 nm，输出散射谱，提取共振波长和 FWHM。" \
  --output outputs/hero_spec.json

# 2. Re-validate the saved spec
optical-spec validate outputs/hero_spec.json

# 3. Validated spec JSON -> Meep script
optical-spec meep-generate outputs/hero_spec.json \
  --mode research-preview \
  --output outputs/hero_meep_research.py

# 4. Optional: if Meep is installed locally, run the generated script
optical-spec meep-check
optical-spec meep-run outputs/hero_meep_research.py \
  --workdir runs/hero \
  --expected-mode research-preview \
  --timeout 300
```

The optional `meep-run` step writes auditable artifacts such as `stdout.txt`,
`stderr.txt`, `execution_result.json`, and `run_manifest.json`. It is a local
execution harness, not a production solver pipeline.

### CLI

Minimal no-network CLI quickstart:

```bash
# Inspect the local command surface
optical-spec --help

# Export schema without contacting any external service
optical-spec schema --output outputs/schema.json

# Parse and validate with the default rule-based parser
optical-spec parse \
  "用 Meep FDTD 仿真金纳米球-金膜 gap plasmon，输出散射谱和 FWHM。" \
  --output outputs/quickstart_spec.json
optical-spec validate outputs/quickstart_spec.json

# List adapter scaffolds without running external solvers
optical-spec adapter-list --json

# Plan a local workflow without executing solvers
optical-spec workflow-plan \
  "用 MPB 计算二维光子晶体 band diagram，输出前 8 条能带。" \
  --parser hybrid \
  --llm-provider mock \
  --tool mpb
```

These examples use local deterministic paths only. External solvers and
external LLM providers are optional and are not required by default.

```bash
# Parse a task description
optical-spec parse "研究金纳米球-金膜体系中gap从5到25nm变化对散射谱主峰线宽和退相位时间的影响，使用Meep FDTD，提取共振波长、FWHM和T2。"

# Parser modes: rule remains default; mock LLM is deterministic and local
optical-spec parse "..." --parser rule
optical-spec parse "..." --parser llm --llm-provider mock
optical-spec parse "..." --parser hybrid --llm-provider mock
optical-spec parse "..." --parser hybrid --llm-provider mock \
  --parser-report-output outputs/parser_report.json

# Deterministic v0.8 LLM parser evaluation
optical-spec llm-eval benchmarks/llm_cases.json \
  --parser hybrid \
  --llm-provider mock \
  --report outputs/llm_eval_report.json

# v0.9 synchronous local workflow orchestration
optical-spec workflow-plan \
  "用 Meep FDTD 仿真金纳米球-金膜 gap plasmon，扫 gap 5 到 25 nm，输出散射谱和 FWHM。" \
  --parser rule \
  --tool auto

optical-spec workflow-run \
  "用 MPB 计算二维光子晶体 band diagram，扫 Γ-X-M-Γ k 点，输出前 8 条能带。" \
  --parser hybrid \
  --llm-provider mock \
  --tool mpb \
  --output-dir outputs/workflows/mpb_demo \
  --no-execute

optical-spec workflow-replay outputs/workflows/mpb_demo/workflow_run.json \
  --output-dir outputs/workflows/mpb_demo_replay

optical-spec workflow-report outputs/workflows/mpb_demo/workflow_run.json \
  --output outputs/workflows/mpb_demo/report.md

# Release-engineering checks; these do not run external solvers or external LLM APIs
OSA_SMOKE_VENV=/tmp/osa-smoke-rc3-dev ./scripts/smoke_release.sh
make check
python scripts/check_cli_surface.py
python scripts/check_docs_consistency.py
python scripts/check_release_readiness.py --report outputs/release_readiness_report.json
python scripts/check_artifact_contracts.py

# Save output to file
optical-spec parse "..." -o outputs/my_spec.json

# Run built-in examples
optical-spec example all
optical-spec example 01

# Validate a saved spec
optical-spec validate outputs/my_spec.json

# Export JSON Schema
optical-spec schema -o schema.json

# Or use python -m
python -m optical_spec_agent parse "..."

# Generate Meep script from a spec
optical-spec parse "用Meep FDTD仿真金纳米球-金膜gap plasmon..." -o spec.json
optical-spec meep-generate spec.json -o sim.py
optical-spec meep-generate spec.json -o sim_research.py --mode research-preview
optical-spec meep-generate spec.json -o smoke.py --mode smoke

# Generic v0.7 adapter registry and scaffold generation
optical-spec adapter-list
optical-spec adapter-list --json

optical-spec adapter-generate spec.json --tool auto --output outputs/generated_input.py
optical-spec adapter-generate spec.json --tool mpb --output outputs/mpb_band.py
optical-spec adapter-generate spec.json --tool gmsh --output outputs/geometry.geo
optical-spec adapter-generate spec.json --tool elmer --mesh outputs/geometry.msh --output outputs/case.sif
optical-spec adapter-generate spec.json --tool optiland --output outputs/optiland_design.py

# Optional v0.5 execution harness for an existing generated script
optical-spec meep-check --json
optical-spec meep-run sim_research.py --workdir runs/demo --timeout 300 --expected-mode research-preview --run-id demo-001

# Recommended v0.6 post-hoc diagnostics entry point
optical-spec diagnose outputs/my_spec.json \
  --output-dir outputs \
  --run-dir runs/demo \
  --create-demo-spec-if-missing

optical-spec diagnose outputs/my_spec.json \
  --output-dir outputs \
  --run-dir runs/demo \
  --json

# Manual/local Meep integration gates, not default CI gates
python scripts/local_meep_integration_gate.py --mode smoke
python scripts/local_meep_integration_gate.py --mode research-preview --timeout 3600
python scripts/local_meep_stability_matrix.py --skip-research
python scripts/local_meep_stability_matrix.py --only low-cost-dielectric-sanity --timeout-research 600
python scripts/local_meep_candidate_hardening.py --timeout 900
python scripts/local_meep_candidate_convergence.py --latest
python scripts/local_meep_observable_diagnostics.py --timeout 900

# Script wrapper remains available for automation/backward compatibility
python scripts/generate_physical_diagnostics.py \
  --spec outputs/my_spec.json \
  --output-dir outputs \
  --run-dir runs/demo \
  --create-demo-spec-if-missing
```

### Generic adapter generation

`adapter-generate` is the v0.7 solver-input scaffold entry point. It does not
run external solvers. It selects an adapter from the spec (`--tool auto`) or an
explicit tool name:

| Tool | Output | Status |
|------|--------|--------|
| `meep` | `.py` | Existing specialized nanoparticle-on-film script path |
| `mpb` | `.py` | MVP band/eigenmode preview scaffold |
| `gmsh` | `.geo` | MVP geometry/mesh scaffold |
| `elmer` | `.sif` | MVP FEM solver-input scaffold, optionally with `--mesh` |
| `optiland` | `.py` | MVP imaging/ray-tracing scaffold |

Use `--strict` when missing adapter-required fields should fail generation.
Without `--strict`, MVP adapters may still write an annotated scaffold with
clear `missing_required`, warnings, defaults, and limitations. `meep-generate`
remains the backward-compatible Meep-specific command with script modes and
readiness reporting.

### Meep generation modes

- `preview`: 快速脚本预览，保留当前 smoke/preview 路径，不保证物理严谨。
- `research-preview`: 生成更可信的研究预览脚本，包含 reference run、structure run、flux subtraction、CSV 和 JSON 输出。
- `smoke`: 只验证生成脚本的结构和最小运行路径，不代表物理结果。

Script generation modes still generate scripts only. v0.5 includes an optional
execution harness with `meep-check` and `meep-run`, but this is not full solver
automation or production-grade result interpretation. Real Meep execution tests
are skipped unless Meep is installed locally.

`meep-run` supports `--expected-mode smoke|preview|research-preview`. In
`research-preview` mode, successful execution requires both
`scattering_spectrum.csv` and `postprocess_results.json`. By default it writes
`stdout.txt`, `stderr.txt`, `execution_result.json`, and `run_manifest.json`
into the run directory. `execution_result.json` uses schema version
`execution_result.v0.1`. Use `--json` for machine-readable CLI output,
`--run-id` for a stable audit ID, or `--no-save-artifacts` to skip artifact
files.

The local integration gate is manual by design: smoke can be used for a quick
local sanity check, while research-preview can be slow and must be requested
explicitly. Ordinary CI does not require Meep to be installed.

v0.5 also includes a manual/local stability matrix for diagnosing
research-preview NaN/Inf issues. The matrix can switch between PML and Absorber
boundaries, lower the Meep Courant factor, and use a nonphysical
`diagnostic_profile=low_cost` + `dielectric_sanity` path to test execution
plumbing. This diagnostic gate is not part of ordinary CI, and low-cost
`dielectric_sanity` results must not be interpreted as physical metal
scattering results. See
[`docs/local_meep_stability_matrix_v0.5.md`](docs/local_meep_stability_matrix_v0.5.md).

v0.6 local diagnostics add a bounded library-Au physical candidate and optional
spectrum consistency tooling for candidate-hardening artifacts. These metrics
are sanity checks only: they help detect repeatability and sensitivity issues,
but they are not a formal convergence study or production validation. See
[`docs/local_meep_candidate_hardening_v0.6.md`](docs/local_meep_candidate_hardening_v0.6.md).
v0.6 also includes local observable diagnostics for flux-monitor geometry and
per-surface flux sanity; see
[`docs/local_meep_observable_diagnostics_v0.6.md`](docs/local_meep_observable_diagnostics_v0.6.md).
Mesh/monitor diagnostics currently show the v0.6 physical candidate is
execution-stable but gap-under-resolved: `resolution=12 px/um` corresponds to
about `83 nm` grid spacing, so a `5 nm` gap is not physically resolved. See
[`docs/local_meep_mesh_monitor_diagnostics_v0.6.md`](docs/local_meep_mesh_monitor_diagnostics_v0.6.md).

For a compact artifact-oriented report, prefer
`optical-spec diagnose outputs/my_spec.json --output-dir outputs --create-demo-spec-if-missing`.
It reads `outputs/my_spec.json`, optional Meep artifacts, and writes
`mesh_report.csv`, `flux_report.csv`, `execution_diagnostics.json`, and
`diagnostic_preview.png` under `outputs/`. See
[`docs/physical_diagnostics_v0.6.md`](docs/physical_diagnostics_v0.6.md).

### Python SDK

```python
from optical_spec_agent.services.spec_service import SpecService
from optical_spec_agent.parsers.llm import LLMParserConfig, MockLLMClient

svc = SpecService()
spec = svc.process(
    "用FDTD仿真金纳米球Mie散射，直径100nm，波长400-800nm",
    task_id="demo-001",
)

print(spec.confirmed_fields)    # {"task.task_type": "simulation", ...}
print(spec.inferred_fields)     # {"task.research_goal": {...}, ...}
print(spec.missing_fields)      # ["simulation.polarization", ...]
print(spec.validation_status)   # ValidationStatus(is_executable=False, ...)

hybrid_svc = SpecService(
    parser="hybrid",
    llm_config=LLMParserConfig(provider="mock"),
    llm_client=MockLLMClient(),
)
hybrid_spec = hybrid_svc.process("用 MPB 计算二维光子晶体 band diagram...")
print(hybrid_svc.last_parser_report)
```

Complex sweep / gap-plasmon example:

```python
from optical_spec_agent.adapters.meep import MeepAdapter
from optical_spec_agent.services.spec_service import SpecService

text = (
    "用 Meep FDTD 仿真 80 nm 金纳米球放在 100 nm 金膜上，"
    "中间 SiO2 gap 从 5 到 25 nm，平面波正入射，"
    "波长范围 400-900 nm，输出散射谱并提取 FWHM。"
)

spec = SpecService().process(text, task_id="gap-sweep-demo")
readiness = MeepAdapter().validate_ready(spec)
print(readiness.adapter_ready, readiness.errors, readiness.warnings)
```

### Provenance and Inference

Every high-level field is wrapped in a provenance-aware `StatusField`:

- `confirmed`: directly extracted from the user request.
- `inferred`: added by conservative post-hoc rules, with a note explaining why.
- `missing`: not available yet, and therefore visible to validators/adapters.

Examples include `nanoparticle_on_film -> 3d`, `FWHM -> lorentzian_fit`, and
gap-plasmon wording that implies FDTD-style simulation. Physical-candidate
hardening is separate from parsing provenance: it is local Meep evidence that a
bounded profile can produce auditable CSV/JSON/PNG artifacts, not proof of a
production-grade plasmon simulation.

### API

```bash
python -m uvicorn optical_spec_agent.api.app:app --reload --host 127.0.0.1 --port 8000
```

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/health` | Health check |
| `POST` | `/parse` | Parse natural language → spec |
| `POST` | `/validate` | Validate a spec |
| `GET` | `/schema` | Export JSON Schema |

Interactive docs at `http://localhost:8000/docs`.
The future Agent Studio handoff surface uses `/api/*` endpoints; see
[`docs/api_local_launch_guide.md`](docs/api_local_launch_guide.md),
[`docs/frontend_handoff_spec.md`](docs/frontend_handoff_spec.md), and
[`docs/api_curl_examples.md`](docs/api_curl_examples.md). The local Agent
Studio frontend MVP is implemented under [`frontend/`](frontend/) and can be
checked with [`scripts/smoke_frontend_mvp.sh`](scripts/smoke_frontend_mvp.sh).

Example parse request:

```bash
curl -X POST "http://localhost:8000/parse" \
  -H "Content-Type: application/json" \
  -d '{"text":"用 Meep FDTD 仿真 80 nm 金纳米球在 100 nm 金膜上，SiO2 gap 为 5 nm，波长范围 400-900 nm，输出散射谱。","task_id":"api-gap-demo"}'

curl -X POST "http://localhost:8000/parse" \
  -H "Content-Type: application/json" \
  -d '{"text":"用 MPB 计算二维光子晶体 band diagram。","parser":"hybrid","llm_provider":"mock","parser_report":true}'
```

## Demo gallery

Three real parser outputs covering different physical systems and solvers. Each was generated by running the rule-based parser — no manual editing.

> **Note:** Demos include COMSOL and Lumerical inputs to demonstrate schema coverage. These are compatibility-oriented examples, not default dependencies, not default tests, and not release-validation targets. The current adapter roadmap ([v0.3–v0.7](#roadmap)) targets open-source tools only (Meep, Elmer, Gmsh, Optiland).

### Demo 1: Nanoparticle-on-film gap plasmon

```
研究金纳米球-金膜体系中 gap 从 5 到 25 nm 变化对散射谱主峰线宽和
退相位时间的影响，使用 Meep FDTD，提取共振波长、FWHM 和 T2。
```

| Field | Value | Status |
|-------|-------|--------|
| `physics.physical_system` | `nanoparticle_on_film` | confirmed |
| `physics.structure_type` | `sphere_on_film` | confirmed |
| `simulation.solver_method` / `software_tool` | `fdtd` / `meep` | confirmed |
| `simulation.sweep_plan` | gap_nm 5→25 nm | confirmed |
| `output.postprocess_target` | lorentzian_fit, fwhm_extraction, T2_extraction | inferred |
| `physics.model_dimension` | `3d` | inferred |

Full JSON: [`examples/outputs/demo_gap_plasmon_sweep.json`](examples/outputs/demo_gap_plasmon_sweep.json)

### Demo 2: Asymmetric gold cross (Lumerical FDTD)

```
建模非对称金纳米十字结构，两臂长度分别为120nm和80nm，宽40nm，厚30nm，
放在SiO2基底上。用Lumerical FDTD计算偏振相关的散射谱，x偏振和y偏振都要做，
波长范围500-1200nm。
```

| Field | Value | Status |
|-------|-------|--------|
| `physics.structure_type` | `cross_structure` | confirmed |
| `simulation.software_tool` | `lumerical` | confirmed |
| `simulation.polarization` | `linear_x` | confirmed |
| `simulation.sweep_plan` | wavelength_nm 500→1200 nm | confirmed |

Full JSON: [`examples/outputs/demo_asymmetric_cross.json`](examples/outputs/demo_asymmetric_cross.json)

### Demo 3: COMSOL waveguide mode analysis

```
COMSOL模式分析：Si3N4脊波导（宽800nm，高400nm，蚀刻深度250nm），SiO2下包层，
上包层为空气，计算1.55μm波长下的基模有效折射率和模场分布，TE和TM模式都要计算。
```

| Field | Value | Status |
|-------|-------|--------|
| `physics.physical_system` | `waveguide` | confirmed |
| `simulation.solver_method` / `software_tool` | `fem` / `comsol` | confirmed |
| `output.output_observables` | field_distribution, mode_profile | confirmed |

Full JSON: [`examples/outputs/demo_comsol_waveguide.json`](examples/outputs/demo_comsol_waveguide.json)

**Reproduce any demo:**
```bash
optical-spec parse "<input text>" -o my_output.json
```

All demo outputs with detailed field annotations: [`examples/outputs/README.md`](examples/outputs/README.md)

## Schema design

> **Stability policy:** The core fields listed below are frozen for 0.1.x. See [`docs/schema_stability.md`](docs/schema_stability.md) for the full stable surface, volatile fields, and compatibility rules.

The spec is organized in five sections, each field wrapped in a `StatusField(value, status, note)`:

```
OpticalSpec
├── task               task_id, task_name, task_type, research_goal
├── physics            physical_system, physical_mechanism, model_dimension, structure_type
├── geometry_material  geometry_definition, material_system, particle_info,
│                      substrate_or_film_info, gap_medium, key_parameters
├── simulation         solver_method, software_tool, sweep_plan, excitation_source,
│                      source_setting, boundary_condition, mesh_setting, ...
├── output             output_observables, postprocess_target
└── system             confirmed_fields, inferred_fields, missing_fields,
                       assumption_log, validation_status
```

### Enums

| Enum | Values |
|------|--------|
| `TaskType` | modeling, simulation, fitting, data_analysis, plotting, writing |
| `SolverMethod` | fdtd, fem, rcwa, analytical, coupled_oscillator |
| `ModelDimension` | 2d, 3d, axisymmetric |
| `SoftwareTool` | meep, elmer, gmsh, optiland, rayoptics, python, ... |
| `PhysicalSystem` | nanoparticle_on_film, waveguide, metasurface, grating, ... |
| `StructureType` | sphere_on_film, rod_on_film, cube_on_film, cross_structure, ... |
| `ExcitationSource` | plane_wave, tfsf, dipole, mode_source, gaussian_beam, ... |

### Structured sub-models

Key fields use structured Pydantic models instead of raw strings:

| Sub-model | Fields |
|-----------|--------|
| `SweepPlan` | variable, range_start, range_end, step, unit |
| `SourceSetting` | source_type, wavelength_range, polarization, incident_angle |
| `BoundaryConditionSetting` | x_min/max, y_min/max, z_min/max |
| `GeometryDefinition` | geometry_type, dimensions (dict), units |
| `MaterialSystem` | materials (list of MaterialEntry with name, role, model) |
| `ParticleInfo` | particle_type, material, dimensions |

### Validation rules

The validator is **task-type-aware**:

- **Always required**: `task_type`, `research_goal`
- **simulation requires**: `solver_method`, `software_tool`, `excitation_source`, `source_setting`, `boundary_condition`, `monitor_setting`
- **Cross-field**: solver vs software consistency (fdtd→meep, fem→elmer), physical system rules (nanoparticle_on_film→particle_info), postprocess vs observables (fwhm_extraction→spectrum output), physical_system+structure_type combination check
- **Solver-specific**: FDTD requires source+boundary+monitor (≥3 missing → error); FEM requires boundary+monitor (both missing → error)
- **Severity escalation**: FWHM/T2 extraction without spectrum output → error (not just warning); nanoparticle_on_film with all geometry missing → error

### JSON Schema export

```python
from optical_spec_agent.models.spec import OpticalSpec
print(OpticalSpec.export_json_schema())
```

## Testing

```bash
make check
pytest -q
pytest --cov=optical_spec_agent # with coverage
```

Test coverage includes:
- Model construction and serialization
- Parser: 6 Chinese inputs, 2 English inputs, inference rules
- Validator: required fields, consistency, physical system rules
- Meep adapter: script generation, rejection, missing field handling
- Optional Meep execution harness contract tests
- Local diagnostic helper tests that do not require real Meep
- API endpoints: parse, validate, schema
- Service integration

## Benchmark

16 golden cases, 2 comparison modes:

```bash
python benchmarks/run_benchmark.py               # exact regression (default)
python benchmarks/run_benchmark.py --mode key_fields  # key-field extraction only
python benchmarks/run_benchmark.py --mode all         # both
```

| Mode | What it checks |
|------|---------------|
| `exact` | Full output JSON must match snapshot byte-for-byte — catches any parser change |
| `key_fields` | Only core fields (`task_type`, `physical_system`, `solver_method`, `observables`) must be present — resilient to non-breaking output changes |

**What it does NOT test:** semantic understanding scoring, solver correctness, or LLM parsing.

The semantic benchmark checks 27 reliability-critical cases at the field level:

```bash
python benchmarks/run_semantic_benchmark.py
python benchmarks/run_semantic_benchmark.py --report outputs/semantic_benchmark_report.json
```

Full details: [`benchmarks/README.md`](benchmarks/README.md)

## Project structure

```
optical-spec-agent/
├── pyproject.toml
├── Makefile
├── LICENSE
├── README.md
├── .gitignore
├── src/optical_spec_agent/
│   ├── __init__.py
│   ├── __main__.py                  # python -m support
│   ├── models/
│   │   ├── enums.py                 # All enum definitions
│   │   ├── base.py                  # StatusField, structured sub-models
│   │   ├── spec.py                  # OpticalSpec + JSON Schema export
│   │   └── __init__.py
│   ├── parsers/
│   │   ├── base.py                  # BaseParser ABC
│   │   ├── rule_based.py            # Keyword/regex parser (default)
│   │   ├── registry.py              # rule / llm / hybrid parser registry
│   │   ├── llm/                     # v0.8 provider-agnostic LLM parser foundation
│   │   │   ├── client.py            # BaseLLMClient, MockLLMClient, disabled external stub
│   │   │   ├── config.py            # LLMParserConfig, reports, client result
│   │   │   ├── prompt.py            # schema-guided prompt builder
│   │   │   ├── repair.py            # JSON extraction / repair / normalization
│   │   │   ├── merge.py             # conservative hybrid merge helpers
│   │   │   ├── parser.py            # LLMParser and HybridParser
│   │   │   └── evaluator.py         # deterministic LLM benchmark runner
│   │   ├── llm_placeholder.py       # Backward-compatible historical stub
│   │   └── __init__.py
│   ├── validators/
│   │   ├── spec_validator.py        # Task-type-aware validation
│   │   └── __init__.py
│   ├── services/
│   │   ├── spec_service.py          # Parse → validate orchestrator
│   │   └── __init__.py
│   ├── api/
│   │   ├── app.py                   # FastAPI app factory
│   │   ├── routes.py                # /health, /parse, /validate, /schema
│   │   └── __init__.py
│   ├── cli/
│   │   ├── main.py                  # parse, validate, schema, example, Meep commands
│   │   └── __init__.py
│   ├── execution/
│   │   ├── meep_runner.py           # Optional Meep availability/run harness
│   │   └── __init__.py
│   ├── workflows/                   # v0.9 synchronous local workflow orchestration
│   │   ├── models.py                # WorkflowRun, WorkflowPlan, artifacts, step results
│   │   ├── planner.py               # workflow-plan implementation
│   │   ├── runner.py                # workflow-run orchestration
│   │   ├── replay.py                # workflow-replay support
│   │   ├── reports.py               # workflow-report rendering
│   │   ├── registry.py              # default agent registry
│   │   └── agents/                  # intake, parse, validate, generate, diagnose, report
│   ├── analysis/
│   │   ├── spectrum_compare.py      # Local spectrum consistency metrics
│   │   ├── mesh_sanity.py           # Local mesh-resolution diagnostics
│   │   ├── physical_diagnostics.py  # Spec/artifact diagnostics report generation
│   │   └── __init__.py
│   ├── adapters/
│   │   ├── base.py                  # BaseAdapter ABC + AdapterResult/readiness metadata
│   │   ├── registry.py              # v0.7 adapter registry and dispatch
│   │   ├── utils.py                 # Shared adapter field helpers
│   │   ├── meep/                    # Meep adapter (nanoparticle_on_film → script)
│   │       ├── models.py            # MeepInputModel
│   │       ├── translator.py        # OpticalSpec → MeepInputModel
│   │       └── template.py          # MeepInputModel → Python script
│   │   ├── mpb/                     # MPB preview script adapter
│   │   ├── gmsh/                    # Gmsh .geo scaffold adapter
│   │   ├── elmer/                   # Elmer .sif scaffold adapter
│   │   └── optiland/                # Optiland Python scaffold adapter
│   └── utils/
│       ├── format.py                # JSON + human-readable summary
│       └── __init__.py
├── tests/
│   ├── conftest.py
│   ├── test_models.py
│   ├── test_parser.py               # Parser tests
│   ├── test_parser_registry.py
│   ├── test_llm_client.py
│   ├── test_llm_prompt.py
│   ├── test_llm_json_repair.py
│   ├── test_llm_parser.py
│   ├── test_hybrid_parser.py
│   ├── test_cli_llm_parse.py
│   ├── test_cli_llm_eval.py
│   ├── test_api_llm_parse.py
│   ├── test_llm_benchmark.py
│   ├── test_llm_guardrails.py
│   ├── test_workflow_models.py
│   ├── test_workflow_agents.py
│   ├── test_workflow_runner.py
│   ├── test_workflow_cli.py
│   ├── test_workflow_api.py
│   ├── test_workflow_replay.py
│   ├── test_workflow_reports.py
│   ├── test_workflow_benchmark.py
│   ├── test_validator.py
│   ├── test_meep_adapter.py         # Meep adapter tests
│   ├── test_adapter_registry.py
│   ├── test_adapter_cli.py
│   ├── test_mpb_adapter.py
│   ├── test_gmsh_adapter.py
│   ├── test_elmer_adapter.py
│   ├── test_optiland_adapter.py
│   ├── test_meep_runner.py          # Optional Meep execution harness tests
│   ├── test_mesh_sanity.py
│   ├── test_physical_diagnostics.py
│   ├── test_spectrum_compare.py
│   ├── test_local_meep_candidate_convergence.py
│   ├── test_local_meep_candidate_hardening.py
│   ├── test_local_meep_integration_gate.py
│   ├── test_local_meep_observable_diagnostics.py
│   ├── test_local_meep_physical_stability_probe.py
│   ├── test_local_meep_stability_matrix.py
│   ├── test_service.py
│   └── test_api.py
├── scripts/
│   ├── local_meep_integration_gate.py
│   ├── local_meep_stability_matrix.py
│   ├── local_meep_physical_stability_probe.py
│   ├── local_meep_candidate_hardening.py
│   ├── local_meep_candidate_convergence.py
│   ├── local_meep_observable_diagnostics.py
│   └── generate_physical_diagnostics.py
├── examples/
│   ├── example_01_nanoparticle_gap_plasmon.py
│   ├── example_02_asymmetric_gold_cross.py
│   ├── example_03_lumerical_fdtd_scattering.py
│   ├── example_04_comsol_mode_analysis.py
│   ├── example_05_lorentzian_fitting.py
│   ├── example_06_meep_nanoparticle.py
│   └── outputs/
│       ├── README.md
│       ├── demo_gap_plasmon_sweep.json
│       ├── demo_asymmetric_cross.json
│       ├── demo_comsol_waveguide.json
│       └── meep_nanoparticle_on_film.py
├── benchmarks/
│   ├── README.md
│   ├── golden_cases.json
│   ├── semantic_cases.json
│   ├── llm_cases.json
│   ├── workflow_cases.json
│   ├── run_benchmark.py
│   ├── run_semantic_benchmark.py
│   ├── run_llm_benchmark.py
│   └── run_workflow_benchmark.py
├── docs/
│   ├── open_source_stack.md              # Tool-stack rationale and per-tool specs
│   ├── open_source_integration_focus.md  # Adapter priority tiers and Meep-first rationale
│   ├── meep_adapter_v0.md               # Meep adapter scope and limitations
│   ├── local_meep_gate_report_v0.5.md    # Manual local Meep gate evidence
│   ├── local_meep_stability_matrix_v0.5.md # Manual Meep stability diagnostics
│   ├── local_meep_physical_stability_prestudy_v0.6.md # Manual v0.6 physical stability pre-study
│   ├── local_meep_candidate_hardening_v0.6.md # Manual v0.6 candidate hardening evidence
│   ├── local_meep_observable_diagnostics_v0.6.md # Manual v0.6 flux observable diagnostics
│   ├── local_meep_mesh_monitor_diagnostics_v0.6.md # Manual v0.6 mesh/monitor diagnostics
│   ├── physical_diagnostics_v0.6.md # Post-hoc outputs/ diagnostics reports
│   ├── release_notes_v0.5.0.md
│   ├── adapter_mvp_v0.7.md             # v0.7 adapter MVP scope and examples
│   ├── release_readiness_v0.7.md       # v0.7 readiness checklist
│   ├── release_notes_v0.7.0.md         # Draft v0.7 release notes
│   ├── llm_parser_v0.8.md              # v0.8 parser architecture
│   ├── llm_eval_v0.8.md                # v0.8 deterministic parser eval
│   ├── provenance_policy_v0.8.md       # Parser provenance policy
│   ├── release_readiness_v0.8.md       # v0.8 readiness checklist
│   ├── release_notes_v0.8.0.md         # Draft v0.8 release notes
│   ├── workflow_orchestration_v0.9.md  # v0.9 workflow architecture and CLI/API/SDK
│   ├── workflow_benchmark_v0.9.md      # v0.9 workflow benchmark format
│   ├── release_readiness_v0.9.md       # v0.9 readiness checklist
│   ├── release_notes_v0.9.0.md         # Draft v0.9 release notes
│   ├── versioning_policy.md             # Packaged/main/release status policy
│   ├── release_readiness_current.md     # Current branch release-readiness matrix
│   ├── release_notes_current.md         # Current branch draft notes
│   ├── artifact_contracts.md            # Generated artifact schemas/contracts
│   ├── security_and_robustness.md       # Local/default safety posture
│   ├── api_contract.md                  # FastAPI endpoint contract
│   ├── cli_contract.md                  # CLI surface and exit-code contract
│   ├── benchmark_contract.md            # Benchmark/report contracts
│   ├── demo_artifacts.md                # Deterministic demo artifact regeneration
│   ├── schema_stability.md              # Stable field surface for 0.x
│   ├── adapter_architecture.md
│   ├── demo_output.md
│   ├── tool_mapping.md
│   └── repo_metadata.md                  # GitHub About + issue drafts
└── outputs/
    └── .gitkeep
```

## Roadmap

> **Strategy**: open-source-native, scriptable-first. All adapters target open-source tools
> (Meep, MPB, Gmsh, Elmer, Optiland, FreeCAD). Commercial software is not a core dependency.

| Version | Goal | Adapter Target | Status |
|---------|------|---------------|--------|
| **v0.1** | NL → spec JSON + validation (rule-based) | — | **Done** |
| v0.2 | Spec hardening + Meep adapter preview | **Meep** (script gen only) | Done |
| v0.3 | Core Meep reliability + semantic benchmark + adapter readiness | **Meep** (script gen only) | Done |
| v0.4 | Meep research-preview script: normalization run, CSV output, postprocess JSON | **Meep** (script gen only) | Done |
| **v0.5** | Meep execution harness + auditable artifacts + low-cost diagnostic pipeline | **Meep** (FDTD) | **Done** |
| v0.6 | Meep physical-candidate hardening + spectrum sanity metrics | **Meep** (FDTD) | Done / local evidence |
| v0.7 | Multi-solver adapter foundation + MPB/Gmsh/Elmer/Optiland MVP scaffolds | **MPB** / **Gmsh** / **Elmer** / **Optiland** | Main branch MVP / release candidate |
| v0.8 | LLM parser foundation + mock provider + hybrid evaluation | — | Main branch foundation |
| v0.9 | Synchronous local workflow orchestration + replay/report/benchmark | — | Current / main branch foundation |
| v1.0 | Release hardening, stable public contracts, packaging, CI, and documentation trust | — | Planned |

**Why Meep first:** Pure Python API, spec fields map 1:1 to Meep objects, and a working adapter proves the full NL → spec → simulation chain. See [`docs/open_source_integration_focus.md`](docs/open_source_integration_focus.md) for the prioritization rationale.

**Adapter vs LLM:** Adapter and execution work (v0.3–v0.7) shipped before LLM integration (v0.8) because real solver feedback must stabilize the spec schema first. The rule-based parser + golden cases remain the evaluation baseline for the v0.8 mock/hybrid parser foundation and any future external provider.

See [`docs/open_source_stack.md`](docs/open_source_stack.md) for per-tool details and [`docs/open_source_integration_focus.md`](docs/open_source_integration_focus.md) for priority tiers.

## Backend Optical-Language Diagnostics

The backend now exposes deterministic source/monitor inference through
`/api/optical-language/infer`, `/api/optical-language/diagnose`,
`/api/optical-language/observables/diagnose`,
`/api/optical-language/adapter-mapping`, and `/api/agent-session`. For
nanoparticle scattering previews, the default metadata is a plane-wave-like
source, 400-900 nm band, `linear_x` polarization, and scattering/extinction
spectrum monitor. The backend can now explain how that intent maps into Meep,
MPB, Gmsh, Elmer, or Optiland preview semantics. These are preview/design-assist
assumptions only; no external solver monitor is executed.

Adapter-native golden preview cases now live in
[`examples/adapter_native_golden/`](examples/adapter_native_golden/) and are
documented in
[`docs/adapter_native_golden_cases.md`](docs/adapter_native_golden_cases.md).
They check Meep, MPB, Gmsh, Elmer, and Optiland source/monitor/observable
fragments and strict expected metadata against local API responses without
running solvers. The coverage matrix is documented in
[`docs/adapter_native_golden_coverage_matrix.md`](docs/adapter_native_golden_coverage_matrix.md)
and exposed by `GET /api/adapter-native-golden-coverage`.

## License

[MIT](LICENSE)
