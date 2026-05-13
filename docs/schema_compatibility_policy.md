# Schema Compatibility Policy

Current main development version: `0.9.0rc4.dev0`.
Current public prerelease: `v0.9.0rc3`.

Schema/API compatibility is being stabilized before `v1.0`. Public fields
documented in `docs/schema_contract.md`, `docs/cli_contract.md`, and exported
through `optical-spec schema` should avoid breaking changes without migration
notes. Migration notes are required when public compatibility is intentionally
changed.

Preview/scaffold fields may change before `v1.0`, especially where adapter,
workflow, diagnostics, or solver-specific metadata is still marked as preview.
Those changes should still preserve deterministic local behavior for documented
offline examples.

Validation errors should remain deterministic for documented invalid inputs.
Tests may assert stable fragments and error categories rather than complete
localized text snapshots.

Default schema validation and parser paths must not require an external LLM.
Default schema validation must not require an external solver. External solver
or external LLM evidence may be added as optional/manual gates, but those gates
must not become default test dependencies.

PyPI/TestPyPI remain unpublished/not uploaded. `v0.9.0rc4.dev0` is not a public
release, and the `v0.9.0rc4` tag has not been created.
