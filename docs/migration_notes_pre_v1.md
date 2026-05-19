# Pre-v1 Migration Notes

## Current status

- Current public prerelease: v0.9.0rc7
- Current main development version: 0.9.0rc8.dev0
- v1.0.0 not released
- TestPyPI uploaded and verified for 0.9.0rc6.dev0
- PyPI published: no
- PyPI publication approval: not granted
- Public contract freeze: approved
- Public contract freeze status: `docs/v1_0_public_contract_freeze_status.md`
- Public contract freeze baseline commit:
  6e7ddf9c1811685c12db16bffb55cd76455267fe
- Public contract freeze source: `docs/v1_0_public_contract_freeze.md`
- Public contract manifest: `docs/public_contract_manifest.json`
- Public contract change checklist: `docs/public_contract_change_checklist.md`

## What may still change before v1.0

- Preview adapter internals.
- Scaffold/MVP generated script details.
- Workflow internal fields.
- Non-public schema internals.
- Optional solver validation paths.
- Preview/scaffold internals that are not declared frozen.

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
- After the approved public contract freeze, changes to the frozen public
  surface require maintainer approval.
- Breaking changes require explicit migration notes.
- Preview/scaffold internals may still change.
- `v1.0.0` final release and PyPI publication still require separate approval.
