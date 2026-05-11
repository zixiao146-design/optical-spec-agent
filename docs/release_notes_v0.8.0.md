# Draft Release Notes v0.8.0

> Draft only. No GitHub release or tag has been created.

## Summary

v0.8 introduces a safe LLM parser foundation while keeping the rule-based parser
as the default. It adds deterministic mock evaluation, schema-guided JSON
parsing, conservative hybrid merge, and parser reports.

## New

- `LLMParserConfig`
- `BaseLLMClient`
- deterministic `MockLLMClient`
- disabled external provider stub
- schema-guided prompt builder `llm_parser.v0.8`
- JSON extraction and repair helpers
- `LLMParser`
- `HybridParser`
- parser registry: `rule`, `llm`, `hybrid`
- `SpecService(parser=...)`
- CLI parser selection:
  - `--parser`
  - `--llm-provider`
  - `--llm-model`
  - `--no-llm-repair`
  - `--no-llm-fallback`
  - `--show-parser-report`
  - `--parser-report-output`
- API `/parse` parser selection
- `optical-spec llm-eval`
- `benchmarks/llm_cases.json`
- `benchmarks/run_llm_benchmark.py`

## Preserved

- Default parser remains rule-based.
- Existing parse/validate/schema/example commands remain.
- Meep, diagnose, and adapter commands remain.
- Tests do not require external LLM APIs or solvers.

## Limitations

- Mock provider is deterministic infrastructure, not a real intelligence
  benchmark.
- External LLM providers are not production-enabled.
- LLM parser extracts candidate specs only; it does not validate physical
  correctness.
- No production-grade physical validation or formal convergence proof is claimed.

## Suggested Verification

```bash
pytest -q
python benchmarks/run_benchmark.py --mode key_fields
python benchmarks/run_semantic_benchmark.py
python benchmarks/run_llm_benchmark.py --cases benchmarks/llm_cases.json --parser hybrid --llm-provider mock --report outputs/llm_eval_report.json
make check
```
