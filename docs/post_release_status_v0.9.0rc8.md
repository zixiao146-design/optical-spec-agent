# v0.9.0rc8 Post-release Status

Release verified: yes

## Tag Verified

- tag: v0.9.0rc8
- target commit: e9b219863026665dcf59c52a4dc29205eb1e15f4
- short target commit: e9b2198
- annotated tag: yes
- annotated tag object: c35f4e6ffdd1f78f2154ac69827a14c03f9cb385

## GitHub Release

- URL: https://github.com/zixiao146-design/optical-spec-agent/releases/tag/v0.9.0rc8
- title: optical-spec-agent v0.9.0rc8
- draft: false
- prerelease: true
- release notes source: docs/github_release_draft_v0.9.0rc8.md
- release notes match local draft: yes

## Verification

- validation claim audit: passed
- application domain benchmarks: 19 pass / 0 warn / 0 fail
- sub-agent audit: passed
- optional solver wrapper default no-execute: passed
- backend capability smoke: passed
- backend report smoke: passed
- backend evidence pack smoke: passed
- scripts/testpypi_preflight.sh: passed
- TestPyPI no-upload preflight: passed
- NO UPLOAD PERFORMED: yes
- scripts/run_quality_gates.sh: passed
- scripts/smoke_release.sh: passed
- wheel install smoke: passed
- API fixture check: passed
- API smoke: passed
- pytest: 890 passed, 4 warnings
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
  - optical_spec_agent-0.9.0rc8-py3-none-any.whl
  - optical_spec_agent-0.9.0rc8.tar.gz

## Publication

- TestPyPI uploaded for 0.9.0rc6.dev0: yes
- TestPyPI uploaded for 0.9.0rc8: no
- PyPI published: no
- PyPI publication approval: not granted

## Optional Solver Evidence

- Gmsh: executed, passed, reviewed, accepted
- Optiland: executed, passed, reviewed, accepted
- Meep: executed, passed, reviewed, accepted
- MPB: executed, passed, reviewed, accepted
- Elmer: deferred, not Level 3
- Default gates execute solvers: no
- Production-grade physical validation claimed: no
- Production-grade solver validation claimed: no
- Formal convergence proof claimed: no
- Optical correctness claimed: no

## Backend Readiness

- application domain benchmarks: 19 pass / 0 warn / 0 fail
- material provenance and diagnostics: available
- ambiguous requirement matching: available
- missing-input diagnostics: available
- fiber/polarization calculators and reference cases: available
- backend validation maturity matrix: available
- preview boundary policy: available
- validation claim audit: available

## v1.0 Readiness

- v1.0 public contract freeze: approved
- v1.0.0 released: no

## Adapter Maturity

- Gmsh: Level 3 + optional manual micro-benchmark evidence
- Meep: Level 3 + optional manual micro-benchmark evidence
- MPB: Level 3 + optional manual micro-benchmark evidence
- Optiland: Level 3 + optional manual micro-benchmark evidence
- Elmer: Level 2 + Level-3-ready, install deferred

## Scope Limitations

- no PyPI publish
- no TestPyPI upload for v0.9.0rc8
- no production-grade physical validation
- no production-grade solver validation
- no production-grade FDTD validation
- no production-grade MPB validation
- no production band-structure validation
- no formal convergence proof
- no optical correctness claim
- external solvers not run by default
- external LLM not required by default
- proprietary solvers not required by default
- Elmer Level 3 validation deferred
- calculator results are sanity-checked preview/design-assist
- optional solver micro-benchmarks are smoke evidence, not production validation
- adapter-native golden cases are preview metadata checks, not real solver monitor results
- workflow is local/synchronous preview
- RC is not final 1.0 stability

## Important

- v0.9.0rc1 tag remains unchanged
- v0.9.0rc2 tag remains unchanged
- v0.9.0rc3 tag remains unchanged
- v0.9.0rc4 tag remains unchanged
- v0.9.0rc5 tag remains unchanged
- v0.9.0rc6 tag remains unchanged
- v0.9.0rc7 tag remains unchanged
- v0.9.0rc8 supersedes v0.9.0rc7 as the current public release candidate
- PyPI remains unpublished
- PyPI publication approval remains not granted
- v1.0.0 remains unreleased
