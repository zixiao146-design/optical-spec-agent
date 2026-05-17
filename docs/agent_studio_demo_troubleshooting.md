# Agent Studio Demo Troubleshooting

For first-run setup, prefer:

```bash
./scripts/bootstrap_demo_env.sh
source /tmp/osa-agent-studio-demo/bin/activate
./scripts/run_quickstart_demo.sh
```

## API Not Running

Start the local API:

```bash
python -m uvicorn optical_spec_agent.api.app:app --reload --host 127.0.0.1 --port 8000
```

Then check `http://127.0.0.1:8000/api/health`.

## Frontend Not Running

Start the frontend:

```bash
cd frontend
npm install
npm run dev -- --host 127.0.0.1 --port 5173
```

Then open `http://127.0.0.1:5173`.

## Port 8000 In Use

Stop the process using port 8000 or point `OSA_DEMO_API_URL` at an existing
compatible local API. The demo is local-only and does not need external network
access.

## Port 5173 In Use

Stop the process using port 5173 or use the already-running local frontend if it
serves the Agent Studio MVP.

## npm Not Installed

The Python API smoke can still run, but the frontend demo requires npm. Install
Node/npm using the maintainer's local development tooling before running the
frontend demo.

## Playwright Browser Download Fails

Playwright visual smoke is optional/manual. If the Chromium browser download
fails, use the local Chrome fallback documented by
`docs/frontend_visual_smoke_runbook.md`, or skip visual smoke and rely on API
and frontend smoke for this demo.

## API Disconnected Demo Mode

If the API is disconnected, the frontend uses labeled demo fixture mode. This is
useful for walkthroughs, but it is not live validation. Start the API and retry
the action to demonstrate live local responses.

## Chinese Guided Tutorial Missing

Confirm the sidebar language is set to 中文 and open Dashboard / Readiness. The
中文手把手教程 should appear there. The written tutorial is
`docs/agent_studio_chinese_guided_tutorial.md`, and terminology is tracked in
`docs/frontend_chinese_terminology.md`.

## CORS Issue

The FastAPI app is configured for local Vite origins such as
`http://127.0.0.1:5173` and `http://localhost:5173`. Confirm the frontend uses a
matching origin and API base URL.

## Stale frontend/dist

Remove `frontend/dist` before committing. Generated frontend build output is not
part of the demo package.

## node_modules Not Committed

Do not commit `node_modules`. The demo and smoke scripts install dependencies
locally when needed and remove generated artifacts where appropriate.

## No Token Needed

No token needed. The demo does not upload packages, publish PyPI/TestPyPI,
create tags, or create GitHub releases.
