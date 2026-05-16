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

Do not commit `node_modules`, `frontend/dist`, or other build artifacts.

## 4. Demo / Fixture Mode

If the Local Agent API is unavailable, the frontend falls back to bundled demo
fixtures so the workbench remains navigable. Demo fixture mode is visibly
marked as not live validation. It does not run solvers, call external LLMs,
publish packages, create tags, or create releases.

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
