# Local Agent API Launch Guide

## Purpose

This guide explains how to run the local Agent API for Agent Studio frontend
development. The implemented MVP frontend runbook is
`docs/frontend_mvp_runbook.md`.

## Current status

- Current public prerelease: v0.9.0rc6
- Current main development version: 0.9.0rc7.dev0
- API contract version: 0.1
- Frontend implementation: MVP available under `frontend/`
- PyPI: not published

## Install local dev package

```bash
python -m pip install -e ".[test]"
```

## Start API locally

```bash
python -m uvicorn optical_spec_agent.api.app:app --reload --host 127.0.0.1 --port 8000
```

Interactive OpenAPI docs are available at `http://127.0.0.1:8000/docs` while
the server is running.

## Health check

```bash
curl http://127.0.0.1:8000/api/health
```

## Safety defaults

- No external solver execution by default.
- No external LLM call by default.
- No proprietary solver required.
- No production-grade physical validation claim.
- No formal convergence proof claim.
- Local, synchronous, preview-first behavior by default.

## Frontend handoff note

Future Agent Studio frontend work should call this local API rather than
shelling out directly to the CLI. CLI/API parity is tracked in
`docs/cli_api_parity.md`, and frontend fixture JSON lives under
`examples/api/`.

Frontend MVP planning is tracked in `docs/frontend_mvp_product_spec.md`,
`docs/frontend_information_architecture.md`, `docs/frontend_api_mapping.md`,
`docs/frontend_mvp_user_flows.md`,
`docs/frontend_mvp_acceptance_criteria.md`,
`docs/frontend_safety_policy.md`, and
`docs/frontend_mvp_implementation_plan.md`.

The MVP frontend lives under `frontend/` and is run with `npm run dev` after
starting the API. It remains local-first and does not expose solver execution,
external LLM, upload, publish, tag, or release controls.
Frontend hardening and local demo checks are tracked in
`docs/frontend_mvp_qa_checklist.md` and `scripts/smoke_frontend_mvp.sh`.
If the API is disconnected, demo fixture mode is visibly marked as not live
validation.
