# Current Release Readiness

This document describes the current `main` branch. It is not a release tag.

## Current State

- `pyproject.toml` packaged version: `0.5.0`
- Formal GitHub release: may lag behind `main`
- Main branch capabilities:
  - v0.6 local/manual post-hoc diagnostics
  - v0.7 multi-solver adapter MVP scaffolds
  - v0.8 LLM parser foundation with deterministic mock provider
  - v0.9 synchronous local workflow orchestration foundation

## Capability Matrix

| Area | Main branch status | Release note |
|---|---|---|
| Rule parser | Stable baseline | Default parser |
| Diagnostics | Main branch preview | Does not run Meep |
| Meep execution harness | Optional local/manual | Meep not required in CI |
| MPB/Gmsh/Elmer/Optiland adapters | MVP scaffold generation | Do not run external solvers |
| LLM parser foundation | Main branch preview | Mock provider is deterministic |
| Workflow orchestration | Main branch preview | Local and synchronous |

## Quality Gates

Run these before proposing a release:

```bash
pip install -e ".[dev]"
pytest -q
python benchmarks/run_benchmark.py --mode key_fields
python benchmarks/run_semantic_benchmark.py
python benchmarks/run_semantic_benchmark.py --report outputs/semantic_benchmark_report.json
python benchmarks/run_llm_benchmark.py --cases benchmarks/llm_cases.json --parser hybrid --llm-provider mock --report outputs/llm_eval_report.json
python benchmarks/run_workflow_benchmark.py --cases benchmarks/workflow_cases.json --output-dir outputs/workflow_benchmark --report outputs/workflow_benchmark_report.json
python scripts/check_cli_surface.py
python scripts/check_docs_consistency.py
python scripts/check_release_readiness.py --report outputs/release_readiness_report.json
python scripts/check_artifact_contracts.py
make check
python -m build
twine check dist/*
```

## Recommended Version Action

Current recommendation: keep `pyproject.toml` at `0.5.0` until a human release
decision is made. If the next formal package should include v0.6-v0.9 work, use
`docs/versioning_policy.md` to choose between a `0.8.0` or `0.9.0` release.

## Release Blockers

- Human decision needed on next version number.
- Confirm whether workflow orchestration should ship in the next formal package
  or remain main-branch preview.
- Confirm that generated adapter scaffolds are still presented as MVP inputs.
- Confirm that default CI remains free of external solver and external LLM
  requirements.

## Known Limitations

- No production-grade physical validation.
- No formal convergence proof.
- No full solver automation.
- No external solver execution in default CI.
- No external LLM provider required by default.
- Mock LLM evaluation is deterministic and not a real model-quality proof.
- Adapter outputs remain scaffold/MVP unless separately validated.
- Meep execution remains optional/local.

## Manual Release Checklist

1. Run all quality gates above.
2. Review `docs/release_notes_current.md`.
3. Decide the next version number.
4. Update `pyproject.toml` and `src/optical_spec_agent/__init__.py` only after
   that decision.
5. Build with `python -m build`.
6. Check distributions with `twine check dist/*`.
7. Create a release branch or tag manually.
8. Publish GitHub/PyPI artifacts manually after review.
