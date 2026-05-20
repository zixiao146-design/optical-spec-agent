# rc8 Backend Readiness Review zh-CN

Current public prerelease: v0.9.0rc7.
Current main release draft: `0.9.0rc8`.

本文汇总 Gmsh、Optiland、Meep、MPB optional solver evidence loop 关闭后的
backend readiness。它是 readiness review，不是 release draft，不授权
`v0.9.0rc8` tag、GitHub release、PyPI 发布、TestPyPI 上传或 `v1.0.0`
release。

## Current Status

- PyPI: not published。
- TestPyPI: 只有 `0.9.0rc6.dev0` 已上传并验证。
- `v0.9.0rc8` tag: not created。
- `v1.0.0` tag: not created。
- Application domain benchmarks: 19 pass / 0 warn / 0 fail。
- Default gates: 不执行 external solver。

## Backend Evidence Completed

- Backend evidence pack 已覆盖 package/release status、sub-agent reality、
  tool-call reality、calculators、material provenance、ambiguous requirement
  matching、missing-input diagnostics、application-domain coverage、
  adapter-native golden coverage、validation maturity 和 preview boundaries。
- Validation claim audit 已存在，任何 release-draft work 前都应运行。
- Backend capability report 已存在，并保持保守声明。

## Optional Solver Evidence Completed

- Gmsh: executed, passed, reviewed, accepted as optional manual
  mesh-generation smoke evidence。
- Optiland: executed, passed, reviewed, accepted as optional manual ray/path
  smoke evidence。
- Meep: executed, passed, reviewed, accepted as optional manual PyMeep/FDTD
  smoke evidence。
- MPB: executed, passed, reviewed, accepted as optional manual
  MPB/band-structure smoke evidence。
- Elmer: deferred, not Level 3, not executed。

## Application Domain Benchmarks

Application domain benchmark suite 当前为 19 pass / 0 warn / 0 fail。它验证
deterministic routing、candidate-domain behavior、missing-input questions、
unsupported/deferred behavior 和 safety boundaries，但不证明 physical
correctness。

## Calculator / Reference Sanity Evidence

Thin-film、paraxial、Gaussian beam、waveguide、fiber-coupling、polarization
calculators 都有 sanity/reference cases 和 failure-mode tests。这些是
sanity-checked preview/design-assist calculators，不是 production-grade
physical validation。

## Material Provenance And Ambiguous Diagnostics

Material catalog 是 local preview/design-assist catalog，包含 provenance 字段和
user-verification 要求。Ambiguous 和 unknown natural-language goals 会产生
confidence、candidates、missing inputs 和 recommended questions，而不是 unsafe
solver actions。

## Adapter-native Golden Coverage

Adapter-native golden coverage 对 Meep、MPB、Gmsh、Elmer、Optiland adapters
进行 metadata 和 expected preview fragments 检查。它不运行 solver，也不是 real
solver monitor results。

## Preview Boundary And Validation Maturity

Validation maturity 将 calculators 映射为 `sanity_checked_preview`，
application-domain benchmarks 映射为 `benchmark_checked_preview`，
adapter/source-monitor evidence 映射为 `fixture_guarded_preview`，已 review 的
Gmsh、Optiland、Meep、MPB solver evidence 映射为 optional manual smoke
evidence。不声明 production-grade physical validation，也不声明 formal
convergence proof。

## Remaining Deferred Items

- Elmer remains deferred until maintainable `ElmerSolver` install route exists。
- PyPI publication 仍是单独 maintainer decision。
- TestPyPI upload for `0.9.0rc8` 未在此批准。
- 后续可以考虑 `v0.9.0rc8` release draft，但本文不授权。
- `v1.0.0` 仍未 release。

## Recommendation

Gmsh、Optiland、Meep、MPB optional solver evidence closure 使 backend readiness
更强。建议继续 v1.0 readiness/backend engineering，保持 Elmer deferred，并将
PyPI/TestPyPI/tag/release decisions 单独 gate。不要从这些证据声明
production-grade validation、formal convergence proof 或 optical correctness。

