# Packaging Gate

Version scope: current `main` release draft `0.9.0rc4` after the
verified public `v0.9.0rc3` prerelease.

## Current package baseline

- Package name: `optical-spec-agent`
- Current package version on `main`: `0.9.0rc4`
- Current main release draft: `0.9.0rc4`
- Current public prerelease: `v0.9.0rc3`
- Product positioning: open-source-solver-first
- `v0.9.0rc1`, `v0.9.0rc2`, and `v0.9.0rc3` tags remain unchanged.
- `v0.9.0rc4` GitHub release: not created
- `v0.9.0rc4` tag: not created
- PyPI status: not published
- TestPyPI status: not published
- TestPyPI dry-run gate doc: `docs/testpypi_dry_run_gate.md`
- TestPyPI no-upload preflight script: `scripts/testpypi_preflight.sh`
- TestPyPI upload approval record:
  `docs/testpypi_upload_approval_v0.9.0rc4.md`
- TestPyPI upload approval status: pending
- TestPyPI upload authorized: no
- PyPI publication approval: not granted
- v1.0 stability gate doc: `docs/v1_0_stability_gate.md`
- Open-source solver strategy doc: `docs/open_source_solver_strategy.md`
- Proprietary solver policy doc: `docs/proprietary_solver_policy.md`
- Build backend: `hatchling`
- Console script: `optical-spec`
- Expected build artifacts for current main:
  - `optical_spec_agent-0.9.0rc4-py3-none-any.whl`
  - `optical_spec_agent-0.9.0rc4.tar.gz`

## Packaging checks required before publication

- `python -m build` passes.
- `scripts/testpypi_preflight.sh` passes for no-upload local publication readiness.
- Wheel and sdist filenames match the package version.
- `python -m twine check dist/*` passes.
- `pip install` from the generated wheel works in a clean venv.
- `python -m pip install -e ".[test]"` works in a clean venv.
- `pytest` passes.
- `optical-spec --help` passes.
- Offline documented examples pass:
  - `optical-spec validate examples/specs/minimal_nanoparticle.json`
  - `optical-spec parse examples/specs/minimal_nanoparticle.json --json`
  - `optical-spec workflow-plan examples/workflows/local_preview_request.json --json`
- README and README.zh-CN describe current release/development state accurately.
- No proprietary license is required for packaging checks, default tests, smoke,
  examples, or release validation.
- README renders acceptably for GitHub/PyPI.
- Package metadata is complete enough for the intended audience:
  - `project.name`
  - `project.version`
  - `project.description`
  - `project.readme`
  - `requires-python`
  - runtime dependencies
  - `optional-dependencies.test`
  - `project.scripts`
  - license metadata
  - project URLs and classifiers, if maintainers decide to publish on PyPI
- Release notes exist for the candidate.
- Post-release status doc is created only after release creation and verification.

## TestPyPI gate

- TestPyPI should be used before PyPI.
- The no-upload preflight performs local build, metadata checks, README/render
  checks through `twine check`, wheel install smoke, version import checks, and
  console script validation.
- The no-upload preflight does not upload, publish, create tags, or create
  GitHub releases.
- TestPyPI upload requires explicit maintainer approval.
- Approval remains pending in
  `docs/testpypi_upload_approval_v0.9.0rc4.md`.
- TestPyPI upload must not be part of the default smoke script.
- Wheel smoke remains local only.
- Smoke script must not publish or upload packages.
- TestPyPI verification should include clean install from TestPyPI and
  `optical-spec --help`.
- If TestPyPI is skipped, the skip decision must be explicitly documented.
- If TestPyPI fails, publish a new candidate or fix main; do not reuse an
  already-published version.

## PyPI gate

- PyPI publication requires explicit maintainer approval.
- PyPI publication is not approved by the TestPyPI approval record.
- PyPI publication should happen only after TestPyPI, or after an explicitly
  recorded decision to skip TestPyPI.
- PyPI release must not be performed by accidental script execution.
- Yanking/rollback policy should be documented before the first PyPI release.
- PyPI remains unpublished for now.
- No token should be printed or committed.

## Non-goals

- No PyPI publish now.
- No TestPyPI upload now.
- No upload from `scripts/testpypi_preflight.sh`.
- No automatic package publishing from `scripts/smoke_release.sh`.
- Do not publish automatically from release scripts.
- No claim of production-grade physical validation.
- No claim of formal convergence proof.
