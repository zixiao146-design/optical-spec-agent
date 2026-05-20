# rc9 Backend Stabilization Plan

This plan captures backend stabilization priorities for post-v0.9.0rc8
development on `0.9.0rc9.dev0`. It does not authorize a release draft, tag,
GitHub release, TestPyPI upload, or PyPI publication.

## Done / stable enough

- Application domain benchmarks: 19 pass / 0 warn / 0 fail.
- Optional solver evidence closed for Gmsh, Optiland, Meep, and MPB.
- Backend validation maturity matrix is available.
- Preview boundary policy is available.
- Material provenance and material suitability diagnostics are available.
- Ambiguous requirement matching and missing-input diagnostics are available.
- Backend evidence pack and backend capability report are available.
- Adapter-native golden preview metadata checks are available.

## Needs monitoring

- Validation claim audit must remain green after every readiness update.
- Default no-solver gates must continue to report no solver execution.
- Public contract manifest consistency must stay aligned with package version,
  current public prerelease, and PyPI/TestPyPI status.
- API fixture drift must be caught by `scripts/check_api_fixtures.py`.
- Solver evidence docs must preserve approval/execution/review separation.
- PyPI decision boundaries must remain explicit in publication docs.

## Deferred

- Elmer Level 3 remains deferred.
- No production-grade physical validation is claimed.
- No production-grade solver validation is claimed.
- No formal convergence proof is claimed.
- Proprietary solver workflows remain non-default/export-only.

## Future

- Consider frontend evidence surfacing later; no frontend UI is added by this
  backend audit task.
- Broaden material provenance sources only with clear user-verification notes.
- Add more analytic reference cases where they improve preview confidence.
- Add more design domains only when benchmark expectations and limitations are
  defined.
- Expand real solver benchmark evidence only with explicit opt-in approval for
  each run.
