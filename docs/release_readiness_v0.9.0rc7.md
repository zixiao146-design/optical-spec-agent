# v0.9.0rc7 Development Readiness

## 1. Baseline

- Current public prerelease: v0.9.0rc6
- v0.9.0rc6 release URL: https://github.com/zixiao146-design/optical-spec-agent/releases/tag/v0.9.0rc6
- v0.9.0rc6 target commit: cf40be6407ae6d8055894a056afa1a2c2b5874b2
- Current main development version: 0.9.0rc7.dev0
- v0.9.0rc7 tag: not created
- v1.0.0 tag: not created
- PyPI: not published
- TestPyPI uploaded and verified for 0.9.0rc6.dev0
- TestPyPI upload for 0.9.0rc7.dev0: not performed
- PyPI publication approval: not granted

## 2. Why main moved to 0.9.0rc7.dev0

- v0.9.0rc6 is already a published GitHub prerelease.
- Post-release commits on main should not keep building as 0.9.0rc6.
- 0.9.0rc7.dev0 marks post-rc6 development toward the next candidate.
- v0.9.0rc7.dev0 is not itself a public release.

## 3. v0.9.0rc7 development goals

- Continue v1.0 readiness engineering.
- Decide whether/when to approve PyPI publication.
- Keep v1.0 public contract freeze stable.
- Keep quality gates passing.
- Keep TestPyPI/PyPI publication boundaries explicit.
- Keep open-source-solver-first strategy.
- Keep proprietary solvers non-default/export-only.
- Keep external solver and external LLM optional.
- Continue validation maturity work without overclaiming physical correctness.
- Optionally revisit Elmer validation only when maintainable install route exists.
- Evaluate API/frontend agent studio only after backend/public contract remains stable.

## 4. Required checks before future v0.9.0rc7 release draft

- `project.version` must change from `0.9.0rc7.dev0` to `0.9.0rc7`.
- `optical_spec_agent.__version__` must match.
- TestPyPI no-upload preflight passed.
- Quality gates passed.
- `smoke_release.sh` passed.
- Wheel smoke passed.
- `pytest` passed.
- `python -m build` passed.
- `make check` passed.
- CLI examples passed.
- E2E examples passed.
- Dist filenames must contain `0.9.0rc7`.
- Release draft notes must exist.
- `v0.9.0rc7` tag must be absent before creation.
- PyPI/TestPyPI decision must be explicit.

## 5. Non-goals

- Do not publish PyPI now.
- Do not upload TestPyPI now.
- Do not create `v0.9.0rc7` tag now.
- Do not create `v1.0.0` tag now.
- Do not claim production-grade physical validation.
- Do not claim formal convergence proof.
- Do not require external solver or external LLM by default.
- Do not require proprietary solver by default.
