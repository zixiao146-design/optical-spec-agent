# v1.0.0 Release Plan

## Release philosophy

v1.0.0 should stabilize the documented public contract and preserve conservative
claims. It should not imply production-grade physical validation, formal
convergence proof, default external solver execution, default external LLM
access, or proprietary solver support.

## Proposed release sequence

- Continue `0.9.0rc7.dev0` engineering.
- Continue local Agent API readiness and keep the Agent Studio frontend MVP
  local-first.
- Keep API response models and `examples/api/` frontend fixtures aligned with
  endpoint behavior.
- Keep `api_contract_version` 0.1, request validation, and error fixtures
  documented while the API remains a frontend-readiness / candidate API.
- Keep `docs/api_local_launch_guide.md`, `docs/frontend_handoff_spec.md`,
  `docs/api_curl_examples.md`, `scripts/smoke_agent_api.sh`, and
  `scripts/check_api_fixtures.py` aligned with the frontend MVP.
- Keep `docs/frontend_mvp_product_spec.md`,
  `docs/frontend_information_architecture.md`,
  `docs/frontend_api_mapping.md`, `docs/frontend_mvp_user_flows.md`,
  `docs/frontend_mvp_acceptance_criteria.md`,
  `docs/frontend_safety_policy.md`, and
  `docs/frontend_mvp_implementation_plan.md` aligned with the implemented MVP.
- Keep `docs/frontend_mvp_runbook.md` aligned with `frontend/`.
- Keep `scripts/demo_agent_studio.sh` and the Agent Studio demo runbook,
  checklist, storyboard, and troubleshooting guide aligned with the frontend
  MVP for local maintainer demos.
- Keep `docs/quickstart.md`, `docs/quickstart.zh-CN.md`,
  `scripts/bootstrap_demo_env.sh`, `scripts/run_quickstart_demo.sh`, and
  `examples/quickstart/` aligned as the first-run onboarding path.
- Keep English / 中文 localization docs and dictionaries aligned:
  `docs/frontend_i18n_zh_CN.md` and `frontend/src/i18n/`. Localization must not
  rename API JSON keys, adapter tool names, package metadata, or
  `api_contract_version`.
- Decide PyPI publication path.
- Prepare v1.0.0 release draft.
- Run quality gates.
- Build distributions.
- Verify dist filenames.
- Create annotated `v1.0.0` tag only after explicit approval.
- Create GitHub release only after explicit approval.
- Optionally publish PyPI only after separate explicit approval.
- Add post-release status doc.

## Required release artifacts

- `docs/github_release_draft_v1.0.0.md`
- `docs/release_notes_v1.0.0.md`
- `docs/release_readiness_v1.0.0.md`
- `docs/post_release_status_v1.0.0.md` after release
- PyPI status doc if PyPI is published

## Explicit non-actions until approval

- No `v1.0.0` tag.
- No GitHub release.
- No PyPI publication.
- No TestPyPI upload.
- No claim expansion.
- No frontend production deployment unless separately approved.
- No committed `node_modules`, `frontend/dist`, or frontend build artifacts.
- No frontend upload, publish, tag, release, solver-run, or external LLM
  controls.
- No demo workflow that uploads packages, publishes PyPI/TestPyPI, creates
  tags, creates GitHub releases, executes solvers, or calls external LLMs.
- No quickstart workflow that uploads packages, publishes PyPI/TestPyPI,
  creates tags, creates GitHub releases, executes solvers, or calls external
  LLMs.
- No PyPI publication trigger from API fixture readiness alone.
- No separate v1.0 API contract freeze unless maintainers explicitly approve it.
- No default external solver, external LLM, network, or proprietary dependency.
