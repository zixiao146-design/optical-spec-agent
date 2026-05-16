# v1.0 Breaking Change Policy

## Before v1.0

- Breaking changes may still occur.
- Breaking changes must be documented in migration notes.
- The public contract manifest should be updated when public CLI, schema,
  adapter, workflow, example, or package metadata boundaries change.

## After v1.0 freeze

- Changes to the frozen public surface require maintainer approval.
- Breaking changes require explicit migration notes.
- Generated internals may change unless documented as frozen.
- Preview/scaffold outputs may change.

## Versioning expectations

- Release candidates use `rcN`.
- Post-release main uses `rcN+1.dev0`.
- Final `v1.0.0` requires separate approval.

This policy does not authorize a v1.0 freeze, PyPI publication, tag creation,
GitHub release creation, production-grade physical validation claims, or formal
convergence proof claims.
