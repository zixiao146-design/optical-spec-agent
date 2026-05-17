# Agent Studio Frontend MVP Runbook

## 1. Prerequisites

Run the local API:

```bash
python -m uvicorn optical_spec_agent.api.app:app --reload --host 127.0.0.1 --port 8000
```

Install frontend dependencies:

```bash
cd frontend
npm install
```

The FastAPI app allows local Vite origins `http://127.0.0.1:5173` and
`http://localhost:5173` through conservative CORS settings.

## 2. Start Frontend

```bash
npm run dev
```

Default API base: `http://127.0.0.1:8000`.

The UI supports English / 中文 switching through the sidebar
`LanguageSwitcher`. The selected language is stored in `localStorage` under
`agent-studio-language`; Chinese browser environments default to `zh-CN`.
API JSON field names and adapter tool names remain untranslated.

Override:

```bash
VITE_API_BASE_URL=http://127.0.0.1:8000 npm run dev
```

## 3. Build/Check

```bash
npm run typecheck
npm run build
```

Or run the repository smoke wrapper:

```bash
./scripts/smoke_frontend_mvp.sh
```

Maintainer-facing local demo wrapper:

```bash
./scripts/demo_agent_studio.sh
```

First-run quickstart:

```bash
./scripts/bootstrap_demo_env.sh
source /tmp/osa-agent-studio-demo/bin/activate
./scripts/run_quickstart_demo.sh
```

See [`quickstart.md`](quickstart.md) and
[`quickstart.zh-CN.md`](quickstart.zh-CN.md).

Use `OSA_DEMO_HOLD=1 ./scripts/demo_agent_studio.sh` to keep the local API and
frontend running for a guided walkthrough. The demo package is documented in
[`agent_studio_demo_runbook.md`](agent_studio_demo_runbook.md),
[`agent_studio_demo_checklist.md`](agent_studio_demo_checklist.md),
[`agent_studio_demo_storyboard.md`](agent_studio_demo_storyboard.md), and
[`agent_studio_demo_troubleshooting.md`](agent_studio_demo_troubleshooting.md).

Optional Playwright visual smoke:

```bash
./scripts/smoke_frontend_visual.sh
```

Visual smoke remains manual/optional and is not part of the default release
gate. See [`frontend_visual_smoke_runbook.md`](frontend_visual_smoke_runbook.md).

Do not commit `node_modules`, `frontend/dist`, or other build artifacts.

## 4. Demo / Fixture Mode

If the Local Agent API is unavailable, the frontend falls back to bundled demo
fixtures so the workbench remains navigable. Demo fixture mode is visibly
marked as not live validation. It does not run solvers, call external LLMs,
publish packages, create tags, or create releases.

The Spec Input, Workflow Plan, and Artifact Preview pages include fixture
loading buttons. Loading a fixture only fills the local form and shows
`Demo fixture loaded - not live validation until submitted.` Live validation or
preview generation starts only after the user submits the form to the local API.

Dashboard and System Status include an API mode indicator with the configured
API base URL. If the API is disconnected, the indicator recommends:

```bash
python -m uvicorn optical_spec_agent.api.app:app --reload --host 127.0.0.1 --port 8000
```

Diagnostics and recommended next actions are rendered in shared panels across
parse, validate, workflow, preview, and readiness views.

## 5. Safety Notes

- No solver execution.
- No external LLM.
- No upload controls.
- No release controls.
- No production-grade validation claim.
- No formal convergence proof claim.

## 6. Troubleshooting

- API not running: start the FastAPI command above and refresh the frontend.
- API disconnected but demo visible: this is expected fixture mode, not live
  validation.
- CORS/local API base: confirm the frontend runs on `127.0.0.1:5173` or
  `localhost:5173`.
- Version mismatch: check `GET /api/version` and the dashboard API contract
  badge.
- Fixture mismatch: run `python scripts/check_api_fixtures.py`.
- Frontend smoke: run `./scripts/smoke_frontend_mvp.sh`.
- Visual smoke: run `./scripts/smoke_frontend_visual.sh` or review
  `docs/frontend_visual_smoke_plan.md`.
- Demo walkthrough: run `./scripts/demo_agent_studio.sh` or review
  `docs/agent_studio_demo_runbook.md`.
- Quickstart walkthrough: run `./scripts/run_quickstart_demo.sh` after
  `./scripts/bootstrap_demo_env.sh`.
