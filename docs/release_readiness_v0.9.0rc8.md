# v0.9.0rc8 Development Readiness

## Baseline

- Current public prerelease: v0.9.0rc7
- v0.9.0rc7 release URL: https://github.com/zixiao146-design/optical-spec-agent/releases/tag/v0.9.0rc7
- v0.9.0rc7 target commit: 7040da21a51c556977be8c862ce889c351077e88
- Current main development version: 0.9.0rc8.dev0
- v0.9.0rc8 tag: not created
- v1.0.0 tag: not created
- PyPI: not published
- TestPyPI uploaded and verified only for 0.9.0rc6.dev0
- TestPyPI upload for 0.9.0rc8.dev0: not performed
- PyPI publication approval: not granted

## Why Main Moved to 0.9.0rc8.dev0

- v0.9.0rc7 is already a published GitHub prerelease.
- Post-release commits on main should not keep building as 0.9.0rc7.
- 0.9.0rc8.dev0 marks post-rc7 development toward the next candidate.
- v0.9.0rc8.dev0 is not itself a public release.

## v0.9.0rc8 Development Goals

- Continue v1.0 readiness/backend engineering.
- Continue backend evidence hardening only where needed.
- Decide whether and when to approve PyPI publication.
- Keep the v1.0 public contract freeze stable.
- Keep quality gates passing.
- Keep TestPyPI/PyPI publication boundaries explicit.
- Keep the open-source-solver-first strategy.
- Keep proprietary solvers non-default/export-only.
- Keep external solver and external LLM use optional.
- Continue validation maturity work without overclaiming physical correctness.
- Optionally revisit Elmer validation only when a maintainable install route exists.
- Decide whether to expose backend evidence in the frontend later.

## Required Checks Before a Future v0.9.0rc8 Release Draft

- `project.version` must change from 0.9.0rc8.dev0 to 0.9.0rc8.
- `optical_spec_agent.__version__` must match.
- Backend evidence smoke passed.
- TestPyPI no-upload preflight passed.
- Quality gates passed.
- `smoke_release.sh` passed.
- Wheel smoke passed.
- `pytest` passed.
- `python -m build` passed.
- `make check` passed.
- CLI examples passed.
- E2E examples passed.
- Dist filenames must contain 0.9.0rc8.
- Release draft notes must exist.
- v0.9.0rc8 tag must be absent before creation.
- PyPI/TestPyPI decision must be explicit.

## Non-goals

- Do not publish PyPI now.
- Do not upload TestPyPI now.
- Do not create the v0.9.0rc8 tag now.
- Do not create the v1.0.0 tag now.
- Do not claim production-grade physical validation.
- Do not claim formal convergence proof.
- Do not require external solver or external LLM by default.
- Do not require proprietary solver by default.
