# CLI Contract

The `optical-spec` CLI is the primary local interface.

## Stable Commands

- `parse`
- `validate`
- `schema`
- `example`
- `meep-generate`
- `meep-check`
- `meep-run`
- `diagnose`
- `adapter-list`
- `adapter-generate`
- `llm-eval`
- `workflow-plan`
- `workflow-run`
- `workflow-replay`
- `workflow-report`

## Exit Code Policy

- Success: `0`
- Warning but completed: `0` unless a command exposes and receives `--strict`
- Missing input file: nonzero
- Validation or generation failure: nonzero
- Unsupported parser/provider/tool: nonzero
- Optional solver unavailable: command-specific warning or unavailable status

## JSON Output Policy

When a command exposes `--json`, stdout should contain machine-readable JSON
without mixed Rich/plain text summaries.

## External Execution Policy

- `parse`, `validate`, `schema`, `diagnose`, `adapter-list`,
  `adapter-generate`, `llm-eval`, and `workflow-*` do not run MPB/Gmsh/Elmer or
  Optiland.
- `meep-run` can run an existing Meep script only when explicitly invoked.
- `workflow-run` defaults to no solver execution.

## Contract Check

Run:

```bash
python scripts/check_cli_surface.py
```
