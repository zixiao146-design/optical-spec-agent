# Benchmark Contract

Benchmarks are deterministic quality gates for extraction, adapter intent, and
workflow completeness. They do not test physical correctness.

## Benchmarks

| Benchmark | Command | What it tests |
|---|---|---|
| Golden key fields | `python benchmarks/run_benchmark.py --mode key_fields` | Stable parser key fields. |
| Golden exact | `python benchmarks/run_benchmark.py --mode exact` | Full snapshot drift review. |
| Semantic | `python benchmarks/run_semantic_benchmark.py` | Intent and field-level semantic checks. |
| Semantic report | `python benchmarks/run_semantic_benchmark.py --report outputs/semantic_benchmark_report.json` | Machine-readable semantic report. |
| LLM mock | `python benchmarks/run_llm_benchmark.py --cases benchmarks/llm_cases.json --parser hybrid --llm-provider mock --report outputs/llm_eval_report.json` | Deterministic parser benchmark with mock provider. |
| Workflow | `python benchmarks/run_workflow_benchmark.py --cases benchmarks/workflow_cases.json --output-dir outputs/workflow_benchmark --report outputs/workflow_benchmark_report.json` | Workflow artifact completeness and false-claim checks. |

## Report Expectations

Reports should include a `schema_version`, total/passed/failed counts, and a
case-level result list.

## Non-Goals

- No external solver execution.
- No external LLM API.
- No production-grade physical validation.
- No formal convergence proof.
