# v1.0 Compatibility Policy

## Purpose

`v1.0` compatibility means downstream users can rely on documented CLI, schema,
adapter registry, workflow preview, examples, and packaging behavior unless a
migration note is provided.

This policy applies to the current public prerelease `v0.9.0rc3` and current
`main` development version `0.9.0rc4.dev0`. The `v0.9.0rc4` tag has not been
created, and PyPI/TestPyPI remain unpublished/not uploaded.

## Compatibility scopes

- CLI command names and stable options documented in `docs/cli_contract.md`.
- JSON output top-level keys for documented commands such as `adapter-list
  --json` and `workflow-plan --json`.
- Schema public fields documented in `docs/schema_contract.md` and exported by
  `optical-spec schema`.
- Parser default offline path using the rule parser.
- Validation error categories and stable fragments for documented invalid
  inputs.
- Adapter registry names: `meep`, `mpb`, `gmsh`, `elmer`, and `optiland`.
- Adapter support matrix status and non-overclaiming limitations.
- Workflow preview output shape, especially top-level plan keys and
  no-execute-by-default policy.
- Examples paths intended for offline use under `examples/`.
- Package metadata and console script name `optical-spec`.

## Preview / non-stable scopes

- Adapter generated script internals may evolve before `v1.0`.
- Scaffold/MVP adapter outputs may change as richer schema fields are added.
- Workflow internals remain a local/synchronous preview.
- Physical validation claims are not production-grade.
- External solver validation remains optional/manual.
- External LLM path remains optional and is not required by default.

## Migration policy before v1.0

- Breaking changes before `v1.0` are allowed, but should be documented.
- Documented examples should be updated with tests.
- Release notes should mention user-visible contract changes.
- Schema changes should include migration notes if public fields change.
- Adapter registry name changes should include compatibility notes and updated
  support-matrix tests.

## v1.0 entry criteria

- CLI contract tests pass.
- Schema compatibility tests pass.
- Adapter matrix consistency tests pass.
- Workflow preview contract tests pass.
- Documented examples pass.
- Packaging gates pass.
- Validation boundary docs remain conservative.
- No external solver or LLM is required by default.
- No proprietary solver is a default dependency.
