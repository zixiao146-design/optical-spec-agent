# v1.0.0 Release Criteria

## Current baseline

- Current public prerelease: v0.9.0rc6
- Current main development version: 0.9.0rc7.dev0
- v1.0 public contract freeze: approved
- TestPyPI uploaded and verified for 0.9.0rc6.dev0
- PyPI published: no
- PyPI publication approval: not granted
- v1.0.0 released: no
- Local Agent API readiness: in progress
- Local Agent API status: frontend-readiness / candidate API
- Local Agent API contract version: 0.1
- Local Agent API response models: available
- Local Agent API frontend fixtures: `examples/api/`
- Frontend implementation: not started

## Required before v1.0.0

- Maintainer approval for v1.0.0 release is recorded.
- Final version is set to 1.0.0.
- `pyproject.toml` version == `1.0.0`.
- `src/optical_spec_agent/__init__.py` `__version__` == `1.0.0`.
- Public contract freeze remains approved.
- PyPI publication decision is recorded.
- Quality gates passed.
- GitHub Actions CI passed.
- TestPyPI no-upload or upload decision is explicit.
- `python -m pytest` passed.
- `python -m build` passed.
- `make check` passed.
- CLI examples passed.
- Wheel install smoke passed.
- Release notes exist.
- GitHub release draft exists.
- `v1.0.0` tag is absent before creation.
- Post-release status plan is ready.

## Validation scope allowed for v1.0.0

- Optional manual validation evidence is available for Gmsh / Meep / MPB /
  Optiland.
- Elmer Level 3 remains deferred unless explicitly validated later.
- v1.0.0 may be released without Elmer Level 3 if documentation remains clear.
- Production-grade physical validation is not claimed.
- Formal convergence proof is not claimed.

## Publication criteria

- PyPI publication is a separate approval.
- PyPI may be published only after explicit maintainer approval.
- TestPyPI verification has been completed for 0.9.0rc6.dev0.
- Final PyPI release may require another TestPyPI upload or an explicit skip
  record.

## Release blocker classification

| Item | Classification | Status | Required action |
|---|---|---|---|
| Public contract freeze | Hard blocker | Satisfied | Keep the approved freeze current and require approval for frozen-surface changes. |
| PyPI publication decision | Hard strategic decision | Pending / not granted | Decide GitHub-only, delayed PyPI, or approved PyPI publication before v1.0. |
| v1.0.0 release approval | Hard blocker | Pending | Record explicit maintainer approval before version/tag/release work. |
| Quality gates and CI | Hard blocker | Established | Re-run immediately before any v1.0.0 release action. |
| TestPyPI decision | Soft blocker | Verified for 0.9.0rc6.dev0 | Decide whether final 1.0.0 needs TestPyPI or an explicit skip record. |
| Elmer Level 3 | Deferred/non-blocker | Deferred | Keep Elmer Level 2 + Level-3-ready unless a maintainable validation route appears. |
| Production-grade validation | Non-goal | Not claimed | Do not add production-grade physical validation claims. |
| Formal convergence proof | Non-goal | Not claimed | Do not add formal convergence proof claims. |
| Frontend/API Agent Studio | Future work | Phase 2 direction | Not a v1.0 blocker. |
| Local Agent API readiness | Engineering track | In progress | Useful for future Agent Studio, but not a v1.0 blocker unless maintainers choose to gate on it. |
| Local Agent API contract freeze | Future decision | Not separately frozen | API remains frontend-readiness / candidate API until maintainer explicitly approves freezing it. |
| Frontend fixture readiness | Engineering track | Available under `examples/api/` | Useful for future Agent Studio mock data, but not a PyPI publication trigger. |
