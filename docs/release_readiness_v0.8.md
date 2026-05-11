# v0.8 Release Readiness Draft

> This is a main-branch readiness note, not a GitHub release or tag.

## Achieved on Main

- Provider-agnostic LLM parser configuration and client interface.
- Deterministic `mock` provider for tests and demos.
- Schema-guided prompt builder.
- JSON extraction, common repair, normalization, and Pydantic validation.
- `LLMParser` and conservative `HybridParser`.
- Parser registry for `rule`, `llm`, and `hybrid`.
- `SpecService` parser selection.
- CLI parser selection and parser reports.
- API `/parse` parser selection.
- `llm-eval` CLI and `benchmarks/run_llm_benchmark.py`.
- 40-case LLM benchmark with deterministic mock provider.

## Verification Commands

```bash
pip install -e ".[dev]"
pytest -q
python benchmarks/run_benchmark.py --mode key_fields
python benchmarks/run_semantic_benchmark.py
python benchmarks/run_semantic_benchmark.py --report outputs/semantic_benchmark_report.json
python benchmarks/run_llm_benchmark.py --cases benchmarks/llm_cases.json --parser hybrid --llm-provider mock --report outputs/llm_eval_report.json
make check
```

Optional:

```bash
make llm-check
```

## Known Limitations

- No external LLM provider is required or enabled by default.
- Mock provider results are deterministic and local; they are not a real LLM
  quality benchmark.
- LLM parser extracts specs only; it does not validate physical correctness.
- No production-grade physical validation or formal convergence proof.
- Solver execution remains optional/local.
- Adapter scaffolds remain MVP-level where applicable.

## Release Blockers to Review

- Decide whether to bump package version from `0.5.0` directly to `0.8.0` or
  publish intermediate v0.6/v0.7 releases first.
- Review parser-report JSON naming before formalizing it as a long-term API.
- Review whether `make check` should include `make llm-check` in a future
  release. It is currently optional to keep the default gate unchanged.
