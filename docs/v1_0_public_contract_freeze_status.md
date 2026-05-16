# v1.0 Public Contract Freeze Status

- Status: approved
- Approval type: maintainer-approved documentation freeze
- Approval date: 2026-05-16
- Current public prerelease: v0.9.0rc6
- Current main development version: 0.9.0rc7.dev0
- Freeze baseline commit: 6e7ddf9c1811685c12db16bffb55cd76455267fe
- TestPyPI uploaded and verified: yes
- PyPI published: no
- PyPI publication approval: not granted
- v1.0.0 released: no

## Frozen areas

- `optical-spec` console script
- Documented CLI commands
- Documented CLI options covered by tests
- Schema public fields
- Adapter registry names
- `adapter-list --json` top-level shape
- `workflow-plan --json` top-level shape
- Examples manifest
- Package metadata/versioning semantics
- No-default solver/LLM/proprietary guarantees

## Not frozen / not claimed

- Generated adapter internals
- Workflow internals
- Optional solver validation internals
- External LLM-assisted parsing internals
- Proprietary export-only targets
- Production-grade physical validation
- Formal convergence proof
- Elmer Level 3 validation

## Important

- This freeze does not publish PyPI.
- This freeze does not create `v1.0.0`.
- This freeze does not create any tag or GitHub release.
- PyPI publication remains separately gated.
- `v1.0.0` remains separately gated.
