# Artifact Contracts

Artifacts are review aids and reproducibility handles. They are not physical
proofs by themselves.

| Artifact | Producer | Format | Required fields or columns | Deterministic | CI use |
|---|---|---|---|---|---|
| `spec.json` | `parse`, workflow parse step | JSON | OpticalSpec sections | Yes for rule/mock | Yes |
| `parser_report.json` | LLM/hybrid parse | JSON | parser mode, provider, warnings, errors | Yes with mock | Yes |
| `validation_report.json` | validator/workflow | JSON | status, errors, warnings | Yes | Yes |
| `mesh_report.csv` | `diagnose` | CSV | `check_name,value,threshold,unit,status,message` | Yes | Contract check |
| `flux_report.csv` | `diagnose` | CSV | `monitor_name,surface,value,unit,status,message` | Yes | Contract check |
| `execution_diagnostics.json` | `diagnose` | JSON | `schema_version`, `status`, `missing_artifacts`, `nan_detected`, `inf_detected`, `timeout_detected` | Yes | Contract check |
| `diagnostic_preview.png` | `diagnose` | PNG | non-empty file | Yes placeholder | Contract check |
| adapter scaffold | `adapter-generate` | `.py`, `.geo`, `.sif` | adapter-specific comments and metadata | Yes | CLI tests |
| `semantic_benchmark_report.json` | semantic benchmark | JSON | `schema_version`, counts, `cases` | Yes | CI/check |
| `llm_eval_report.json` | LLM benchmark | JSON | `schema_version`, counts, `field_accuracy`, `cases` | Yes with mock | Optional/CI |
| `workflow_run.json` | workflow runner | JSON | `schema_version`, `run_id`, `steps`, `artifacts`, `status` | Yes with mock/no-execute | Workflow check |
| `workflow_summary.md` | workflow report | Markdown | run metadata, limitations, next action | Yes with mock | Workflow tests |
| `release_readiness_report.json` | release checker | JSON | `schema_version`, `status`, `blockers`, `warnings`, `recommended_actions` | Mostly | Release check |

## Contract Checker

Run:

```bash
python scripts/check_artifact_contracts.py
```

The checker generates minimal deterministic artifacts under
`outputs/release_checks/artifact_contracts/` and validates required JSON fields,
CSV columns, and PNG existence. It does not run external solvers or call an
external LLM provider.
