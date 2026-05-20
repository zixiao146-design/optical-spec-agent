# v0.9.0rc8 Release Draft Readiness

## Baseline

- Current public prerelease: v0.9.0rc7
- v0.9.0rc7 release URL: https://github.com/zixiao146-design/optical-spec-agent/releases/tag/v0.9.0rc7
- Current main release draft: v0.9.0rc8
- v0.9.0rc8 tag: not created
- GitHub release: not created
- v1.0.0: not released
- PyPI: not published
- PyPI publication approval: not granted
- TestPyPI uploaded and verified only for 0.9.0rc6.dev0
- TestPyPI upload for 0.9.0rc8: not performed
- v1.0 public contract freeze: approved
- Optional solver evidence closed for Gmsh / Optiland / Meep / MPB.
- Elmer deferred and not Level 3.

## Included rc8 Hardening

- Material provenance.
- Ambiguous requirement matching.
- Missing-input diagnostics.
- Application domain registry.
- Application domain benchmarks.
- Fiber coupling calculator.
- Polarization calculator.
- Fiber/polarization reference sanity cases.
- Backend validation maturity matrix.
- Preview boundary policy.
- Validation claim audit.
- Optional solver readiness / approval / environment profiles.
- Optional solver evidence for Gmsh / Optiland / Meep / MPB.
- Optional solver evidence summary and rc8 backend readiness review.

## Required Checks Before Tag Creation

- git status clean.
- `project.version == 0.9.0rc8`.
- `__version__ == 0.9.0rc8`.
- v0.9.0rc8 tag absent.
- validation claim audit passed.
- application benchmarks passed.
- backend evidence smoke passed.
- quality gates passed.
- TestPyPI no-upload preflight passed.
- smoke passed.
- wheel smoke passed.
- pytest passed.
- build passed.
- make check passed.
- CLI examples passed.
- dist filenames contain 0.9.0rc8.
- no PyPI upload.
- no TestPyPI upload for rc8.
- no tag/release until approval.

## Validation Boundaries

- Production-grade physical validation: not claimed.
- Production-grade solver validation: not claimed.
- Production-grade FDTD validation: not claimed.
- Production-grade MPB validation: not claimed.
- Production band-structure validation: not claimed.
- Formal convergence proof: not claimed.
- Optical correctness: not claimed.
- External solvers are not default dependencies and are not run by default.
- External LLMs are not default dependencies and are not called by default.

## Next Step

After maintainer approval, create the annotated v0.9.0rc8 tag, create the
GitHub prerelease, verify `draft=false` and `prerelease=true`, and add
`docs/post_release_status_v0.9.0rc8.md`. Do not publish PyPI unless separately
approved.
