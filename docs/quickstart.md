# Quickstart

## 1. What You Will Build / Run

Run a local Agent Studio demo that parses an optical spec, validates it,
selects an adapter, generates a workflow plan, previews solver input, and
reviews validation evidence.

This is a local-first, preview-first agent workflow for `optical-spec-agent`.
It uses the Local Agent API and Agent Studio frontend MVP.

## 2. What This Quickstart Does Not Do

- Does not run external solvers by default.
- Does not call external LLM by default.
- Does not publish PyPI/TestPyPI.
- Does not create tags/releases.
- Does not claim production-grade physical validation.
- Does not claim formal convergence proof.
- Does not copy external website content, branding, or assets.

## 3. Prerequisites

- Python 3.11.
- Node/npm.
- Local checkout of this repository.
- Current public prerelease: v0.9.0rc6.
- Current main development version: 0.9.0rc7.dev0.

## 4. One-command Setup

Prepare a throwaway local demo virtual environment and frontend dependencies:

```bash
./scripts/bootstrap_demo_env.sh
```

Default virtual environment:

```bash
/tmp/osa-agent-studio-demo
```

## 5. Run Local Demo

Activate the demo environment and start the quickstart:

```bash
source /tmp/osa-agent-studio-demo/bin/activate
./scripts/run_quickstart_demo.sh
```

For a non-interactive smoke run that exits after checks:

```bash
OSA_QUICKSTART_NO_HOLD=1 ./scripts/run_quickstart_demo.sh
```

Optional visual smoke remains manual:

```bash
OSA_QUICKSTART_WITH_VISUAL=1 OSA_QUICKSTART_NO_HOLD=1 ./scripts/run_quickstart_demo.sh
```

## 6. Open Agent Studio

- Frontend: http://127.0.0.1:5173
- API health: http://127.0.0.1:8000/api/health
- API docs: http://127.0.0.1:8000/docs

## 7. Guided Demo Steps

1. Load example spec.
2. Parse locally.
3. Validate.
4. View adapter matrix.
5. Generate workflow plan.
6. Preview artifact.
7. Review validation evidence.
8. Review readiness / next actions.

The frontend guided demo panel maps each step to the Local Agent API endpoint
used by Agent Studio.

## 8. Expected Success

You should see:

- API connected.
- Package version `0.9.0rc7.dev0`.
- `api_contract_version` `0.1`.
- No solver executed.
- No external LLM called.
- Preview-only warnings.
- Adapter evidence summary.
- PyPI not published.
- No tag/release controls.

## 9. Troubleshooting

Use `docs/agent_studio_demo_troubleshooting.md` for API startup, frontend
startup, port conflict, npm, Playwright, CORS, and fixture-mode troubleshooting.
