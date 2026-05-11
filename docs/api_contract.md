# API Contract

The FastAPI app exposes local parsing and validation helpers. API defaults do
not run solvers.

## Endpoints

| Endpoint | Method | Purpose |
|---|---|---|
| `/health` | GET | Return package health and version. |
| `/schema` | GET | Return the OpticalSpec JSON schema. |
| `/parse` | POST | Parse text into an OpticalSpec. |
| `/validate` | POST | Validate an OpticalSpec payload. |
| `/workflow/plan` | POST | Plan a local workflow when workflow code is present. |
| `/workflow/run` | POST | Run a synchronous no-execute workflow by default. |
| `/workflow/report` | POST | Render a workflow report from a run object. |

## Parse Request Defaults

```json
{
  "text": "用 Meep FDTD 仿真金纳米球-金膜 gap plasmon。",
  "parser": "rule",
  "llm_provider": "mock",
  "parser_report": false
}
```

- `parser=rule` is the backward-compatible default.
- `parser=llm` and `parser=hybrid` are available with the deterministic mock
  provider.
- Unsupported providers should return a clean client error.
- The API does not run external solvers.

## Workflow Defaults

- `allow_execute=false`
- `llm_provider=mock`
- no external solver execution
- output is orchestration metadata, not physical validation
