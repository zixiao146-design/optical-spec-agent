# Current Release Blockers

This audit reflects the repository state after commit
`76d1646 Add release engineering quality gates`.

## Hard Blockers

These block a release candidate:

- `make check` fails.
- `pytest -q` fails.
- `python -m build` fails.
- `twine check dist/*` fails.
- README/docs claims contradict code behavior.
- Release docs imply production-grade physical validation.
- Default CI requires Meep, MPB, Gmsh, Elmer, Optiland, or an external LLM API.
- Generated artifacts are accidentally committed as release evidence without
  provenance.

Current hard blocker status: **none known**.

## Soft Blockers

These do not block an RC, but must be explained in release notes:

- GitHub release/tag for `0.9.0rc1` remains manual and has not been created.
- v0.9 workflow orchestration is local/synchronous preview.
- External solvers do not run by default.
- External LLM providers are not enabled by default.
- Adapter outputs are MVP/scaffold inputs.

## Non-Blockers

These are known limitations and should stay visible, but they are not release
blockers for an engineering release candidate:

- No production-grade physical validation.
- No formal convergence proof.
- No full solver automation.
- No external solver execution in CI.
- Mock LLM is a deterministic test provider, not proof of real model quality.
- Meep execution remains optional/local.

## Current Status

Current blocker status: **ready for RC validation, not blocked**.

Recommended next action: review the `0.9.0rc1` version bump diff and quality
gate results. A maintainer should explicitly approve any manual tag/release
process.
