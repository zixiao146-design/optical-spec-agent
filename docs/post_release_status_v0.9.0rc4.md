# v0.9.0rc4 Post-release Status

Release verified: yes

Tag verified:
- tag: v0.9.0rc4
- target commit: 497acc3
- full target commit: 497acc37a021db1af24629a77abab16f1d0f62f8
- annotated tag: yes
- annotated tag object: e37fadef125ac08786afcf7baa9a93593df959c2

GitHub release:
- URL: https://github.com/zixiao146-design/optical-spec-agent/releases/tag/v0.9.0rc4
- title: optical-spec-agent v0.9.0rc4
- draft: false
- prerelease: true
- release notes source: docs/github_release_draft_v0.9.0rc4.md
- release notes match local draft: yes

Verification:
- scripts/testpypi_preflight.sh: passed
- TestPyPI no-upload preflight: passed
- NO UPLOAD PERFORMED: yes
- scripts/smoke_release.sh: passed
- wheel install smoke: passed
- pytest: 429 passed, 4 warnings
- build: passed
- make check: passed
- CLI examples passed:
  - optical-spec --help
  - optical-spec adapter-list --json
  - optical-spec validate examples/specs/minimal_nanoparticle.json
  - optical-spec parse examples/specs/minimal_nanoparticle.json --json
  - optical-spec workflow-plan examples/workflows/local_preview_request.json --json
  - optical-spec workflow-plan examples/e2e/local_optical_workflow.json --json
- dist files:
  - optical_spec_agent-0.9.0rc4-py3-none-any.whl
  - optical_spec_agent-0.9.0rc4.tar.gz
- PyPI published: no
- TestPyPI uploaded: no

Scope limitations:
- no PyPI publish
- no TestPyPI upload
- no production-grade physical validation
- no formal convergence proof
- external solvers not run by default
- external LLM not required by default
- proprietary solvers not required by default
- adapter outputs may still be MVP/scaffold unless explicitly validated
- workflow is local/synchronous preview
- RC is not final 1.0 stability

Important:
- v0.9.0rc1 tag remains unchanged
- v0.9.0rc2 tag remains unchanged
- v0.9.0rc3 tag remains unchanged
- v0.9.0rc4 supersedes v0.9.0rc3 as the current public release candidate
- PyPI/TestPyPI remain unpublished/unuploaded
- TestPyPI upload approval remains pending
- Upload command authorized: no
- PyPI publication approval: not granted
