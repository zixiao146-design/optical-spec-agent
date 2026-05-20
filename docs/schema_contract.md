# Schema and API Contract

Version scope: current public prerelease `v0.9.0rc7`; current `main` development
version `0.9.0rc8`. The `v0.9.0rc8` tag has not been created, PyPI remains
unpublished, TestPyPI contains the `0.9.0rc6.dev0` development package, and
TestPyPI upload for `0.9.0rc8` has not been performed.

## Public spec model

The public schema is exported from `OpticalSpec` and contains these top-level
sections:

- `task`
- `physics`
- `geometry_material`
- `simulation`
- `output`
- `confirmed_fields`
- `inferred_fields`
- `missing_fields`
- `assumption_log`
- `validation_status`

The schema is available through both:

```bash
optical-spec schema --output outputs/schema.json
GET /schema
```

Compatibility policy is tracked in `docs/schema_compatibility_policy.md`.
The fixed valid spec `examples/specs/minimal_nanoparticle.json` and deterministic
invalid-spec regression tests provide v1.0-readiness evidence without external
solvers or external LLM providers.

## Minimum expectations

An executable simulation spec generally needs:

- `task.task_type`
- `task.research_goal`
- `simulation.solver_method`
- `simulation.software_tool`
- `simulation.excitation_source`
- `simulation.source_setting`
- `simulation.boundary_condition`
- `simulation.monitor_setting`

Domain-specific adapters may require more fields. For example,
`nanoparticle_on_film` generation needs particle, film/substrate, and gap-related
information to be meaningful.

## Optional and provenance fields

Most extraction fields are represented as status-bearing values with:

- `confirmed`: directly present in the user input or source artifact.
- `inferred`: conservatively inferred and recorded with notes/assumptions.
- `missing`: intentionally visible as missing rather than invented.

`assumption_log`, `confirmed_fields`, `inferred_fields`, and `missing_fields`
are public audit aids. They are not guarantees of physical correctness.

## Validation behavior

Validation is deterministic and local. It checks structural completeness,
task-aware required fields, and obvious consistency risks. It does not run
solvers, prove convergence, or validate production physical correctness.

Invalid specs should report deterministic validation errors through
`validation_status.errors` and should not silently become executable.

## Parser expectations

The default parser remains `rule`. `llm` and `hybrid` parser modes are available
through a provider-agnostic foundation with deterministic `mock` provider
support. External LLM providers are not required by default.

## API expectations

The public API surface includes:

- `GET /health`
- `POST /parse`
- `POST /validate`
- `GET /schema`
- Workflow endpoints where enabled by the application.

Old `/parse` requests with only `text` remain backward compatible. Parser
selection is optional and defaults to rule-based behavior.

## Not guaranteed yet

- No stable `1.0` schema freeze has been declared.
- No production-grade physical validation is claimed.
- No formal convergence proof is provided.
- No external solver execution is required or performed by default.
- No external LLM provider is required by default.
