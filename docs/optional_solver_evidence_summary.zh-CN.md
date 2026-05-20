# Optional Solver Evidence Summary zh-CN

Current public prerelease: v0.9.0rc7.
Current main release draft: `0.9.0rc8`.

PyPI 未发布。TestPyPI 只有 `0.9.0rc6.dev0` 已上传并验证。`v0.9.0rc8`
tag 未创建，`v1.0.0` tag 未创建。

本文汇总已经执行、记录并 review 的 optional solver micro-benchmark 证据。
它不授权 solver rerun、TestPyPI/PyPI 上传、tag、release 或发布动作。

## Evidence Summary Table

| Solver | Readiness status | Approval status | Execution status | Review status | Evidence record | Review record | Accepted evidence type | Default gate behavior | Production-grade claim | Formal convergence claim | Optical correctness claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Gmsh | CLI/PATH profile candidate ready | 仅批准已记录的 2026-05-20 run | executed / passed | reviewed / accepted | `validation/gmsh/gmsh_micro_benchmark_2026-05-20.md` | `docs/optional_solver_approval_records/gmsh_micro_benchmark_review_2026-05-20.md` | optional manual mesh-generation smoke evidence | 默认不执行 solver | no | no | no |
| Optiland | local Python/package profile candidate ready | 仅批准已记录的 2026-05-20 run | executed / passed | reviewed / accepted | `validation/optiland/optiland_micro_benchmark_2026-05-20.md` | `docs/optional_solver_approval_records/optiland_micro_benchmark_review_2026-05-20.md` | optional manual ray/path smoke evidence | 默认不执行 solver | no | no | no |
| Meep | `OSA_SOLVER_PYTHON` profile candidate ready | 仅批准已记录的 2026-05-20 run | executed / passed | reviewed / accepted | `validation/meep/meep_micro_benchmark_2026-05-20.md` | `docs/optional_solver_approval_records/meep_micro_benchmark_review_2026-05-20.md` | optional manual PyMeep/FDTD smoke evidence | 默认不执行 solver | no | no | no |
| MPB | `OSA_SOLVER_PYTHON` + `meep.mpb` candidate ready | 仅批准已记录的 2026-05-20 run | executed / passed | reviewed / accepted | `validation/mpb/mpb_micro_benchmark_2026-05-20.md` | `docs/optional_solver_approval_records/mpb_micro_benchmark_review_2026-05-20.md` | optional manual MPB/band-structure smoke evidence | 默认不执行 solver | no | no | no |
| Elmer | deferred until maintainable install route exists | deferred | not executed | deferred | `validation/elmer/elmer_install_deferred_2026-05-15.md` | `docs/optional_solver_approval_records/elmer_micro_benchmark_deferred.md` | none; not Level 3 | 默认不执行 solver | no | no | no |

## What This Evidence Proves

- 在每个 solver 单独批准时，optional opt-in wrapper 可以执行已记录的
  Gmsh、Optiland、Meep、MPB smoke path。
- wrapper 和记录保持 no-upload、no-tag、no-release 边界。
- 默认 pytest、smoke、release、quality gates 不执行 solver。
- Gmsh、Optiland、Meep、MPB 都有 evidence record 和 maintainer review
  decision。

## What This Evidence Does Not Prove

- 不声明 production-grade physical validation。
- 不声明 production-grade solver validation。
- 不声明 production-grade FDTD validation。
- 不声明 production-grade MPB validation。
- 不声明 production band-structure validation。
- 不声明 formal convergence proof。
- 不声明 optical correctness。
- 不声明 Elmer Level 3 validation。
- 不代表 PyPI readiness decision。

## Recommended Next Step

把这些证据作为 rc8 backend readiness review 的输入。Elmer 继续 deferred。
PyPI、TestPyPI、tag/release 和 `v1.0.0` 决策继续单独 gate。

