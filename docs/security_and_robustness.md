# Security And Robustness Baseline

This repository is local-first and deterministic by default.

## Defaults

- No external API is required by default.
- CI uses the deterministic mock LLM provider only.
- External solvers are not run by default.
- Meep execution is optional and local.
- MPB/Gmsh/Elmer/Optiland adapters write scaffolds only.

## LLM Guardrails

- LLM output is parsed as JSON and never executed as code.
- Prompt-injection-like text is treated as input text, not instructions to
  change parser safety rules.
- Unknown or malformed JSON is repaired conservatively or falls back to the
  rule-based parser when configured.
- Secrets are not read from environment variables for default tests.

## CLI And Artifact Safety

- Commands create output directories when needed.
- Generated artifacts are review aids and should not be treated as solver
  results unless an execution artifact explicitly records a local solver run.
- Release/demo scripts avoid destructive filesystem operations.
- Manual local gates should write into `outputs/` or `runs/` and should not
  modify user system environments.

## Known Risks

- Adapter scaffolds are intentionally incomplete and need human review.
- Diagnostics can detect red flags such as missing artifacts, NaN/Inf, timeout,
  and under-resolved mesh settings, but they cannot prove physical correctness.
- Mock LLM benchmark success is not evidence of real model quality.
- Manual Meep runs can be slow or unstable and must use explicit timeouts.

## Reporting Security Issues

Open a private advisory or contact the maintainer before publishing details for
any issue involving code execution, path traversal, secret exposure, or unsafe
artifact handling.
