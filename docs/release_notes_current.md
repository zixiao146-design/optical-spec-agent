# Current Draft Release Notes

Draft only. This document summarizes current `main` branch work since the
`0.5.0` packaged baseline and does not create a release.

## Summary

The current branch extends the v0.5 packaged Meep execution baseline with local
diagnostics, multi-solver input scaffolds, deterministic LLM parser evaluation,
and synchronous workflow orchestration.

## Since v0.5.0

- v0.6: post-hoc physical diagnostics via `optical-spec diagnose`.
- v0.7: adapter registry and `adapter-list` / `adapter-generate` for Meep,
  MPB, Gmsh, Elmer, and Optiland input scaffolds.
- v0.8: provider-agnostic parser foundation with deterministic mock LLM client,
  conservative hybrid parser, parser reports, and LLM benchmark.
- v0.9: local synchronous workflow orchestration with workflow artifacts,
  replay, reports, human-review checklist, and workflow benchmark.

## Quality Gates

- `pytest -q`
- `python benchmarks/run_benchmark.py --mode key_fields`
- `python benchmarks/run_semantic_benchmark.py`
- `python benchmarks/run_llm_benchmark.py --cases benchmarks/llm_cases.json --parser hybrid --llm-provider mock --report outputs/llm_eval_report.json`
- `python benchmarks/run_workflow_benchmark.py --cases benchmarks/workflow_cases.json --output-dir outputs/workflow_benchmark --report outputs/workflow_benchmark_report.json`
- `make check`

## Not Included

- No production-grade physical validation.
- No formal convergence proof.
- No automatic external solver execution for MPB/Gmsh/Elmer/Optiland.
- No mandatory external LLM provider.
- No solver result interpretation by LLM.

## Suggested Release Tag

Human decision required. If v0.9 workflow orchestration is included, `0.9.0` is
the clearest semantic tag. If workflow remains preview, consider `0.8.0`.
