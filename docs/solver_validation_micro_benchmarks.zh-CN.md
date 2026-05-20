# 可选 Solver-backed Validation Micro-benchmarks

## 目的

这些 micro-benchmarks 定义一条可选、手动、显式 opt-in 的验证路径，用于在维护者明确要求时，检查本地 adapter preview artifact 到小型开源 solver 运行之间的最小链路。

它们不是默认 release gate，不是默认 quality gate，也不是默认 pytest 行为。它们不声称生产级物理验证（production-grade physical validation）、形式化收敛证明或真实光学设计正确性。

## 当前默认行为

- 默认 pytest 不运行外部 solver。
- 默认（default）pytest does not run solvers by default。
- 默认 smoke 脚本不运行外部 solver。
- 默认 quality gates 不运行外部 solver。
- 默认 release gates 不运行外部 solver。
- 默认检查中 solver 缺失是 non-blocking。
- Elmer 仍保持 deferred，直到存在可维护的安装路径。

## 候选 micro-benchmarks

| Solver | 候选 benchmark | 预期产物 | 边界 |
| --- | --- | --- | --- |
| Gmsh | 从本地 `.geo` preview 生成微型 mesh | `.msh` | 2026-05-20 已按 Gmsh-only 批准执行并通过；只验证语法和路径，不验证光学正确性。 |
| Meep | 基于生成的 preview artifact 执行微型 PyMeep smoke | result JSON | 只验证 import/run 路径，不是生产级 FDTD。 |
| MPB | 通过 `meep.mpb` 执行微型 band-structure smoke | band summary JSON | 只验证 MPB Python 路径。 |
| Optiland | 微型 ray-trace 或 import/run smoke | result JSON | 2026-05-20 已按 Optiland-only 批准执行并通过；只验证本地 Optiland 路径，不验证透镜设计正确性。 |
| Elmer | 等待可维护的 `ElmerSolver` 安装路径 | deferred report | 不声称 Level 3 验证。 |

2026-05-20 的 Gmsh 结果已被 review 并接受为 optional manual
mesh-generation smoke evidence。它不授权任何进一步 solver 执行，也不改变默认
test、quality gate 或 release gate 行为。另一个单独批准的 2026-05-20
Optiland-only run 已通过，并只记录为 optional manual ray/path smoke
evidence。Meep/MPB 需要 `OSA_SOLVER_PYTHON` 和单独批准；Elmer 仍
deferred。当前记录不批准未来 Gmsh 或 Optiland rerun。

## 必需批准

Solver-backed run 必须显式设置 opt-in 环境变量。默认 CI、默认 smoke、release gates 或 quality gates 不应设置这些变量：

- `OSA_RUN_OPTIONAL_GMSH_VALIDATION=1`
- `OSA_RUN_OPTIONAL_MEEP_VALIDATION=1`
- `OSA_RUN_OPTIONAL_MPB_VALIDATION=1`
- `OSA_RUN_OPTIONAL_OPTILAND_VALIDATION=1`

Elmer 仍保持 deferred。现有 pilot 脚本文档中保留 `OSA_RUN_OPTIONAL_ELMER_VALIDATION=1`，但本 micro-benchmark plan 不把 Elmer 提升为 Level 3。

统一 wrapper：

```bash
./scripts/run_optional_solver_micro_benchmarks.sh
```

默认情况下它只打印 manifest summary；如果设置了 `OSA_SOLVER_MICRO_BENCHMARK_REPORT`，会写出 JSON report；默认不执行任何 solver。

任何 opt-in run 之前，都应先审查
[`optional_solver_micro_benchmark_approval_matrix.zh-CN.md`](optional_solver_micro_benchmark_approval_matrix.zh-CN.md)
readiness matrix，并为被选中的 solver 填写
[`optional_solver_micro_benchmark_approval_record_template.zh-CN.md`](optional_solver_micro_benchmark_approval_record_template.zh-CN.md)。
只做可用性检测、且不执行 solver 的命令是：

```bash
python scripts/check_optional_solver_readiness.py
```

该脚本只做 availability detection，不运行 solver binary，也不执行 solver example。
Readiness 与环境相关：默认使用当前 Python 和当前 `PATH`；如果维护者希望探测
专用 solver Python，可以设置 `OSA_SOLVER_PYTHON`，例如本地 `osa-solvers`
conda 环境：

```bash
OSA_SOLVER_PYTHON=/opt/homebrew/Caskroom/miniforge/base/envs/osa-solvers/bin/python \
OSA_SOLVER_READINESS_PROFILE=osa-solvers \
python scripts/check_optional_solver_readiness.py
```

这样可以区分项目基础环境和专用 PyMeep / `meep.mpb` 环境，但仍不会执行 solver。
环境 profile 见
[`optional_solver_environment_profiles.zh-CN.md`](optional_solver_environment_profiles.zh-CN.md)。
执行审批准备见
[`optional_solver_micro_benchmark_execution_packet.zh-CN.md`](optional_solver_micro_benchmark_execution_packet.zh-CN.md)，
一次只运行一个 solver 的顺序见
[`optional_solver_execution_sequence.zh-CN.md`](optional_solver_execution_sequence.zh-CN.md)，
per-solver pending/deferred approval records，以及 2026-05-20 Gmsh-only 和
Optiland-only approved execution records，位于
[`optional_solver_approval_records/`](optional_solver_approval_records/)。

## 声明边界

这些 micro-benchmarks 在显式运行并记录后，可以作为小型项目路径的可选手动验证证据。它们不意味着：

- no production-grade physical validation（不声称生产级物理验证）
- 形式化收敛证明
- 应用域 benchmark 的真实 solver monitor result
- 默认外部 solver 依赖
- 默认外部 LLM 使用
- PyPI/TestPyPI 发布就绪
