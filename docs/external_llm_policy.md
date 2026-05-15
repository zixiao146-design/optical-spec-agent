# External LLM Policy

External LLM access is not required by default.

Current public prerelease: `v0.9.0rc4`. Current main release draft:
`0.9.0rc5`. `v0.9.0rc5` release draft is not a public release, the `v0.9.0rc5` tag has
not been created, and PyPI/TestPyPI remain unpublished. Continue v1.0 readiness
engineering and prepare a `v0.9.0rc5` release draft only when accumulated
changes should be published as another RC.

## Default behavior

- The rule parser remains available as the offline default.
- The mock LLM provider is deterministic and local.
- Default tests must not require network LLM calls.
- Default CI must not require external LLM credentials.

## Optional LLM-assisted parsing

LLM-assisted parsing is optional. Any future external provider integration
should:

- Be disabled by default.
- Require explicit provider selection.
- Fail clearly when credentials or providers are unavailable.
- Preserve deterministic mock-provider tests.
- Pass all LLM output through schema normalization, Pydantic validation,
  SpecValidator, provenance logging, and benchmark evaluation.

## Token and log safety

- Do not print, commit, or store provider tokens.
- Do not include secrets in prompts, parser reports, benchmark reports, or
  workflow artifacts.
- Redact sensitive input before logging if external providers are enabled.
- Prefer short-lived, least-privilege credentials.

## Expected failure modes

- Unsupported provider: clean error.
- Missing credentials: clean error.
- Malformed LLM output: repair/fallback path or visible parser error.
- Prompt injection attempt: schema contract still wins.

External LLM output is candidate extraction only; it is not physical validation.
