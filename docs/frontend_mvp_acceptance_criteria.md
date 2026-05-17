# Agent Studio Frontend MVP Acceptance Criteria

## 1. Functional criteria

- Can launch against local API.
- Can call all frontend-ready endpoints.
- Can render readiness state.
- Can render adapter matrix.
- Can submit parse and validate requests.
- Can render workflow plan.
- Can render adapter preview.
- Can render validation evidence.
- Can render Material Library.
- Can request local material suggestions.
- Can render Agent Collaboration trace.
- Can render Example Gallery with bundled optical design examples.
- Can render Agent Trace Timeline with sub-agent input/output, diagnostics,
  evidence refs, safety notes, and recommendations.
- Can show loading, empty, error, and API disconnected states.
- Can show demo fixture mode when the local API is unavailable.
- Can load example/fixture requests into Spec Input, Workflow Plan, and Artifact
  Preview without calling the API until submitted.
- Can show API connected, API disconnected, and demo fixture mode with the API
  base URL.
- Can render diagnostics and recommended next actions consistently.
- Can show a guided quickstart demo with Example Gallery, Load example spec,
  Parse locally, Validate spec, Review adapter matrix, Material Library, Agent
  Trace Timeline, Generate workflow plan, Preview artifact, Review validation
  evidence, and Review readiness / next action.
- Can switch between English and 中文 without refreshing the page.
- Chinese guided demo shows 示例库、加载示例规格、本地解析、验证规格、查看适配器矩阵、
  材料库、多智能体协作轨迹、生成工作流计划、预览适配器产物、查看验证证据、查看 readiness / 下一步建议。
- Can show a quickstart completion checklist with API connected,
  `0.9.0rc7.dev0`, `api_contract_version` 0.1, no solver executed, and no
  external LLM called.

## 2. Safety criteria

- UI must show no-default-solver boundary.
- UI must show no-default-LLM boundary.
- UI must not expose PyPI/TestPyPI upload button.
- UI must not expose tag/release button.
- UI must not imply production-grade validation.
- UI must not imply formal convergence proof.
- UI must show material catalog is preview-only.
- UI must show sub-agent trace does not call external LLMs.
- Demo fixture mode must state that it is not live validation.
- UI must show that it does not control PyPI/TestPyPI publication or GitHub
  releases.
- 中文 UI 必须显示默认不执行外部求解器、默认不调用外部 LLM、不声明形式化收敛证明、
  不控制 PyPI/TestPyPI 上传或 GitHub tag/release 的边界。

## 3. Technical criteria

- Local-first.
- No cloud backend.
- No login system.
- API base configurable.
- Uses API contract version 0.1.
- Uses `examples/api` fixtures for initial development.
- No generated build artifacts committed.
- Uses shared `LoadingState`, `EmptyState`, `ErrorState`, `SafetyNotice`, and
  `ApiDisconnectedNotice` components.
- Buttons are disabled while the matching local API action is loading.
- Status and error regions use `aria-live`.
- JSON panels are labeled, scrollable, and can be collapsed for scan-friendly
  local demos.
- Playwright visual smoke is documented in `docs/frontend_visual_smoke_plan.md`
  and `docs/frontend_visual_smoke_runbook.md`.
- Optional Playwright visual smoke can be run with
  `./scripts/smoke_frontend_visual.sh`.
- Playwright visual smoke remains manual and outside the default release gate.
- Quickstart setup/run scripts are documented and do not upload, publish,
  create tags/releases, run solvers, or call external LLMs.
- i18n dictionaries live under `frontend/src/i18n/`; API JSON keys and adapter
  tool names remain untranslated.

## 4. Not required for MVP

- Solver execution.
- External LLM.
- Multi-user accounts.
- 3D visualization.
- Optimization UI.
- PyPI/release operations.
- Required Playwright screenshot automation in the default quality gates.

## Implementation evidence

- Frontend source exists under `frontend/`.
- API base URL is configurable with `VITE_API_BASE_URL`.
- The MVP uses Local Agent API endpoints only.
- The MVP has demo fixture fallback for API disconnected local demos.
- `./scripts/smoke_frontend_mvp.sh` verifies typecheck/build without committing
  generated frontend artifacts.
- `./scripts/smoke_frontend_visual.sh` verifies major pages and safety copy
  manually without committing Playwright reports.
- Build outputs, `node_modules`, and generated artifacts must not be committed.
