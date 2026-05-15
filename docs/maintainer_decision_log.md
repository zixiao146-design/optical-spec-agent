# Maintainer Decision Log

## Current Decisions

- v0.9.0rc5 is the current public prerelease.
- main is prepared as the 0.9.0rc6.dev0 development state for maintainer review.
- TestPyPI upload approval: pending.
- Upload command authorized: no.
- PyPI publication approval: not granted.
- Continue v1.0 readiness engineering.
- Do not create v0.9.0rc6 tag now.
- Do not create a GitHub release now.
- Do not use proprietary solvers as default dependencies.
- Do not require external solver or external LLM by default.
- Do not publish PyPI without explicit approval.
- Do not upload TestPyPI without explicit approval.
- Use `docs/ci_quality_gate_parity.md` to compare local and CI quality gates.
- Use `docs/release_dry_run_operations.md` for no-upload release rehearsal.
- Follow `docs/secrets_and_token_hygiene.md` before any token-mediated action.
- Follow `docs/maintainer_operations_checklist.md` before RC, TestPyPI, or PyPI
  transitions.
- Use `docs/v1_0_gap_audit.md` to classify v1.0 blockers, deferred items, and
  future work.
- Use `docs/rc6_development_plan.md` for the active `0.9.0rc6.dev0`
  development scope.
- Use `docs/v1_0_decision_matrix.md` before deciding TestPyPI upload, PyPI
  publication, Elmer Level 3, production-validation scope, or public contract
  freeze.

## Safety Notes

- Tokens must not be printed, committed, logged, or pasted into chat.
- Default smoke, quality, and preflight scripts remain no-upload and no-release.
- Existing release tags must not be moved, deleted, or re-created.
