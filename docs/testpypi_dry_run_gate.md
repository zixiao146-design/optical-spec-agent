# TestPyPI Dry-run Gate

## Current status

- TestPyPI uploaded: yes, for 0.9.0rc6.dev0
- TestPyPI upload for 0.9.0rc8.dev0: not performed
- PyPI published: no
- Current public prerelease: v0.9.0rc7
- Current main development version: `0.9.0rc8.dev0`
- Product positioning: open-source-solver-first
- Proprietary solvers are not default dependencies
- v0.9.0rc8 tag: not created
- GitHub release: not created
- PyPI remains unpublished; TestPyPI contains 0.9.0rc6.dev0
- The rc6 approval record is `docs/testpypi_upload_approval_v0.9.0rc6.md` and
  remains pending.
- The rc7 approval record is
  `docs/testpypi_upload_approval_v0.9.0rc7.md` and remains pending.
- The rc8 development approval record is
  `docs/testpypi_upload_approval_v0.9.0rc8.dev0.md` and remains pending.
- TestPyPI upload approval record:
  `docs/testpypi_upload_approval_v0.9.0rc6.dev0.md`
- Latest TestPyPI upload attempt:
  `docs/testpypi_upload_attempt_v0.9.0rc6.dev0.md`
- TestPyPI status:
  `docs/testpypi_status_v0.9.0rc6.dev0.md`
- TestPyPI Trusted Publishing doc:
  `docs/testpypi_trusted_publishing.md`
- TestPyPI Trusted Publishing workflow:
  `.github/workflows/testpypi-trusted-publish.yml`
- TestPyPI Trusted Publishing workflow status: passed for 0.9.0rc6.dev0
- TestPyPI upload approval status for 0.9.0rc8.dev0: pending
- TestPyPI upload authorized for rc8.dev0: no
- Upload command authorized for 0.9.0rc8.dev0: no
- Latest TestPyPI upload attempt result: failed with HTTP 403 Forbidden
- TestPyPI clean install verification: passed
- PyPI publication approval: not granted

## Purpose

This document defines what must be checked before TestPyPI upload. The
maintainer has authorized a TestPyPI-only upload for `0.9.0rc6.dev0`; it does
not authorize PyPI publication, tag creation, or GitHub release creation.

## No-upload preflight

`scripts/testpypi_preflight.sh` performs the repeatable local preflight before
any future TestPyPI decision. It runs a local build, `python -m twine check
dist/*`, dist filename checks, clean wheel installation, package version import
checks, and `optical-spec --help`.

The preflight does not upload. It does not publish. It does not create tags. It
does not create GitHub releases. It prints `NO UPLOAD PERFORMED`.

The manual TestPyPI Trusted Publishing workflow was used successfully for
`0.9.0rc6.dev0`. It is manual only, requires the confirmation string
`UPLOAD_TESTPYPI`, and targets `https://test.pypi.org/legacy/`. Re-uploading the
same version may fail because package files are already present.

`scripts/run_quality_gates.sh` includes this preflight as the first local gate
unless `OSA_SKIP_PREFLIGHT=1` is set.

Related operations docs:

- `docs/ci_quality_gate_parity.md`
- `docs/release_dry_run_operations.md`
- `docs/secrets_and_token_hygiene.md`
- `docs/maintainer_operations_checklist.md`

## Required dry-run checks

- `python -m build` passes.
- `scripts/testpypi_preflight.sh` passes.
- Wheel/sdist filenames match `project.version`.
- `python -m twine check dist/*` passes.
- Wheel install smoke passes.
- `pip install -e ".[test]"` passes.
- `pytest` passes.
- `make check` passes.
- `optical-spec --help` passes.
- Documented CLI examples pass offline.
- Metadata is reviewed.
- README/readme field is correct.
- License metadata is acceptable.
- Dependencies are reasonable.
- Package imports cleanly after wheel install.
- No proprietary license is required.
- External solvers are not run by default.
- External LLM access is not required by default.

## Manual approval requirement

- TestPyPI upload requires explicit maintainer approval.
- PyPI upload requires explicit maintainer approval.
- The approval record granted TestPyPI upload for `0.9.0rc6.dev0` only, and the
  status record now documents the completed Trusted Publishing upload.
- Approval must be recorded in docs or release notes.
- Default smoke/release scripts must never upload automatically.
- No token should be printed or committed.

## Upload non-goals

- This document does not authorize another upload of `0.9.0rc6.dev0`.
- This task does not publish PyPI.
- This task does not create release artifacts beyond local dist.
- This task does not create GitHub release.
- This task does not create tags.

## Future command placeholders

HISTORICAL LOCAL TOKEN TEMPLATE FOR 0.9.0rc6.dev0 ONLY. DO NOT RERUN AFTER THE
SUCCESSFUL TRUSTED PUBLISHING UPLOAD:

```bash
python -m twine upload \
  --repository testpypi \
  -u __token__ \
  -p "$TESTPYPI_TOKEN" \
  dist/optical_spec_agent-0.9.0rc6.dev0-py3-none-any.whl \
  dist/optical_spec_agent-0.9.0rc6.dev0.tar.gz
```

- Do not run this command for PyPI.
- Token must never be committed or printed.
