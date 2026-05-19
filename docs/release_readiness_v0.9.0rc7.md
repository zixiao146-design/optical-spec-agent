# v0.9.0rc7 Release Draft Readiness

## Baseline

- Current public prerelease: v0.9.0rc6
- v0.9.0rc6 release URL: https://github.com/zixiao146-design/optical-spec-agent/releases/tag/v0.9.0rc6
- Current main release draft: v0.9.0rc7
- `pyproject.toml` version: 0.9.0rc7
- `optical_spec_agent.__version__`: 0.9.0rc7
- v0.9.0rc7 tag: not created
- GitHub release: not created
- v1.0.0: not released
- PyPI: not published
- PyPI publication approval: not granted
- TestPyPI uploaded and verified only for 0.9.0rc6.dev0
- TestPyPI upload for 0.9.0rc7: not performed
- v1.0 public contract freeze: approved
- Backend evidence review decision: sufficient for rc7 release draft

## Included Post-rc6 Hardening

- Material Library
- Optical design examples
- Sub-agent collaboration
- Agent Command Center
- Tool-call ledger
- Local optical calculators
- Calculator reference sanity cases
- Design requirement templates
- Natural-language to optical-language matching
- Source/monitor diagnostics
- Observable diagnostics
- Adapter-native mappings
- Adapter golden coverage metadata checks
- Backend evidence review pack
- Frontend quickstart/demo/localization work

## Required Checks Before Tag Creation

- `git status --short` clean.
- `project.version == 0.9.0rc7`.
- `optical_spec_agent.__version__ == 0.9.0rc7`.
- `v0.9.0rc7` tag absent.
- Backend evidence smoke passed.
- Backend capability smoke passed.
- Adapter-native golden checker passed.
- Sub-agent audit passed.
- API fixture check passed.
- API smoke passed.
- TestPyPI no-upload preflight passed.
- Normal smoke passed.
- Wheel smoke passed.
- `pytest` passed.
- `python -m build` passed.
- `make check` passed.
- Quality gates passed.
- CLI examples passed.
- Dist filenames contain `0.9.0rc7`.
- No PyPI upload.
- No TestPyPI upload for rc7.
- No tag/release until approval.

## Verification Snapshot

- backend evidence pack smoke: passed
- backend capability smoke: passed
- adapter-native golden checker: passed
- sub-agent audit: passed
- API fixture check: passed
- API smoke: passed
- quality gates: passed
- TestPyPI no-upload preflight: passed
- normal smoke: passed
- wheel smoke: passed
- pytest: 761 passed, 4 warnings
- python -m build: passed
- make check: passed, with the expected rc7 release-note consistency warning resolved by this release notes file
- CLI examples: passed
- dist files:
  - `optical_spec_agent-0.9.0rc7-py3-none-any.whl`
  - `optical_spec_agent-0.9.0rc7.tar.gz`

## Safety Boundaries

- No PyPI publication is approved.
- No TestPyPI upload for 0.9.0rc7 is approved or performed.
- No production-grade physical validation is claimed.
- No formal convergence proof is claimed.
- External solvers are not run by default.
- External LLMs are not required by default.
- Proprietary solvers are not required by default.
- Elmer remains Level 2 + Level-3-ready; Level 3 validation is deferred.
- Calculator results are sanity-checked preview/design-assist outputs, not
  production-grade validation.
- Adapter-native golden cases are preview metadata checks, not real solver
  monitor results.
- This RC is not final 1.0 stability.

## Next Step

- After maintainer approval, create an annotated `v0.9.0rc7` tag.
- Create the GitHub prerelease.
- Verify `draft=false` and `prerelease=true`.
- Add `docs/post_release_status_v0.9.0rc7.md`.
- Do not publish PyPI unless separately approved.
