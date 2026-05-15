# TestPyPI Trusted Publishing

## Purpose

This document records the GitHub Actions Trusted Publishing route for a future
manual TestPyPI upload of `optical-spec-agent` `0.9.0rc6.dev0`.

The local token-based TestPyPI upload attempt for `0.9.0rc6.dev0` failed with
HTTP 403 Forbidden. The next safer route is to use TestPyPI Trusted Publishing
bound to GitHub Actions, so no TestPyPI token needs to be stored in the
repository or pasted into a workflow secret.

## Workflow

- Workflow path: `.github/workflows/testpypi-trusted-publish.yml`
- Trigger: manual `workflow_dispatch` only
- Required confirmation string: `UPLOAD_TESTPYPI`
- Target repository URL: `https://test.pypi.org/legacy/`
- Package version guarded by workflow: `0.9.0rc6.dev0`
- Token storage: no token stored
- PyPI publication approved: no
- GitHub tag created: no
- GitHub release created: no

This task adds the workflow only. It does not run the workflow, upload to
TestPyPI, publish to PyPI, create a tag, or create a GitHub release.

## Required TestPyPI Trusted Publisher Settings

The TestPyPI trusted publisher configuration should match:

- owner: `zixiao146-design`
- repository: `optical-spec-agent`
- workflow filename: `testpypi-trusted-publish.yml`
- environment: `testpypi` if configured

## Safety Boundaries

- The workflow has no `push` trigger.
- The workflow has no `pull_request` trigger.
- The workflow is not part of automatic CI.
- The workflow requires `workflow_dispatch` and the confirmation input
  `UPLOAD_TESTPYPI`.
- The workflow uses `id-token: write` for Trusted Publishing.
- The workflow does not use a TestPyPI token, PyPI token, password, or stored
  secret.
- The workflow uploads only to TestPyPI, not PyPI.
- The workflow does not create tags.
- The workflow does not create GitHub releases.
- PyPI publication remains separately gated and not approved.
