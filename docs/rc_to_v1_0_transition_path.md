# RC to v1.0.0 Transition Path

`v0.9.0rc7` is the current public prerelease. `main` is
`0.9.0rc8.dev0`. The `v0.9.0rc8` tag has not been created, `v1.0.0` has not
been released, and PyPI remains unpublished.

## Transition facts

- rc8 may or may not be needed.
- v1.0.0 requires separate maintainer approval.
- PyPI publication remains separate from GitHub release planning.
- After any release, `main` must move to the next development state.

## Version transition options

- `0.9.0rc8.dev0` -> `0.9.0rc8` release draft -> `v0.9.0rc8` tag
  if more release candidates are needed.
- `0.9.0rc8.dev0` -> `1.0.0` release draft if v1.0.0 criteria are satisfied
  and the maintainer explicitly approves.

## Required guardrails

- Do not create `v0.9.0rc8` without approval.
- Do not create `v1.0.0` without approval.
- Do not publish PyPI without separate approval.
- Keep the v1.0 public contract freeze approved and current.
- Keep production-grade physical validation and formal convergence proof out of
  scope unless separately approved and evidenced.
