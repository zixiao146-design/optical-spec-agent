# v0.9.0rc3 Release Readiness

## Baseline

- Current public pre-release: `v0.9.0rc2`
- `v0.9.0rc2` tag target: `510f275c81599e10cfcec1a5acc7d6c3fd8aee8a`
- `v0.9.0rc3` draft version: `0.9.0rc3`
- `v0.9.0rc3` tag: not created
- PyPI/TestPyPI: not published / not uploaded

## Included Post-rc2 Hardening

- v1.0 readiness foundation.
- v1.0 contract stabilization.
- Validation and packaging gates.
- `0.9.0rc3.dev0` development-state correction into `0.9.0rc3` release-draft
  state.
- Wheel install smoke.
- Packaging gate.
- Validation gate.
- External solver policy.
- External LLM policy.
- Documented offline CLI examples.

## Required Checks Before Tag Creation

- `git status` is clean.
- `project.version == "0.9.0rc3"`.
- `optical_spec_agent.__version__ == "0.9.0rc3"`.
- `v0.9.0rc3` tag is absent locally and remotely.
- `scripts/smoke_release.sh` passed.
- Wheel smoke passed.
- `pytest` passed.
- `python -m build` passed.
- `make check` passed.
- Dist filenames contain `0.9.0rc3`.
- `optical-spec` CLI examples passed.
- Release draft exists: `docs/github_release_draft_v0.9.0rc3.md`.
- No PyPI/TestPyPI publication.

## Current Verification

- `scripts/smoke_release.sh`: passed.
- Wheel smoke: passed.
- `pytest`: 357 passed, 4 warnings.
- `python -m build`: passed.
- `make check`: passed.
- CLI examples: passed.
- Dist files:
  - `optical_spec_agent-0.9.0rc3-py3-none-any.whl`
  - `optical_spec_agent-0.9.0rc3.tar.gz`

## Next Step

After maintainer approval:

1. Confirm `git status` is clean.
2. Confirm local and remote `v0.9.0rc3` tags are absent.
3. Create an annotated `v0.9.0rc3` tag.
4. Push the tag.
5. Create the GitHub pre-release.
6. Verify `draft=false` and `prerelease=true`.
7. Create `docs/post_release_status_v0.9.0rc3.md`.
8. Do not publish PyPI unless explicitly approved.

## Remaining Limitations

- No production-grade physical validation.
- No formal convergence proof.
- External solvers are not run by default.
- External LLM providers are not required by default.
- Adapter outputs may still be MVP/scaffold unless explicitly validated.
- Workflow orchestration is a local/synchronous preview.
- This RC is not final `1.0` stability.
