# v0.9 Release Readiness Draft

> This is a main-branch readiness note, not a GitHub release or tag.

## Achieved on Main

- Synchronous local workflow models and runner.
- Workflow agents for intake, parse, validate, adapter selection, generation,
  execution planning, optional Meep execution, diagnostics, evaluation, review,
  and reporting.
- `workflow-plan`, `workflow-run`, `workflow-replay`, and `workflow-report` CLI.
- FastAPI workflow endpoints for plan/run/report.
- Standard workflow artifact layout and `workflow_run.json` source of truth.
- Human review checklist generation.
- Deterministic workflow replay report.
- Workflow benchmark and optional `make workflow-check`.

## Verification Commands

```bash
pip install -e ".[dev]"
pytest -q
python benchmarks/run_benchmark.py --mode key_fields
python benchmarks/run_semantic_benchmark.py
python benchmarks/run_semantic_benchmark.py --report outputs/semantic_benchmark_report.json
python benchmarks/run_llm_benchmark.py --cases benchmarks/llm_cases.json --parser hybrid --llm-provider mock --report outputs/llm_eval_report.json
python benchmarks/run_workflow_benchmark.py --cases benchmarks/workflow_cases.json --output-dir outputs/workflow_benchmark --report outputs/workflow_benchmark_report.json
make check
make workflow-check
```

## Manual Smoke Tests

```bash
optical-spec workflow-plan "用 Meep FDTD 仿真金纳米球-金膜 gap plasmon..."
optical-spec workflow-run "用 MPB 计算二维光子晶体 band diagram。" --parser hybrid --llm-provider mock --tool mpb --output-dir outputs/workflows/mpb_demo --no-execute
optical-spec workflow-replay outputs/workflows/mpb_demo/workflow_run.json --output-dir outputs/workflows/mpb_demo_replay
optical-spec workflow-report outputs/workflows/mpb_demo/workflow_run.json --output outputs/workflows/mpb_demo/report.md
```

## Known Limitations

- No async/background worker.
- No cloud execution.
- No automatic external solver execution for MPB/Gmsh/Elmer/Optiland.
- Meep execution remains optional/local.
- No production-grade physical validation.
- No formal convergence proof.
- Workflow artifacts support audit/replay/reporting; they are not scientific proof.

## Version Note

`pyproject.toml` remains at the packaged baseline `0.5.0`. A formal v0.9 release
would need an explicit version bump decision and release/tag process.

## Release Blockers

- Decide whether to publish intermediate v0.6/v0.7/v0.8 releases or jump to v0.9.
- Review workflow artifact schema names before long-term API stabilization.
- Decide whether `workflow-check` should join default `make check` in a future release.
