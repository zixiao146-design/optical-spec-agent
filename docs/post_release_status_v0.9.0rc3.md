# v0.9.0rc3 Post-release Status

Release verified: yes

Tag verified:
- tag: v0.9.0rc3
- target commit: acc407d
- full target commit: acc407df1822db99bed258b6165099f3e5c2e424
- annotated tag: yes
- annotated tag object: 75eee9486be19139c06a1eb8b7a6c681dcef542f

GitHub release:
- URL: https://github.com/zixiao146-design/optical-spec-agent/releases/tag/v0.9.0rc3
- title: optical-spec-agent v0.9.0rc3
- draft: false
- prerelease: true
- release notes source: docs/github_release_draft_v0.9.0rc3.md
- release notes match local draft: yes

Verification:
- scripts/smoke_release.sh: passed
- wheel install smoke: passed
- pytest: 357 passed, 4 warnings
- build: passed
- make check: passed
- CLI examples passed:
  - optical-spec --help
  - optical-spec adapter-list --json
  - optical-spec schema
  - optical-spec parse
  - optical-spec validate
  - optical-spec workflow-plan --json
- dist files:
  - optical_spec_agent-0.9.0rc3-py3-none-any.whl
  - optical_spec_agent-0.9.0rc3.tar.gz
- PyPI published: no
- TestPyPI uploaded: no

Scope limitations:
- no PyPI publish
- no TestPyPI upload
- no production-grade physical validation
- no formal convergence proof
- external solvers not run by default
- external LLM not required by default
- adapter outputs may still be MVP/scaffold unless explicitly validated
- workflow is local/synchronous preview
- RC is not final 1.0 stability

Important:
- v0.9.0rc1 tag remains unchanged
- v0.9.0rc2 tag remains unchanged
- v0.9.0rc3 supersedes v0.9.0rc2 as the current public release candidate
- PyPI/TestPyPI remain unpublished
