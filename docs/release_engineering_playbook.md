# Release Engineering Playbook

This playbook captures the release process hardened during the `v0.9.0rc1`,
`v0.9.0rc2`, `v0.9.0rc3`, `v0.9.0rc4`, and `v0.9.0rc5` release candidates.

Current public prerelease: `v0.9.0rc5`.
Current main development version: `0.9.0rc6.dev0`.
`0.9.0rc6.dev0` is not a public release, and the `v0.9.0rc6` tag has not
been created. PyPI remains unpublished; TestPyPI contains the `0.9.0rc6.dev0`
development package.

Release engineering is open-source-solver-first. Default tests, smoke, examples,
and release validation require no proprietary solver license. External solvers
are not run by default, external LLM access is not required by default, and
commercial/proprietary solver validation must be explicit, manual, and
non-default.

Operations references:

- CI/local gate parity: `docs/ci_quality_gate_parity.md`
- Release dry-run operations: `docs/release_dry_run_operations.md`
- Secrets and token hygiene: `docs/secrets_and_token_hygiene.md`
- Maintainer operations checklist: `docs/maintainer_operations_checklist.md`

## Release phases

1. Readiness preparation: update release notes, readiness docs, and known limitations.
2. Version bump: update `pyproject.toml` and `src/optical_spec_agent/__init__.py`.
3. Smoke validation: run a clean install/test/build/CLI smoke cycle.
4. Tag creation: create an annotated RC tag only after remote tag absence is verified.
5. GitHub pre-release creation: publish a pre-release from the checked-in draft notes.
6. Post-release verification: verify tag, release URL, draft status, pre-release flag, and notes.
7. Post-release status documentation: record the verified state in `docs/post_release_status_<version>.md`.
8. Next-candidate planning: document any post-release fixes in a new RC plan.

## Clean smoke command

```bash
OSA_SMOKE_VENV=/tmp/osa-smoke-<version> ./scripts/smoke_release.sh
```

The smoke script creates a fresh virtual environment, installs the project with
the `test` extra, runs `pytest`, builds the package, validates dist filenames,
and checks `optical-spec --help` when the console script is declared.

Optional wheel install smoke:

```bash
OSA_SMOKE_VERIFY_WHEEL=1 OSA_SMOKE_WHEEL_VENV=/tmp/osa-smoke-wheel ./scripts/smoke_release.sh
```

This installs the generated wheel into a second clean virtual environment and
checks import/version metadata plus `optical-spec --help`. It does not upload
anything.

Wheel smoke remains local only. The smoke script must not publish, upload to
TestPyPI/PyPI, create tags, or create GitHub releases.
It must not require Zemax, Lumerical, COMSOL, proprietary Ansys tools, or any
other proprietary commercial solver.

## TestPyPI no-upload preflight

Before asking for approval to upload to TestPyPI, run:

```bash
OSA_TESTPYPI_PREFLIGHT_VENV=/tmp/osa-testpypi-preflight \
OSA_TESTPYPI_WHEEL_VENV=/tmp/osa-testpypi-preflight-wheel \
./scripts/testpypi_preflight.sh
```

The preflight performs a local build, `python -m twine check dist/*`, dist
filename checks, clean wheel installation, version import checks, and
`optical-spec --help`. It prints `NO UPLOAD PERFORMED`. It must not upload,
publish, create tags, create GitHub releases, print tokens, or commit tokens.

Makefile convenience targets are available for local operations:

```bash
make quality
make testpypi-preflight
```

## Required verification

- `git status` is clean before tagging.
- The package version matches `pyproject.toml`.
- `src/optical_spec_agent/__init__.py` matches the package version.
- `python -m pip install -e ".[test]"` passes in a clean environment.
- `pytest` passes.
- `python -m build` passes.
- Dist filenames match the package version.
- Optional wheel install smoke passes before any packaging publication decision.
- `optical-spec --help` passes.
- Release notes source exists.
- Post-release status doc is created after the GitHub release is verified.

## Tag and release policy

- Use annotated tags for RC releases.
- Never move existing tags.
- Never re-tag `v0.9.0rc1`, `v0.9.0rc2`, `v0.9.0rc3`, `v0.9.0rc4`, or
  `v0.9.0rc5`.
- Create a new RC tag for post-release fixes.
- GitHub pre-releases must have `draft=false` and `prerelease=true`.
- Release notes should match `docs/github_release_draft_<version>.md`.

## Token and credential safety

- Never paste tokens into chat, logs, docs, or commits.
- Use `read -s GH_TOKEN` for temporary local authentication when needed.
- Unset `GH_TOKEN` and `GITHUB_TOKEN` after use.
- Revoke exposed tokens immediately.
- Use least-privilege fine-grained tokens.
- Grant Contents read/write only when tag/release creation is required.

## Network failure handling

- `Empty reply from server` and TLS timeouts can happen during GitHub HTTPS operations.
- Do not reset or delete local work after a network failure.
- Keep local commits and retry push later.
- The GitHub API path can be used when git HTTPS is unstable.
- Stop before unsafe tag creation if remote tag existence cannot be verified.

## PyPI policy

- PyPI remains unpublished unless explicitly approved.
- Prefer TestPyPI first if packaging publication is later approved.
- Never publish during release engineering smoke without explicit approval.
- Follow `docs/packaging_gate.md` and `docs/pypi_publication_decision.md` before
  any TestPyPI or PyPI operation.
- TestPyPI dry-run gate doc: `docs/testpypi_dry_run_gate.md`.
- TestPyPI no-upload preflight script: `scripts/testpypi_preflight.sh`.
- v1.0 stability gate doc: `docs/v1_0_stability_gate.md`.
- TestPyPI/PyPI upload requires explicit approval.
- Do not publish automatically from release scripts.
