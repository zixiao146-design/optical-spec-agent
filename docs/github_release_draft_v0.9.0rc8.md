# optical-spec-agent v0.9.0rc8

## English Summary

v0.9.0rc8 is the eighth release candidate for v0.9.0. It packages rc8
backend readiness work after v0.9.0rc7, including application domain benchmark
coverage, material provenance diagnostics, validation maturity boundaries,
optional solver evidence summaries, and optional solver-backed micro-benchmark
evidence for Gmsh, Optiland, Meep, and MPB.

PyPI publication remains unapproved and unpublished. v1.0.0 remains unreleased.
This candidate preserves conservative validation boundaries and does not claim
production-grade physical validation, production-grade solver validation,
optical correctness, or a formal convergence proof.

## 中文简介

v0.9.0rc8 是 v0.9.0 的第八个候选版本。它纳入 v0.9.0rc7 之后的 rc8 后端
readiness 工作，包括应用域 benchmark 覆盖、材料来源诊断、验证成熟度边界、
可选 solver evidence 汇总，以及 Gmsh、Optiland、Meep、MPB 的可选
solver-backed micro-benchmark 证据。

PyPI 仍未发布，仍需单独批准。v1.0.0 仍未发布。本候选版本继续保持保守验证边界，
不声称生产级物理验证、生产级 solver 验证、光学正确性或形式化收敛证明。

## Highlights

- Application domain benchmarks: 19 pass / 0 warn / 0 fail.
- Material provenance and suitability diagnostics strengthened.
- Ambiguous requirement and missing-input diagnostics strengthened.
- Fiber coupling and polarization preview calculators added with reference
  sanity evidence.
- Backend validation maturity matrix added.
- Preview boundary policy added.
- Validation claim audit added.
- Optional solver micro-benchmark plan, approval matrix, environment profiles,
  and execution approval packets added.
- Optional solver evidence closed for:
  - Gmsh: executed, passed, reviewed, accepted.
  - Optiland: executed, passed, reviewed, accepted.
  - Meep: executed, passed, reviewed, accepted.
  - MPB: executed, passed, reviewed, accepted.
- Elmer remains deferred and not Level 3.
- Backend evidence pack, backend capability report, and validation maturity
  records updated.
- Agent Studio frontend, Chinese localization, quickstart, and local demo
  package remain available.

## Adapter Maturity

- Gmsh: Level 3 plus optional manual micro-benchmark evidence.
- Meep: Level 3 plus optional manual micro-benchmark evidence.
- MPB: Level 3 plus optional manual micro-benchmark evidence.
- Optiland: Level 3 plus optional manual micro-benchmark evidence.
- Elmer: Level 2 plus Level-3-ready, install deferred.

## Verification

- validation claim audit: passed.
- application domain benchmarks: 19 pass / 0 warn / 0 fail.
- sub-agent audit: passed.
- optional solver wrapper default no-execute: passed.
- backend evidence pack smoke: passed.
- backend capability smoke: passed.
- backend report smoke: passed.
- API fixture check: passed.
- API smoke: passed.
- TestPyPI no-upload preflight: passed.
- quality gates: passed.
- normal smoke: passed.
- wheel smoke: passed.
- pytest: passed.
- python -m build: passed.
- make check: passed.
- CLI examples: passed.
- dist files:
  - optical_spec_agent-0.9.0rc8-py3-none-any.whl
  - optical_spec_agent-0.9.0rc8.tar.gz

## Scope Limitations

- No PyPI publish.
- No TestPyPI upload for 0.9.0rc8.
- No production-grade physical validation.
- No production-grade solver validation.
- No production-grade FDTD validation.
- No production-grade MPB validation.
- No production band-structure validation.
- No formal convergence proof.
- No optical correctness claim.
- External solvers are not run by default.
- External LLMs are not required by default.
- Proprietary solvers are not required by default.
- Elmer Level 3 validation is deferred.
- Calculator results are sanity-checked preview/design-assist.
- Optional solver micro-benchmarks are smoke evidence, not production
  validation.
- Adapter-native golden cases are preview metadata checks, not real solver
  monitor results.
- This release candidate is not final 1.0 stability.

## Important Note

- v0.9.0rc1, v0.9.0rc2, v0.9.0rc3, v0.9.0rc4, v0.9.0rc5, v0.9.0rc6, and
  v0.9.0rc7 tags are unchanged.
- v0.9.0rc8 tag should be created only after maintainer approval.
- This task does not create a tag, create a GitHub release, or upload packages.
- PyPI publication remains separately gated.
