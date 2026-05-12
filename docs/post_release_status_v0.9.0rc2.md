# Post-release Status: v0.9.0rc2

Release verified: yes

## Tag verified

- tag: v0.9.0rc2
- target commit: 510f275c81599e10cfcec1a5acc7d6c3fd8aee8a
- short commit: 510f275
- annotated tag: yes
- annotated tag object: 5730ced294ab4fe4bb7e361624ae771a4a9bc36e

## GitHub release

- URL: https://github.com/zixiao146-design/optical-spec-agent/releases/tag/v0.9.0rc2
- title: optical-spec-agent v0.9.0rc2
- draft: false
- prerelease: true
- release notes source: docs/github_release_draft_v0.9.0rc2.md
- release notes match local draft: yes

## Verification

- scripts/smoke_release.sh: passed
- pytest: 331 passed, 4 warnings
- build: passed
- dist files:
  - optical_spec_agent-0.9.0rc2-py3-none-any.whl
  - optical_spec_agent-0.9.0rc2.tar.gz
- CLI help: optical-spec --help passed
- PyPI published: no

## Scope limitations

- no PyPI publish
- no production-grade physical validation
- no formal convergence proof
- external solvers not run by default
- external LLM not required by default
- adapter outputs are MVP/scaffold
- workflow is local/synchronous preview
- RC is not final 1.0 stability

## Important

- v0.9.0rc1 tag remains unchanged
- v0.9.0rc2 includes the post-release dependency fix from 730f6b6
- v0.9.0rc2 includes release smoke automation from 39fb14f
- v0.9.0rc2 supersedes v0.9.0rc1 as the current release candidate
- PyPI remains unpublished
