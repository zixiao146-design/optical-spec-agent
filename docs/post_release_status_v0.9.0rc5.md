# v0.9.0rc5 Post-release Status

Release verified: yes

Tag verified:
- tag: v0.9.0rc5
- target commit: accce88c88a7e823b6e71ff3e1b51b0ac08db781
- short target commit: accce88
- annotated tag: yes
- annotated tag object: cb61ee21cb4d5a3dc23d5ec17289d813aeb98ac9

GitHub release:
- URL: https://github.com/zixiao146-design/optical-spec-agent/releases/tag/v0.9.0rc5
- title: optical-spec-agent v0.9.0rc5
- draft: false
- prerelease: true
- release notes source: docs/github_release_draft_v0.9.0rc5.md
- release notes match local draft: yes

Verification:
- scripts/testpypi_preflight.sh: passed
- TestPyPI no-upload preflight: passed
- NO UPLOAD PERFORMED: yes
- scripts/run_quality_gates.sh: passed
- scripts/smoke_release.sh: passed
- wheel install smoke: passed
- pytest: 475 passed, 4 warnings
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
  - optical_spec_agent-0.9.0rc5-py3-none-any.whl
  - optical_spec_agent-0.9.0rc5.tar.gz
- PyPI published: no
- TestPyPI uploaded: no

Adapter maturity:
- Gmsh: Level 3
- Meep: Level 3
- MPB: Level 3
- Optiland: Level 3
- Elmer: Level 2 + Level-3-ready, install deferred

Scope limitations:
- no PyPI publish
- no TestPyPI upload
- no production-grade physical validation
- no formal convergence proof
- external solvers not run by default
- external LLM not required by default
- proprietary solvers not required by default
- Elmer Level 3 validation deferred
- adapter outputs may still be MVP/scaffold unless explicitly validated
- workflow is local/synchronous preview
- RC is not final 1.0 stability

Important:
- v0.9.0rc1 tag remains unchanged
- v0.9.0rc2 tag remains unchanged
- v0.9.0rc3 tag remains unchanged
- v0.9.0rc4 tag remains unchanged
- v0.9.0rc5 supersedes v0.9.0rc4 as the current public release candidate
- PyPI/TestPyPI remain unpublished/unuploaded
- TestPyPI upload approval remains pending
- Upload command authorized: no
- PyPI publication approval: not granted
