# PyPI Publication Decision

## Current status

- PyPI published: no.
- TestPyPI uploaded: no.
- Current public prerelease: `v0.9.0rc3`.
- Current main development version: `0.9.0rc4.dev0`.
- `v0.9.0rc4.dev0` is not a public release.
- `v0.9.0rc4` tag has not been created.
- Package build smoke: passed for the RC line.
- Packaging gate: `docs/packaging_gate.md`.
- Validation gate: `docs/validation_gate.md`.
- TestPyPI dry-run gate doc: `docs/testpypi_dry_run_gate.md`.
- TestPyPI no-upload preflight script: `scripts/testpypi_preflight.sh`.
- v1.0 stability gate doc: `docs/v1_0_stability_gate.md`.

## Recommendation

Use TestPyPI before any PyPI release. Do not publish from smoke scripts,
workflow automation, or local release engineering checks without explicit
maintainer approval.

`scripts/testpypi_preflight.sh` is a local no-upload check. It builds artifacts,
runs `python -m twine check dist/*`, installs the wheel in a clean environment,
checks `optical_spec_agent.__version__`, and runs `optical-spec --help`. It does
not upload, publish, create tags, or create GitHub releases.

## Preconditions before any PyPI publication

- Explicit maintainer approval is recorded.
- The decision record must include the phrase: explicit maintainer approval.
- `git status` is clean.
- Package version in `pyproject.toml` and `__version__` match.
- `scripts/smoke_release.sh` passes in a clean environment.
- Optional wheel install smoke passes with `OSA_SMOKE_VERIFY_WHEEL=1`.
- Wheel smoke remains local only and must not upload artifacts.
- `scripts/testpypi_preflight.sh` passes and prints `NO UPLOAD PERFORMED`.
- `pytest` passes.
- `python -m build` passes.
- `twine check dist/*` passes.
- Dist filenames match the candidate version.
- Release notes and post-release status docs are prepared.
- Token handling follows `docs/release_engineering_playbook.md`.
- No token is printed or committed.
- TestPyPI upload/install is evaluated first, unless maintainers explicitly
  waive it.

## Rollback and yanking considerations

PyPI artifacts are immutable by version. If a broken artifact is published,
maintainers should generally publish a new patch/RC version rather than attempt
to reuse the same version. Yanking may reduce accidental installs but does not
remove the artifact from all caches.

## Explicit non-goals

- Do not publish automatically from `scripts/smoke_release.sh`.
- Do not publish automatically from GitHub release creation.
- Do not publish as part of default CI.
- Do not publish without separate approval.
- Do not publish automatically from release scripts.
- Do not upload from `scripts/testpypi_preflight.sh`.
