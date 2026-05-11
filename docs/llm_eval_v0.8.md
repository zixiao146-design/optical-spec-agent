# v0.8 LLM Parser Evaluation

The LLM evaluation harness is deterministic and offline. It evaluates parser
extraction behavior against explicit expected fields; it does not evaluate
physical correctness or solver results.

## Files

- `benchmarks/llm_cases.json`: v0.8 LLM parser cases.
- `benchmarks/run_llm_benchmark.py`: CLI runner.
- `outputs/llm_eval_report.json`: optional JSON report.
- `outputs/llm_eval_summary.csv`: optional CSV summary.

## Run

```bash
python benchmarks/run_llm_benchmark.py \
  --cases benchmarks/llm_cases.json \
  --parser hybrid \
  --llm-provider mock \
  --report outputs/llm_eval_report.json \
  --summary-csv outputs/llm_eval_summary.csv
```

Or through the package CLI:

```bash
optical-spec llm-eval benchmarks/llm_cases.json \
  --parser hybrid \
  --llm-provider mock \
  --report outputs/llm_eval_report.json
```

## Case Schema

Each case includes:

- `id`
- `text`
- `expected`: dotted `OpticalSpec` paths and expected values
- `allowed_missing`: fields that should remain missing for ambiguous requests
- `parser_modes`
- `notes`

## Report Schema

The report includes:

- `schema_version`
- `generated_at`
- `parser_mode`
- `provider`
- `model`
- `total_cases`
- `passed_cases`
- `failed_cases`
- `field_accuracy`
- `cases[]`

Each case records expected/actual values, missing handling, warnings, errors,
fallback usage, repair usage, and conflict count.

## Interpretation

Passing this benchmark means the parser can reproduce expected structured fields
under deterministic mock conditions. It does not mean:

- an external LLM provider is reliable;
- the extracted spec is physically correct;
- generated solver input is production-ready;
- solver execution or convergence has been validated.
