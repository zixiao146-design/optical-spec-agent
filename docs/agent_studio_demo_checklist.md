# Agent Studio Demo Checklist

## Pre-demo

- [ ] Quickstart docs reviewed: `docs/quickstart.md` and
      `docs/quickstart.zh-CN.md`.
- [ ] Chinese guided tutorial reviewed:
      `docs/agent_studio_chinese_guided_tutorial.md`.
- [ ] Chinese terminology reviewed: `docs/frontend_chinese_terminology.md`.
- [ ] `./scripts/bootstrap_demo_env.sh` completed for first-run setup if needed.
- [ ] `./scripts/run_quickstart_demo.sh` starts the local quickstart.
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

- [ ] Guided demo panel shows Load example spec, Parse locally, Validate spec,
      Review adapter matrix, Generate workflow plan, Preview artifact, Review
      validation evidence, and Review readiness / next action.
- [ ] 中文手把手教程 shows nine steps: 打开 Agent Studio, 查看 readiness / 系统状态,
      加载中文纳米颗粒示例, 本地解析规格, 验证规格, 查看适配器矩阵, 生成工作流计划,
      预览适配器产物, 查看验证证据和下一步建议.
- [ ] Dashboard shows readiness, API mode, package version, TestPyPI/PyPI
      status, and recommended next actions.
- [ ] Spec Input parse/validate works with the local API, or demo fixture mode
      works and is labeled as not live validation.
- [ ] Adapter Matrix shows five adapters: Gmsh, Meep, MPB, Optiland, and Elmer.
- [ ] Material Library shows local preview materials and a no-production-grade optical constants warning.
- [ ] Workflow Plan shows no solver execution.
- [ ] Artifact Preview shows the preview-only boundary.
- [ ] Agent Collaboration shows SpecAgent / MaterialAgent / AdapterAgent / SafetyAgent trace.
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
