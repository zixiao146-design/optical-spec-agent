# v1.0 Readiness Plan

## Current baseline

- Current public prerelease: `v0.9.0rc3`
- Current main development version: `0.9.0rc4.dev0`
- `v0.9.0rc4.dev0` is not a release
- `v0.9.0rc4` tag has not been created
- Release URL: https://github.com/zixiao146-design/optical-spec-agent/releases/tag/v0.9.0rc3
- Release verified: yes
- Post-release status: `docs/post_release_status_v0.9.0rc3.md`
- Latest post-release status commit: `4d2991f`
- PyPI published: no
- TestPyPI uploaded: no

## What v0.9.0rc2 already proves

- Clean install with the test extra passed: `python -m pip install -e ".[test]"`.
- Test suite passed at release time: `pytest: 331 passed, 4 warnings`.
- Current main hardening baseline after `40ed807`: `pytest: 332 passed, 4 warnings`.
- Build passed and produced wheel/sdist artifacts.
- `optical-spec --help` passed.
- Release smoke automation exists: `scripts/smoke_release.sh`.
- GitHub pre-release was verified with `draft=false` and `prerelease=true`.

These prove the release-candidate engineering path is reproducible enough for
early adopters. They do not prove physical correctness of generated simulations.

## Remaining limitations

- No PyPI publish has been performed.
- No production-grade physical validation is claimed.
- No formal convergence proof is provided.
- External solvers are not run by default.
- External LLM providers are not required by default.
- Adapter outputs remain MVP/scaffold unless separately validated.
- Workflow orchestration is a local/synchronous preview.
- The RC is not final `1.0` stability.

## Recommended path to v0.9.0rc4

`v0.9.0rc4` should be prepared only when accumulated post-rc3 hardening changes
should be published as another RC. Recommended goals:

- TestPyPI gate dry-run foundation.
- Packaging metadata hardening.
- Wheel install smoke reliability.
- v1.0 stability gate.
- Stronger adapter golden-output regression tests.
- Better workflow replay and dry-run smoke coverage.
- Clearer CLI quickstart examples for local/no-network usage.
- Stronger release engineering playbook coverage.
- Optional external solver validation path documented, but not made default.
- Physical validation status clarified without overclaiming.
- PyPI remains unpublished unless explicitly approved.
- TestPyPI remains not uploaded unless explicitly approved.

## Recommended path to v1.0.0

Before `v1.0.0`, maintainers should decide and document:

- Stable public API and CLI contract: `docs/cli_contract.md` and
  `docs/schema_contract.md`.
- Supported adapters and their stability levels:
  `docs/adapter_support_matrix.md`.
- Workflow preview boundaries: `docs/workflow_preview_contract.md`.
- Unsupported assumptions, validation limits, and non-goals:
  `docs/validation_boundary.md`.
- Reproducible release procedure and rollback policy.
- Production-grade validation plan, or an explicit non-production disclaimer.
- Versioning policy for previews, RCs, and final releases.
- PyPI publication decision: `docs/pypi_publication_decision.md`.
- Packaging publication gate: `docs/packaging_gate.md`.
- Validation gate for RC/v1.0 readiness: `docs/validation_gate.md`.
- Optional external solver policy: `docs/external_solver_policy.md`.
- Optional external LLM policy: `docs/external_llm_policy.md`.
- Security and token-handling guidance for release operations.

## Immediate engineering priorities

### P0

- Release closure verification. Completed for `v0.9.0rc2`.
- Tag sync verification. Completed locally for `v0.9.0rc2`; repeat before any new tag.
- Release status visibility. Completed through post-release status docs.
- Smoke script reliability. Strengthened after `40ed807`.
- Public contract docs and regression tests. Added in current main.
- Packaging and validation gates. Added in current main.
- Optional external solver/LLM policy docs. Added in current main.
- Continue v1.0 readiness engineering from `0.9.0rc4.dev0`.

### P1

- Additional CLI examples around failure/strict modes.
- Adapter golden-output tests for non-Meep scaffold adapters.
- Workflow replay smoke tests for Meep/no-execute diagnostics.
- Release rollback playbook.

### P2

- TestPyPI evaluation only with explicit approval.
- Optional external solver gate.
- Expanded physical validation examples.

## Explicit non-goals

- Do not publish PyPI yet.
- Do not upload TestPyPI yet.
- Do not move `v0.9.0rc1`, `v0.9.0rc2`, or `v0.9.0rc3` tags.
- Do not create the `v0.9.0rc4` tag until final readiness checks and maintainer approval.
- Do not treat `v0.9.0rc4.dev0` as a published release.
- Do not claim production-grade physical validation.
- Do not claim formal convergence proof.
- Do not require external solver or external LLM by default.
