# CLI Contract

Version scope: current public prerelease `v0.9.0rc4`; current `main`
development version `0.9.0rc5.dev0`. `v0.9.0rc5.dev0` is not a release, the
`v0.9.0rc5` tag has not been created, and PyPI/TestPyPI remain unpublished.
Continue v1.0 readiness engineering and prepare a `v0.9.0rc5.dev0` development version
only when accumulated changes should be published as another RC.

The `optical-spec` console script is the supported command-line entry point:

```toml
[project.scripts]
optical-spec = "optical_spec_agent.cli.main:app"
```

## Supported command list

| Command | Purpose | Stability |
|---|---|---|
| `parse` | Parse natural language into an `OpticalSpec` JSON document. | Public |
| `validate` | Validate an existing spec JSON file. | Public |
| `schema` | Export the `OpticalSpec` JSON Schema. | Public |
| `example` | Run built-in examples. | Public demo utility |
| `meep-generate` | Generate Meep Python input from a validated spec. | Research-preview |
| `meep-check` | Check whether Meep is importable locally. | Local/manual utility |
| `meep-run` | Run an existing generated Meep script explicitly. | Optional local harness |
| `adapter-list` | List registered solver-input adapters. | Public |
| `adapter-generate` | Generate solver-native input scaffolds through the adapter registry. | Public scaffold interface |
| `diagnose` | Generate post-hoc diagnostics for a spec and optional Meep artifacts. | Preview diagnostics |
| `llm-eval` | Run deterministic mock-provider LLM parser evaluation cases. | Evaluation utility |
| `workflow-plan` | Plan a synchronous local workflow. | Preview workflow |
| `workflow-run` | Run a synchronous local workflow and write `workflow_run.json`. | Preview workflow |
| `workflow-replay` | Replay an existing workflow run with deterministic local settings. | Preview workflow |
| `workflow-report` | Render workflow artifacts as Markdown or JSON. | Preview workflow |

## Stable arguments and options

- `parse TEXT` supports `--output`, `--json`, `--parser`, `--llm-provider`,
  `--llm-model`, `--llm-temperature`, `--no-llm-repair`, `--no-llm-fallback`,
  `--show-parser-report`, and `--parser-report-output`.
- `validate PATH` takes a spec JSON path.
- `schema` supports `--output`.
- `adapter-list` supports `--json`.
- `adapter-generate PATH` supports `--tool`, `--output`, `--json`, `--strict`,
  and adapter-specific options such as `--mesh` where documented by help text.
- `workflow-plan TEXT` supports `--parser`, `--llm-provider`, `--tool`,
  `--output`, and `--json`.
- `workflow-run TEXT` supports parser/tool selection, `--output-dir`,
  `--no-execute`, `--execute-meep`, diagnostics flags, strictness flags, and
  `--json`.

The help text is the source of truth for incidental wording. Contract tests
assert stable fragments rather than full rich-formatted help snapshots.

## Output expectations

- `--json` output must be parseable JSON and must not include rich console text.
- `schema --output` writes JSON Schema to the requested path.
- `parse --output` writes an `OpticalSpec` JSON file.
- `adapter-list --json` returns a top-level object with an `adapters` array.
- `workflow-plan --json` returns a `workflow_plan.v0.9` compatible object.
- Workflow commands write artifacts under the requested output directory.

## Research-preview commands

`meep-generate`, `meep-run`, `diagnose`, and `workflow-*` are engineering aids.
They do not imply production-grade physical validation or a formal convergence
proof. `adapter-generate` outputs for MPB, Gmsh, Elmer, and Optiland are
MVP/scaffold outputs unless separately validated.

## Default offline behavior

Default CLI paths must not require external LLM providers or external solvers.
The mock LLM provider is deterministic and local. External solver execution is
manual and explicit, currently only through `meep-run` or external commands run
by the user.

## Offline examples

```bash
optical-spec --help
optical-spec schema --output outputs/schema.json
optical-spec validate examples/specs/minimal_nanoparticle.json
optical-spec parse examples/specs/minimal_nanoparticle.json --json
optical-spec adapter-list --json
optical-spec workflow-plan examples/workflows/local_preview_request.json --json
```

The JSON example fixtures are documented in `examples/README.md` and tested by
`tests/test_documented_examples.py`. They do not require network access,
external solvers, or external LLM providers.
