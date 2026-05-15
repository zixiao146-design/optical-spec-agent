# PyPI Publication Decision

## Current status

- PyPI published: no.
- TestPyPI uploaded: yes, for `0.9.0rc6.dev0`.
- Current public prerelease: `v0.9.0rc5`.
- Current main development version: `0.9.0rc6.dev0`.
- `v0.9.0rc6` GitHub release has not been created.
- `v0.9.0rc6` tag has not been created.
- Package build smoke: passed for the RC line.
- Packaging gate: `docs/packaging_gate.md`.
- Validation gate: `docs/validation_gate.md`.
- TestPyPI dry-run gate doc: `docs/testpypi_dry_run_gate.md`.
- TestPyPI no-upload preflight script: `scripts/testpypi_preflight.sh`.
- One-command quality gate script: `scripts/run_quality_gates.sh`.
- CI/local quality parity: `docs/ci_quality_gate_parity.md`.
- Release dry-run operations: `docs/release_dry_run_operations.md`.
- Secrets and token hygiene: `docs/secrets_and_token_hygiene.md`.
- Maintainer operations checklist: `docs/maintainer_operations_checklist.md`.
- TestPyPI upload approval record:
  `docs/testpypi_upload_approval_v0.9.0rc6.dev0.md`.
- Latest TestPyPI upload attempt:
  `docs/testpypi_upload_attempt_v0.9.0rc6.dev0.md`.
- TestPyPI status:
  `docs/testpypi_status_v0.9.0rc6.dev0.md`.
- TestPyPI Trusted Publishing doc:
  `docs/testpypi_trusted_publishing.md`.
- TestPyPI Trusted Publishing workflow:
  `.github/workflows/testpypi-trusted-publish.yml`.
- TestPyPI Trusted Publishing workflow status: passed for 0.9.0rc6.dev0.
- TestPyPI upload approval status: granted for 0.9.0rc6.dev0 only.
- TestPyPI upload authorized: yes, TestPyPI only.
- Upload command authorized: TestPyPI only.
- Latest TestPyPI upload attempt result: failed with HTTP 403 Forbidden.
- TestPyPI clean install verification: passed.
- PyPI publication approval: not granted.
- v1.0 stability gate doc: `docs/v1_0_stability_gate.md`.

## Recommendation

Use TestPyPI before any PyPI release. TestPyPI upload is completed for
`0.9.0rc6.dev0` through the manual Trusted Publishing workflow, and clean
install verification passed. The earlier local token-based attempt failed with
HTTP 403 Forbidden and remains recorded as historical evidence. PyPI
publication remains prohibited without separate explicit maintainer approval.
Do not publish to PyPI from smoke scripts, workflow automation, or local release
engineering checks.

Dependency-index caveat: the successful TestPyPI verification installed runtime
dependencies from PyPI and installed `optical-spec-agent` from TestPyPI with
`--no-deps`, because TestPyPI contains an unrelated `FASTAPI` package that can
shadow the real `fastapi` dependency when TestPyPI is the primary index.

`scripts/testpypi_preflight.sh` is a local no-upload check. It builds artifacts,
runs `python -m twine check dist/*`, installs the wheel in a clean environment,
checks `optical_spec_agent.__version__`, and runs `optical-spec --help`. It does
not upload, publish, create tags, or create GitHub releases.

## Preconditions before any PyPI publication

- Explicit maintainer approval is recorded.
- The approval record changes from pending to granted for the intended package
  version.
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
- Token handling follows `docs/release_engineering_playbook.md` and
  `docs/secrets_and_token_hygiene.md`.
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
