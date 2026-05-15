# TestPyPI Status for 0.9.0rc6.dev0

TestPyPI upload: completed

## Package

- name: optical-spec-agent
- version: 0.9.0rc6.dev0

## Publication

- TestPyPI uploaded: yes
- PyPI published: no
- PyPI publication approval: not granted
- GitHub tag created: no
- GitHub release created: no

## Upload Method

- GitHub Actions Trusted Publishing
- workflow: .github/workflows/testpypi-trusted-publish.yml
- trigger: workflow_dispatch
- confirmation input: UPLOAD_TESTPYPI
- token used: no local token; trusted publishing/OIDC

## Artifacts Uploaded

- optical_spec_agent-0.9.0rc6.dev0-py3-none-any.whl
- optical_spec_agent-0.9.0rc6.dev0.tar.gz

## Pre-upload Verification

- GitHub CI: passed
- build: passed
- twine check: passed
- target repository: TestPyPI

## Post-upload Verification

- clean install from TestPyPI: passed
- import version check: passed
- optical_spec_agent.__version__: 0.9.0rc6.dev0
- installed package file: /private/tmp/osa-testpypi-install-0.9.0rc6.dev0/lib/python3.11/site-packages/optical_spec_agent/__init__.py
- optical-spec executable: /tmp/osa-testpypi-install-0.9.0rc6.dev0/bin/optical-spec
- optical-spec --help: passed
- optical-spec adapter-list --json: passed

## Dependency-index Note

- A naive install using TestPyPI as the primary package index failed because TestPyPI contains an unrelated FASTAPI package that can shadow the real fastapi dependency.
- The successful verification installed runtime dependencies from PyPI and installed optical-spec-agent from TestPyPI with --no-deps.
- This is a TestPyPI verification caveat, not a failure of the optical-spec-agent package.

## Scope Limitations

- no PyPI publish
- no production-grade physical validation
- no formal convergence proof
- external solvers not run by default
- external LLM not required by default
- proprietary solvers not required by default
- v0.9.0rc6.dev0 is a development/pre-release package, not final v1.0

## Important

- This TestPyPI upload does not authorize PyPI publication.
- This TestPyPI upload does not create a GitHub release.
- This TestPyPI upload does not create any tag.
- PyPI publication remains separately gated.
- Re-uploading the same version may fail because package files are already present.
