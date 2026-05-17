# Agent Studio Demo Checklist

## Pre-demo

- [ ] `git status clean`.
- [ ] `python scripts/check_api_fixtures.py` passes.
- [ ] API smoke `./scripts/smoke_agent_api.sh` passes.
- [ ] frontend smoke `./scripts/smoke_frontend_mvp.sh` passes.
- [ ] optional visual smoke `./scripts/smoke_frontend_visual.sh` passes
      when the environment supports it.
- [ ] `node_modules`, `frontend/dist`, `frontend/build`,
      `frontend/test-results`, and `frontend/playwright-report` are not staged.
- [ ] Local API starts at `http://127.0.0.1:8000/api/health`.
- [ ] Local frontend starts at `http://127.0.0.1:5173`.
- [ ] No token is needed.

## During demo

- [ ] Dashboard shows readiness, API mode, package version, TestPyPI/PyPI
      status, and recommended next actions.
- [ ] Spec Input parse/validate works with the local API, or demo fixture mode
      works and is labeled as not live validation.
- [ ] Adapter Matrix shows five adapters: Gmsh, Meep, MPB, Optiland, and Elmer.
- [ ] Workflow Plan shows no solver execution.
- [ ] Artifact Preview shows the preview-only boundary.
- [ ] Validation Evidence shows Gmsh/Meep/MPB/Optiland Level 3 and Elmer
      deferred.
- [ ] System Status shows API contract version 0.1.
- [ ] Safety notices are visible.
- [ ] No upload/tag/release controls visible.
- [ ] No solver-run or external LLM controls visible.

## Post-demo

- [ ] Stop local servers.
- [ ] Confirm `git status clean` or only intentional docs/script changes.
- [ ] Remove `frontend/dist` if generated.
- [ ] Remove Playwright reports or screenshots if generated.
- [ ] Do not commit screenshots unless explicitly approved.
- [ ] Do not commit `node_modules`, frontend build output, Python build output,
      cache directories, or temporary venvs.
