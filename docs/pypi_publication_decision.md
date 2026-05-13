# PyPI Publication Decision

## Current status

- PyPI published: no.
- GitHub pre-release candidate: `v0.9.0rc2`.
- Current main release draft version: `0.9.0rc3`.
- `v0.9.0rc3` tag and GitHub pre-release have not been created yet.
- Package build smoke: passed for the RC line.
- Packaging gate: `docs/packaging_gate.md`.
- Validation gate: `docs/validation_gate.md`.

## Recommendation

Use TestPyPI before any PyPI release. Do not publish from smoke scripts,
workflow automation, or local release engineering checks without explicit
maintainer approval.

## Preconditions before any PyPI publication

- Explicit maintainer approval is recorded.
- The decision record must include the phrase: explicit maintainer approval.
- `git status` is clean.
- Package version in `pyproject.toml` and `__version__` match.
- `scripts/smoke_release.sh` passes in a clean environment.
- Optional wheel install smoke passes with `OSA_SMOKE_VERIFY_WHEEL=1`.
- `pytest` passes.
- `python -m build` passes.
- `twine check dist/*` passes.
- Dist filenames match the candidate version.
- Release notes and post-release status docs are prepared.
- Token handling follows `docs/release_engineering_playbook.md`.
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
