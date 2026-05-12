# Post-Push CI Checklist: `0.9.0rc1`

Use this checklist after the release-candidate commit is pushed to `main`.

## Expected Workflows

- `.github/workflows/ci.yml`
- `.github/workflows/docs.yml`
- `.github/workflows/benchmarks.yml` when manually dispatched
- `.github/workflows/release-dry-run.yml` when manually dispatched

## Expected Checks

`ci.yml` should run:

- Python 3.11 / 3.12 install
- `make check`
- deterministic local tests and benchmarks

`docs.yml` should run:

- `python scripts/check_docs_consistency.py`
- `python scripts/check_cli_surface.py`
- `python scripts/check_release_readiness.py --report outputs/release_readiness_report.json`
- `python scripts/check_artifact_contracts.py --report outputs/artifact_contract_report.json`

`benchmarks.yml` should run on manual dispatch:

- golden parser benchmark
- semantic benchmark report
- mock LLM benchmark
- workflow benchmark
- report artifact upload

`release-dry-run.yml` should run on manual dispatch:

- release readiness report
- `python -m build`
- `twine check dist/*`
- dry-run artifact upload

## If CI Fails

- Treat `pytest`, benchmark, docs consistency, CLI surface, release readiness,
  artifact contract, build, or `twine check` failures as RC blockers.
- Treat external solver or external LLM availability as environment-only only
  if a workflow unexpectedly tries to use them; default CI should not require
  Meep, MPB, Gmsh, Elmer, Optiland, or external LLM APIs.
- Do not create the `v0.9.0rc1` tag until CI is green or the failure is clearly
  documented and accepted by maintainers.

## Manual Command Equivalents

```bash
pip install -e ".[dev]"
pytest -q
python benchmarks/run_benchmark.py --mode key_fields
python benchmarks/run_semantic_benchmark.py
python benchmarks/run_semantic_benchmark.py --report outputs/semantic_benchmark_report.json
python benchmarks/run_llm_benchmark.py --cases benchmarks/llm_cases.json --parser hybrid --llm-provider mock --report outputs/llm_eval_report.json
python benchmarks/run_workflow_benchmark.py --cases benchmarks/workflow_cases.json --output-dir outputs/workflow_benchmark --report outputs/workflow_benchmark_report.json
make check
python scripts/check_docs_consistency.py
python scripts/check_cli_surface.py
python scripts/check_release_readiness.py --report outputs/release_readiness_report.json
python scripts/check_artifact_contracts.py
python -m build
twine check dist/*
```
