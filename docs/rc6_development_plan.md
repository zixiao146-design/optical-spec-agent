# v0.9.0rc6 Development Plan

## Baseline

- Current public prerelease: v0.9.0rc5
- Current main development version: 0.9.0rc6.dev0
- v0.9.0rc6 tag: not created
- PyPI/TestPyPI: PyPI not published / TestPyPI uploaded for 0.9.0rc6.dev0

## Goals for rc6.dev cycle

- Keep the approved v1.0 public contract freeze current.
- Keep `docs/v1_0_public_contract_freeze_checklist.md` current.
- Keep `docs/v1_0_public_contract_freeze_confirmation.md`,
  `docs/v1_0_contract_frozen_surface.md`,
  `docs/v1_0_contract_non_goals.md`, and
  `docs/v1_0_breaking_change_policy.md` current after maintainer approval.
- Keep `docs/v1_0_public_contract_freeze_status.md` current.
- Keep `docs/publication_decision_record.md` current now that TestPyPI
  succeeded for 0.9.0rc6.dev0 and PyPI publication remains not granted.
- Keep `docs/pypi_publication_readiness_checklist.md` and
  `docs/pypi_post_publication_verification_plan.md` current before any PyPI
  approval.
- Improve release/quality documentation consistency.
- Decide future TestPyPI uploads explicitly per candidate.
- Keep quality gates passing.
- Keep adapter maturity documentation current.
- Optionally revisit Elmer only if a maintainable install route appears.
- Avoid overclaiming physical validation.

## Non-goals

- No tag creation now.
- No release creation now.
- No PyPI upload and no repeat TestPyPI upload now.
- No production-grade physical validation claim.
- No formal convergence proof claim.
- No proprietary solver dependency.

## Exit criteria before v0.9.0rc6 release draft

- `project.version` changed from `0.9.0rc6.dev0` to `0.9.0rc6`.
- Release notes exist.
- Readiness doc updated.
- Quality gates passed.
- TestPyPI preflight passed.
- Pytest/build/make check passed.
- CLI examples passed.
- PyPI/TestPyPI decision explicit.
- PyPI publication readiness checklist reviewed.
- PyPI post-publication verification plan prepared.
- Elmer deferred or validated status explicit.
- Public contract freeze approval remains recorded.
- Any frozen-surface changes have maintainer approval and migration notes.
