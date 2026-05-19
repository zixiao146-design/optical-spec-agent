# optical-spec-agent v0.9.0rc7

## English Summary

v0.9.0rc7 is the seventh release candidate for v0.9.0. It packages backend
evidence hardening and optical design agent capability expansion after
v0.9.0rc6. It adds backend evidence review decision support for rc7 draft
readiness.

This candidate adds the Material Library, optical design examples, design
requirement templates, sub-agent task sessions, tool-call ledger, local optical
calculators, source/monitor diagnostics, observable diagnostics, adapter-native
mappings, adapter golden coverage, and backend evidence review pack.

PyPI publication remains unapproved and unpublished. v1.0.0 remains unreleased.
The release draft preserves conservative validation boundaries.

## 中文简介

v0.9.0rc7 是 v0.9.0 的第七个候选版本，纳入 v0.9.0rc6 之后的后端证据加固和
光学设计 agent 能力扩展。

本候选版本已记录 backend evidence review decision，结论是可以准备 rc7 release
draft。新增材料库、光学设计示例、设计需求模板、子智能体任务会话、工具调用账本、
本地光学计算器、光源/监测诊断、observable 诊断、adapter-native 映射、adapter
golden coverage 和 backend evidence review pack。

PyPI 仍未发布，仍需单独批准。v1.0.0 仍未发布。仍不声称生产级物理验证或形式化收敛证明。

## Highlights

- Backend evidence review decision recorded as sufficient for v0.9.0rc7 release draft.
- Material Library / 材料库 added.
- Optical design examples expanded.
- Design requirement templates added.
- Natural-language to optical-language matching added.
- Agent Command Center task sessions added.
- Tool-call ledger added.
- Local optical calculators deepened with reference sanity cases.
- Source/monitor inference and missing-input diagnostics added.
- Observable diagnostics added.
- Adapter-native source/monitor mapping added.
- Adapter-native golden cases and strict metadata diff checks added.
- Backend evidence review pack added.
- Agent Studio frontend, Chinese localization, quickstart, and local demo package remain available.
- PyPI remains unpublished.

## Adapter Maturity

- Gmsh: Level 3
- Meep: Level 3
- MPB: Level 3
- Optiland: Level 3
- Elmer: Level 2 + Level-3-ready, install deferred

## Verification

- backend evidence pack smoke: passed
- backend capability smoke: passed
- adapter-native golden checker: passed
- sub-agent audit: passed
- API fixture check: passed
- API smoke: passed
- quality gates: passed
- TestPyPI no-upload preflight: passed
- normal smoke: passed
- wheel smoke: passed
- pytest: 761 passed, 4 warnings
- python -m build: passed
- make check: passed
- CLI examples: passed
- dist files:
  - `optical_spec_agent-0.9.0rc7-py3-none-any.whl`
  - `optical_spec_agent-0.9.0rc7.tar.gz`

## Scope Limitations

- No PyPI publish.
- No TestPyPI upload for 0.9.0rc7.
- No production-grade physical validation.
- No formal convergence proof.
- External solvers are not run by default.
- External LLM is not required by default.
- Proprietary solvers are not required by default.
- Elmer Level 3 validation deferred.
- Calculator results are sanity-checked preview/design-assist, not production-grade validation.
- Adapter-native golden cases are preview metadata checks, not real solver monitor results.
- RC is not final 1.0 stability.

## Important Note

- v0.9.0rc1 / v0.9.0rc2 / v0.9.0rc3 / v0.9.0rc4 / v0.9.0rc5 / v0.9.0rc6 tags are unchanged.
- v0.9.0rc7 tag should be created only after maintainer approval.
- This task does not create tag/release or upload packages.
- PyPI publication remains separately gated.
