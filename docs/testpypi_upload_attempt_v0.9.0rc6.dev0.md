# TestPyPI Upload Attempt for 0.9.0rc6.dev0

TestPyPI upload: attempted, not completed

Package:
- name: optical-spec-agent
- version: 0.9.0rc6.dev0

Publication:
- TestPyPI upload approval: granted for 0.9.0rc6.dev0 only
- Upload command authorized: TestPyPI only
- TestPyPI uploaded: no
- PyPI published: no
- PyPI publication approval: not granted
- GitHub tag created: no
- GitHub release created: no

Artifacts attempted:
- optical_spec_agent-0.9.0rc6.dev0-py3-none-any.whl
- optical_spec_agent-0.9.0rc6.dev0.tar.gz

Pre-upload verification:
- quality gates: passed
- TestPyPI no-upload preflight: passed
- twine check: passed
- build: passed

Upload result:
- command target: TestPyPI only
- result: failed
- failure class: HTTP 403 Forbidden from https://test.pypi.org/legacy/
- likely cause: TestPyPI token permission, project ownership, or a TestPyPI
  token that is not allowed to create/upload this package
- token cleanup: yes
- token printed, saved, or committed: no

Post-upload verification:
- clean install from TestPyPI: not run because upload failed
- import version check from TestPyPI install: not run because upload failed
- optical-spec --help from TestPyPI install: not run because upload failed

Scope limitations:
- no PyPI publish
- no production-grade physical validation
- no formal convergence proof
- external solvers not run by default
- external LLM not required by default
- proprietary solvers not required by default
- v0.9.0rc6.dev0 is a development/pre-release package, not final v1.0

Important:
- This failed TestPyPI upload attempt does not authorize PyPI publication.
- This failed TestPyPI upload attempt does not create a GitHub release.
- This failed TestPyPI upload attempt does not create any tag.
- PyPI publication remains separately gated.
- A future retry should use a TestPyPI API token with permission to create or
  upload the `optical-spec-agent` project on TestPyPI.
