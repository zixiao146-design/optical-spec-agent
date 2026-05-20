# Schema Compatibility Policy

Current main release draft: `0.9.0rc8`.
Current public prerelease: `v0.9.0rc7`.

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

Adapter family evidence fixtures for Gmsh, Elmer, MPB, and Optiland are local
scaffold compatibility evidence. They help stabilize generated artifact shape,
metadata, warnings, and defaults, but they do not assert solver-backed physical
correctness.

PyPI remains unpublished. TestPyPI contains the `0.9.0rc6.dev0` development
package. `v0.9.0rc7` is the current public prerelease, and the `v0.9.0rc8` tag
has not been created.
