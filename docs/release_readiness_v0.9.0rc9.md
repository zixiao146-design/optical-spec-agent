# v0.9.0rc9 Development Readiness

This document tracks post-v0.9.0rc8 development readiness on `main`. It is not
a release draft, tag, GitHub release, TestPyPI upload, PyPI publication, or
v1.0.0 release authorization.

## Baseline

- Current public prerelease: v0.9.0rc8
- v0.9.0rc8 release URL:
  https://github.com/zixiao146-design/optical-spec-agent/releases/tag/v0.9.0rc8
- v0.9.0rc8 target commit: e9b219863026665dcf59c52a4dc29205eb1e15f4
- Current main development version: 0.9.0rc9.dev0
- v0.9.0rc9 tag: not created
- v1.0.0 tag: not created
- PyPI: not published
- TestPyPI uploaded and verified only for 0.9.0rc6.dev0
- TestPyPI upload for 0.9.0rc9.dev0: not performed
- PyPI publication approval: not granted

## Why Main Moved To 0.9.0rc9.dev0

v0.9.0rc8 is already a published GitHub prerelease. Post-release commits on
`main` should not keep building as 0.9.0rc8. The 0.9.0rc9.dev0 version marks
post-rc8 development toward the next candidate. 0.9.0rc9.dev0 is not itself a
public release.

## v0.9.0rc9 Development Goals

- Continue v1.0 readiness/backend engineering.
- Review whether rc8 backend evidence is enough for a future PyPI decision.
- Keep the v1.0 public contract freeze stable.
- Keep quality gates passing.
- Keep TestPyPI and PyPI publication boundaries explicit.
- Keep the open-source-solver-first strategy.
- Keep proprietary solvers non-default/export-only.
- Keep external solver and external LLM use optional.
- Continue validation maturity work without overclaiming physical correctness.
- Keep Elmer deferred unless a maintainable install route exists.
- Decide whether backend evidence should be surfaced in the frontend later.
- Decide whether to prepare a v1.0.0 planning package later.

## Required Checks Before A Future v0.9.0rc9 Release Draft

- `project.version` must change from 0.9.0rc9.dev0 to 0.9.0rc9.
- `__version__` must match.
- Validation claim audit passed.
- Application domain benchmarks passed.
- Optional solver wrapper default no-execute passed.
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
- Dist filenames must contain 0.9.0rc9.
- Release draft notes must exist.
- v0.9.0rc9 tag must be absent before creation.
- PyPI/TestPyPI decision must be explicit.

## Non-goals

- Do not publish PyPI now.
- Do not upload TestPyPI now.
- Do not create the v0.9.0rc9 tag now.
- Do not create the v1.0.0 tag now.
- Do not claim production-grade physical validation.
- Do not claim production-grade solver validation.
- Do not claim formal convergence proof.
- Do not claim optical correctness.
- Do not require an external solver or external LLM by default.
- Do not require a proprietary solver by default.

## Evidence Carried Forward

- Application domain benchmarks: 19 pass / 0 warn / 0 fail.
- Optional solver evidence closed for Gmsh, Optiland, Meep, and MPB.
- Elmer remains deferred and not Level 3.
- Backend validation maturity matrix is available.
- Preview boundary policy is available.
- Validation claim audit is available.
- Backend evidence pack and backend capability report are available.
- PyPI remains unpublished and PyPI publication approval remains not granted.
