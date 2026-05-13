# Packaging Gate

Version scope: current `main` `v0.9.0rc3` release draft after the verified
`v0.9.0rc2` pre-release.

## Current package baseline

- Package name: `optical-spec-agent`
- Current package version on `main`: `0.9.0rc3`
- Current main release draft: `v0.9.0rc3`
- Current public pre-release: `v0.9.0rc2`
- `v0.9.0rc2` tag remains unchanged.
- `v0.9.0rc3` tag: not created
- PyPI status: not published
- TestPyPI status: not published
- Build backend: `hatchling`
- Console script: `optical-spec`
- Expected build artifacts for current main:
  - `optical_spec_agent-0.9.0rc3-py3-none-any.whl`
  - `optical_spec_agent-0.9.0rc3.tar.gz`

## Packaging checks required before publication

- `python -m build` passes.
- Wheel and sdist filenames match the package version.
- `pip install` from the generated wheel works in a clean venv.
- `python -m pip install -e ".[test]"` works in a clean venv.
- `pytest` passes.
- `optical-spec --help` passes.
- README and README.zh-CN describe current release/development state accurately.
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
- TestPyPI upload requires explicit maintainer approval.
- TestPyPI upload must not be part of the default smoke script.
- TestPyPI verification should include clean install from TestPyPI and
  `optical-spec --help`.
- If TestPyPI is skipped, the skip decision must be explicitly documented.
- If TestPyPI fails, publish a new candidate or fix main; do not reuse an
  already-published version.

## PyPI gate

- PyPI publication requires explicit maintainer approval.
- PyPI publication should happen only after TestPyPI, or after an explicitly
  recorded decision to skip TestPyPI.
- PyPI release must not be performed by accidental script execution.
- Yanking/rollback policy should be documented before the first PyPI release.
- PyPI remains unpublished for now.

## Non-goals

- No PyPI publish now.
- No TestPyPI upload now.
- No automatic package publishing from `scripts/smoke_release.sh`.
- No claim of production-grade physical validation.
- No claim of formal convergence proof.
