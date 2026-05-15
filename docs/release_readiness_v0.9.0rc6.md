# v0.9.0rc6 Development Readiness

## Baseline

- Current public prerelease: v0.9.0rc5
- v0.9.0rc5 release URL: https://github.com/zixiao146-design/optical-spec-agent/releases/tag/v0.9.0rc5
- v0.9.0rc5 target commit: accce88c88a7e823b6e71ff3e1b51b0ac08db781
- Current main development version: 0.9.0rc6.dev0
- v0.9.0rc6 tag: not created
- PyPI/TestPyPI: not published / not uploaded
- TestPyPI upload approval: pending

## Why Main Moved To 0.9.0rc6.dev0

- v0.9.0rc5 is already a published GitHub prerelease.
- Post-release commits on main should not keep building as 0.9.0rc5.
- 0.9.0rc6.dev0 marks post-rc5 development toward the next candidate.
- v0.9.0rc6.dev0 is not itself a public release.

## v0.9.0rc6 Development Goals

- Continue v1.0 readiness engineering.
- Decide whether to evaluate TestPyPI upload with explicit approval.
- Keep quality gates passing.
- Keep the open-source-solver-first strategy.
- Keep proprietary solvers non-default/export-only.
- Keep external solver and external LLM use optional.
- Keep TestPyPI/PyPI gated by explicit approval.
- Continue validation maturity work without overclaiming physical correctness.
- Optionally revisit Elmer validation only when a maintainable install route exists.

## Required Checks Before Future v0.9.0rc6 Release Draft

- `project.version` must change from `0.9.0rc6.dev0` to `0.9.0rc6`.
- `optical_spec_agent.__version__` must match.
- TestPyPI no-upload preflight passed.
- Quality gates passed.
- `smoke_release.sh` passed.
- Wheel smoke passed.
- Pytest passed.
- `python -m build` passed.
- `make check` passed.
- CLI examples passed.
- E2E examples passed.
- Dist filenames must contain `0.9.0rc6`.
- Release draft notes must exist.
- `v0.9.0rc6` tag must be absent before creation.
- PyPI/TestPyPI decision must be explicit.

## Non-goals

- Do not publish PyPI now.
- Do not upload TestPyPI now.
- Do not create `v0.9.0rc6` tag now.
- Do not claim production-grade physical validation.
- Do not claim formal convergence proof.
- Do not require external solver or external LLM by default.
- Do not require proprietary solver by default.
