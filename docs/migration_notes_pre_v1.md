# Pre-v1 Migration Notes

## Current status

- Current public prerelease: v0.9.0rc5
- Current main development version: 0.9.0rc6.dev0
- v1.0.0 not released
- PyPI/TestPyPI not published/uploaded
- Public contract freeze candidate: `docs/v1_0_public_contract_freeze.md`
- Public contract manifest: `docs/public_contract_manifest.json`
- Public contract change checklist: `docs/public_contract_change_checklist.md`

## What may still change before v1.0

- Preview adapter internals.
- Scaffold/MVP generated script details.
- Workflow internal fields.
- Non-public schema internals.
- Optional solver validation paths.
- Public contract manifest fields before they are declared frozen for v1.0.

## What should be stabilized toward v1.0

- CLI command names.
- Documented CLI options.
- Schema public fields.
- Adapter registry names.
- `adapter-list` JSON top-level shape.
- `workflow-plan` public top-level keys.
- Documented examples paths.
- Packaging metadata and console script.
- Public contract manifest coverage.

## Migration expectations

- User-visible changes should be documented.
- Examples should be updated with tests.
- Release notes should mention contract changes.
- Schema public field changes should include migration notes.
- Changes to CLI command names, JSON top-level keys, adapter registry names,
  `workflow-plan` public keys, examples paths, or package metadata should update
  `docs/public_contract_manifest.json` and release notes.
