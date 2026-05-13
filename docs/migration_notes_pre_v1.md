# Pre-v1 Migration Notes

## Current status

- Current public prerelease: v0.9.0rc3
- Current main development version: 0.9.0rc4.dev0
- v1.0.0 not released
- PyPI/TestPyPI not published/uploaded

## What may still change before v1.0

- Preview adapter internals.
- Scaffold/MVP generated script details.
- Workflow internal fields.
- Non-public schema internals.
- Optional solver validation paths.

## What should be stabilized toward v1.0

- CLI command names.
- Documented CLI options.
- Schema public fields.
- Adapter registry names.
- `adapter-list` JSON top-level shape.
- `workflow-plan` public top-level keys.
- Documented examples paths.
- Packaging metadata and console script.

## Migration expectations

- User-visible changes should be documented.
- Examples should be updated with tests.
- Release notes should mention contract changes.
- Schema public field changes should include migration notes.
