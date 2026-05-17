# Frontend Visual Smoke Runbook

## 1. Purpose

Playwright visual smoke checks confirm that the Agent Studio MVP renders the
major local workbench pages, keeps safety copy visible, and does not expose
publication, tag, release, solver-run, or external LLM controls.

## 2. Current Status

- Current public prerelease: v0.9.0rc6
- Current main development version: `0.9.0rc7.dev0`
- Frontend MVP implemented and hardened
- API contract version: 0.1
- Visual smoke: manual / optional
- PyPI: not published
- v0.9.0rc7 tag: not created

The visual smoke is not part of the default release gate or
`./scripts/run_quality_gates.sh`.

## 3. Run Command

Preferred wrapper:

```bash
./scripts/smoke_frontend_visual.sh
```

Manual frontend-only form, assuming the local Agent API is already running:

```bash
cd frontend
npm install
npx playwright install chromium
npm run visual:smoke
```

The wrapper starts the local API if needed. The frontend dev server is started
by `frontend/playwright.config.ts` through Playwright `webServer`.
The wrapper attempts `npx playwright install chromium`; if the browser download
is unavailable, it continues with the configured local Chrome channel and the
visual smoke result still reports honestly.

## 4. What It Checks

- Dashboard
- Spec Input
- Adapter Matrix
- Workflow Plan
- Artifact Preview
- Validation Evidence
- System Status
- Safety notices remain visible
- Forbidden controls are absent

Forbidden controls include PyPI/TestPyPI upload controls, tag/release controls,
solver-run controls, and external LLM controls.

## 5. Safety Notes

- No solver execution.
- No external LLM call.
- No package upload.
- No tag creation.
- No GitHub release creation.
- No PyPI/TestPyPI controls.
- No production-grade physical validation claim.
- No formal convergence proof claim.

## 6. Artifacts

The following generated paths are ignored and should not be committed by
default:

- `frontend/test-results/`
- `frontend/playwright-report/`
- `test-results/`
- `playwright-report/`
- `frontend/dist/`
- `frontend/build/`
- `frontend/node_modules/`
