# Agent Studio Frontend MVP QA Checklist

## Current Status

- Current public prerelease: v0.9.0rc6
- Current main development version: `0.9.0rc7.dev0`
- API contract version: 0.1
- Frontend MVP: implemented under `frontend/`
- PyPI: not published
- v0.9.0rc7 tag: not created
- v1.0.0 tag: not created

## Local Demo Readiness

- Start the Local Agent API with `python -m uvicorn optical_spec_agent.api.app:app --reload --host 127.0.0.1 --port 8000`.
- Start the frontend with `cd frontend && npm run dev`.
- Confirm Dashboard loads live health, version, readiness, and recommended next actions.
- Confirm every page remains navigable if the API is disconnected.
- Confirm demo fixture mode is visibly labeled as not live validation.
- Confirm fixture loading buttons fill forms without calling the API until the
  user submits.
- Confirm Dashboard and System Status show the API mode indicator and API base
  URL.
- Confirm API disconnected state does not imply solver execution, external LLM calls, publication, tags, or releases.

## UX States

- Loading state appears while API requests are pending.
- Empty state appears before parse, validate, workflow, or preview actions are run.
- Error state appears for invalid JSON or API error responses.
- API disconnected notice appears when the local API cannot be reached.
- API mode indicator distinguishes API connected, API disconnected, and demo
  fixture mode.
- Diagnostics panels show warnings, missing fields, assumptions, and
  limitations without hiding them.
- Recommended next actions are visible when returned by the API.
- Buttons are disabled while the matching action is loading.
- Status and error regions use `aria-live`.

## Safety Boundaries

- No solver is executed by default.
- No external LLM is called by default.
- Preview artifacts are not production-grade physical validation.
- Formal convergence proof is not claimed.
- This UI does not control PyPI/TestPyPI publication or GitHub releases.
- No PyPI/TestPyPI upload buttons are present.
- No tag/release buttons are present.

## Accessibility Basics

- Pages use semantic headings.
- Textareas, selects, and action buttons have accessible labels.
- Loading, error, and API disconnected states are announced through status or alert regions.
- Controls that are waiting on a request are disabled.
- JSON panels remain scrollable without overlapping adjacent content.

## Verification

- `python scripts/check_api_fixtures.py`
- `./scripts/smoke_agent_api.sh`
- `./scripts/smoke_frontend_mvp.sh`
- `python -m pytest`
- `python -m build`
- `make check`
- `./scripts/run_quality_gates.sh`
- Future visual smoke plan: `docs/frontend_visual_smoke_plan.md`

## Generated Artifacts

- Do not commit `node_modules`.
- Do not commit `frontend/dist`.
- Do not commit `frontend/build`.
- Do not commit Python `dist/`, `build/`, egg-info, cache, or temporary venv artifacts.
