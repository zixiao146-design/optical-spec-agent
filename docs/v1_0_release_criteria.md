# v1.0.0 Release Criteria

## Current baseline

- Current public prerelease: v0.9.0rc8
- Current main development version: 0.9.0rc9.dev0
- v1.0 public contract freeze: approved
- TestPyPI uploaded and verified for 0.9.0rc6.dev0
- PyPI published: no
- PyPI publication approval: not granted
- v1.0.0 released: no
- Local Agent API readiness: in progress
- Local Agent API status: frontend-readiness / candidate API
- Local Agent API contract version: 0.1
- Local Agent API response models: available
- Local Agent API frontend fixtures: `examples/api/`
- Local Agent API handoff docs: `docs/api_local_launch_guide.md`,
  `docs/frontend_handoff_spec.md`, and `docs/api_curl_examples.md`
- Local Agent API fixture/smoke scripts: `scripts/check_api_fixtures.py` and
  `scripts/smoke_agent_api.sh`
- Agent Studio frontend MVP planning and implementation: available in
  `docs/frontend_mvp_product_spec.md`,
  `docs/frontend_information_architecture.md`,
  `docs/frontend_api_mapping.md`, `docs/frontend_mvp_user_flows.md`,
  `docs/frontend_mvp_acceptance_criteria.md`,
  `docs/frontend_safety_policy.md`, and
  `docs/frontend_mvp_implementation_plan.md`
- Frontend implementation: local MVP under `frontend/`
- Frontend MVP runbook: `docs/frontend_mvp_runbook.md`
- Agent Studio demo package: `scripts/demo_agent_studio.sh`,
  `docs/agent_studio_demo_runbook.md`,
  `docs/agent_studio_demo_checklist.md`,
  `docs/agent_studio_demo_storyboard.md`, and
  `docs/agent_studio_demo_troubleshooting.md`
- Quickstart onboarding: `docs/quickstart.md`, `docs/quickstart.zh-CN.md`,
  `scripts/bootstrap_demo_env.sh`, `scripts/run_quickstart_demo.sh`, and
  `examples/quickstart/`
- Agent Studio English / 中文 localization:
  `docs/frontend_i18n_zh_CN.md` and `frontend/src/i18n/`; it improves local
  usability without changing API JSON fields, adapter tool names,
  `api_contract_version`, package version, or release status.
- Backend evidence review decision:
  `docs/backend_evidence_review_decision.md` records backend evidence as
  sufficient to prepare the `v0.9.0rc7` release draft. The `v0.9.0rc7`
  GitHub prerelease has since been created and verified; PyPI publication,
  TestPyPI upload for `0.9.0rc9.dev0`, future `v0.9.0rc9` tag/release work,
  and `v1.0.0` release approval remain separate and not granted.

## Required before v1.0.0

- Maintainer approval for v1.0.0 release is recorded.
- Final version is set to 1.0.0.
- `pyproject.toml` version == `1.0.0`.
- `src/optical_spec_agent/__init__.py` `__version__` == `1.0.0`.
- Public contract freeze remains approved.
- PyPI publication decision is recorded.
- Quality gates passed.
- GitHub Actions CI passed.
- TestPyPI no-upload or upload decision is explicit.
- `python -m pytest` passed.
- `python -m build` passed.
- `make check` passed.
- CLI examples passed.
- Wheel install smoke passed.
- Release notes exist.
- GitHub release draft exists.
- `v1.0.0` tag is absent before creation.
- Post-release status plan is ready.

## Validation scope allowed for v1.0.0

- Optional manual validation evidence is available for Gmsh / Meep / MPB /
  Optiland.
- Elmer Level 3 remains deferred unless explicitly validated later.
- v1.0.0 may be released without Elmer Level 3 if documentation remains clear.
- Production-grade physical validation is not claimed.
- Formal convergence proof is not claimed.

## Publication criteria

- PyPI publication is a separate approval.
- PyPI may be published only after explicit maintainer approval.
- TestPyPI verification has been completed for 0.9.0rc6.dev0.
- Final PyPI release may require another TestPyPI upload or an explicit skip
  record.

## Release blocker classification

| Item | Classification | Status | Required action |
|---|---|---|---|
| Public contract freeze | Hard blocker | Satisfied | Keep the approved freeze current and require approval for frozen-surface changes. |
| PyPI publication decision | Hard strategic decision | Pending / not granted | Decide GitHub-only, delayed PyPI, or approved PyPI publication before v1.0. |
| v1.0.0 release approval | Hard blocker | Pending | Record explicit maintainer approval before version/tag/release work. |
| Quality gates and CI | Hard blocker | Established | Re-run immediately before any v1.0.0 release action. |
| TestPyPI decision | Soft blocker | Verified for 0.9.0rc6.dev0 | Decide whether final 1.0.0 needs TestPyPI or an explicit skip record. |
| Elmer Level 3 | Deferred/non-blocker | Deferred | Keep Elmer Level 2 + Level-3-ready unless a maintainable validation route appears. |
| Production-grade validation | Non-goal | Not claimed | Do not add production-grade physical validation claims. |
| Formal convergence proof | Non-goal | Not claimed | Do not add formal convergence proof claims. |
| Frontend/API Agent Studio | Engineering track | Local MVP implemented; production UI remains future/Phase 2 | Not a v1.0 blocker. |
| Local Agent API readiness | Engineering track | In progress | Useful for future Agent Studio, but not a v1.0 blocker unless maintainers choose to gate on it. |
| Local Agent API contract freeze | Future decision | Not separately frozen | API remains frontend-readiness / candidate API until maintainer explicitly approves freezing it. |
| Frontend fixture readiness | Engineering track | Available under `examples/api/` | Useful for future Agent Studio mock data, but not a PyPI publication trigger. |
| Frontend handoff docs/scripts | Engineering track | Available | Launch guide, handoff spec, curl examples, API smoke, and fixture consistency checks support future frontend planning. |
| Frontend MVP | Engineering track | Local React + Vite + TypeScript MVP implemented | Not a v1.0 blocker and not a PyPI publication trigger. |
| Agent Studio demo package | Engineering track | Local demo runbook/script/checklist/storyboard/troubleshooting available | Useful for maintainer review, but not a release, PyPI, tag, or GitHub release action. |
| Quickstart onboarding | Engineering track | Local quickstart docs/scripts/examples available | Useful for public-demo rehearsal, but not a release, PyPI, tag, or GitHub release action. |
| Frontend localization | Engineering track | English / 中文 UI available | Improves local demos; does not change the API contract or release criteria. |
| Example Gallery / Material Library / Agent Trace Timeline | Engineering track | Preview-first domain expansion | Useful for Agent Studio orientation, but does not expand validation claims or require v1.0 release gating. |
| Agent Command Center | Engineering track | Local task-session surface available | Useful for maintainer demos; not a release, upload, tag, or PyPI publication trigger. |
| Tool-call reality ledger | Engineering track | Backend task sessions include ledger records | Helps prove which local tools were called and which external actions were blocked; not a release trigger. |
| Optical calculators | Engineering track | Preview/design-assist endpoints available, including sweeps, case helpers, quality fields, and formula sanity reference cases | Useful backend functionality; not production-grade physical validation and not a v1.0 blocker by itself. |
| Backend capability report | Engineering track | JSON/Markdown script and API endpoints available | Proves installed/callable/executed backend reality and design-case cross-checks; not a release/upload/tag trigger. |
| Backend evidence review pack | Engineering track | JSON/Markdown generator, smoke script, docs, and API summary available | Bundles maintainer review evidence; not production-grade validation and not a release/upload/tag trigger. |
| Backend evidence review decision | Engineering track | Backend evidence sufficient for the `v0.9.0rc7` release draft; rc7 GitHub prerelease created and verified | PyPI/TestPyPI/future rc8 tag/release/v1.0 approval remains separate and not granted. |

Material constants remain preview/design-assist data unless independently
verified. Sub-agent trace is local/deterministic and does not call external
LLMs or run solvers.

Validation maturity is consolidated in
[`backend_validation_maturity_matrix.md`](backend_validation_maturity_matrix.md)
and [`preview_boundary_policy.md`](preview_boundary_policy.md). These documents
help prevent future v1.0 decisions from overreading backend evidence as physical
validation, solver convergence, or material-data verification.

## rc9 decision checkpoint

Use `docs/rc9_v1_0_readiness_gap_audit.md`,
`docs/rc9_backend_stabilization_plan.md`,
`docs/rc9_pypi_publication_decision_review.md`,
`docs/rc9_go_no_go_matrix.md`, and `docs/rc9_release_strategy.md` before any
future rc9 release draft, PyPI decision, or `v1.0.0` planning package.

Current public prerelease is `v0.9.0rc8`; current main development version is
`0.9.0rc9.dev0`. PyPI is not published, PyPI publication approval is not
granted, `v1.0.0` is not approved, and no production-grade validation or formal
convergence proof is claimed.
