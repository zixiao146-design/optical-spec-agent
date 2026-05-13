# v0.9.0rc5 Development Readiness

## Baseline

- Current public prerelease: v0.9.0rc4
- v0.9.0rc4 release URL: https://github.com/zixiao146-design/optical-spec-agent/releases/tag/v0.9.0rc4
- v0.9.0rc4 target commit: 497acc37a021db1af24629a77abab16f1d0f62f8
- Current main development version: 0.9.0rc5.dev0
- v0.9.0rc5 tag: not created
- PyPI/TestPyPI: not published / not uploaded
- TestPyPI upload approval: pending

## Why main moved to 0.9.0rc5.dev0

v0.9.0rc4 is already a published GitHub prerelease. Post-release commits on
`main` should not keep building as `0.9.0rc4`, because that would blur the
boundary between the verified public release candidate and new development
work. `0.9.0rc5.dev0` marks post-rc4 development toward the next candidate.
`v0.9.0rc5.dev0` is not itself a public release.

## v0.9.0rc5 Development Goals

- Continue v1.0 readiness engineering.
- Deepen public contract evidence.
- Improve validation evidence without overclaiming physical correctness.
- Keep the open-source-solver-first strategy.
- Keep proprietary solvers non-default/export-only.
- Keep external solver and external LLM paths optional.
- Keep TestPyPI/PyPI gated by explicit approval.
- Prepare for a future v1.0 stability review.

## Required Checks Before Future v0.9.0rc5 Release Draft

- `project.version` must change from `0.9.0rc5.dev0` to `0.9.0rc5`.
- `__version__` must match.
- TestPyPI no-upload preflight passed.
- `smoke_release.sh` passed.
- Wheel smoke passed.
- `pytest` passed.
- `python -m build` passed.
- `make check` passed.
- CLI examples passed.
- E2E examples passed.
- Quality gates passed.
- Dist filenames must contain `0.9.0rc5`.
- Release draft notes must exist.
- `v0.9.0rc5` tag must be absent before creation.
- PyPI/TestPyPI decision must be explicit.

## Non-goals

- Do not publish PyPI now.
- Do not upload TestPyPI now.
- Do not create `v0.9.0rc5` tag now.
- Do not claim production-grade physical validation.
- Do not claim formal convergence proof.
- Do not require external solver or external LLM by default.
- Do not require proprietary solver by default.
