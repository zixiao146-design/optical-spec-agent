# 可选 Solver Micro-benchmark 执行审批包

本文档用于准备未来的可选 solver-backed micro-benchmark 执行审批。它本身
不批准执行，也不批准 PyPI/TestPyPI 发布、tag 创建、GitHub release 创建或
`v1.0.0` 发布。

## 当前状态

- 当前公开候选版本：v0.9.0rc7
- 当前 main 开发版本：0.9.0rc8.dev0
- PyPI：未发布
- TestPyPI 仅上传并验证过：0.9.0rc6.dev0
- v0.9.0rc8 tag：未创建
- v1.0.0 tag：未创建
- solver micro-benchmark approval：仅授予 2026-05-20 Gmsh run 和单独批准的
  2026-05-20 Optiland run
- 已执行 solver micro-benchmark：是，Gmsh only 用于其批准 run，Optiland only
  用于其单独批准 run
- solver micro-benchmark review decision：Gmsh 只被接受为 optional manual
  mesh-generation smoke evidence；Optiland 只被接受为 optional manual ray/path
  smoke evidence
- Meep decision packet：
  `docs/optional_solver_approval_records/meep_micro_benchmark_decision_packet.md`；
  approval pending，execution authorized: no，executed: no
- 其他 solver micro-benchmark 执行：否

## 执行原则

- 一次只运行一个 solver。
- 设置任何 `OSA_RUN_OPTIONAL_*_VALIDATION=1` 之前，必须获得明确的
  solver-specific 维护者批准。
- 执行前记录 environment profile。
- 执行前记录 expected artifacts 和 report path。
- benchmark 后需要 review 并清理临时 artifact。
- 每个 solver 完成后暂停 review，再决定是否考虑下一个 solver。
- 本审批包不授权 PyPI、TestPyPI、tag、release 或 `v1.0.0`。
- 不提供 production-grade physical validation。
- 不提供 formal convergence proof。

## 推荐执行顺序

1. Gmsh first：CLI mesh generation 风险最低，只验证本地 `.geo` 到 `.msh`
   路径。状态：2026-05-20 已按 Gmsh-only 批准执行并通过，并已 review 为
   optional manual mesh-generation smoke evidence。
2. Optiland second：本地 Python/package ray-preview 路径，不涉及外部电磁
   solver。状态：2026-05-20 已按单独批准的 Optiland-only run 执行并通过，
   并已 review 为 optional manual ray/path smoke evidence。
3. Meep third：需要 solver Python profile，通常是
   `OSA_SOLVER_PYTHON=<osa-solvers python>`。状态：decision packet 已准备，
   approval pending，execution authorized: no。
4. MPB fourth：需要 solver Python profile 和 `meep.mpb`。
5. Elmer deferred：直到存在可维护的 `ElmerSolver` 安装路径。

## Per-solver 审批包

### Gmsh

- Solver：Gmsh
- Readiness profile：`homebrew-cli` 或当前 PATH 中的 `gmsh`
- 批准后需要的 env var：
  - `OSA_RUN_OPTIONAL_GMSH_VALIDATION=1`
- 审批短语：
  - `I approve running the optional Gmsh micro-benchmark for optical-spec-agent.`
- 命令模板：
  - `OSA_RUN_OPTIONAL_GMSH_VALIDATION=1 ./scripts/run_optional_solver_micro_benchmarks.sh`
- Expected artifacts：
  - `/tmp/osa-gmsh-micro-benchmark-output/gmsh_preview.geo`
  - `/tmp/osa-gmsh-micro-benchmark-output/gmsh_preview.msh`
  - `/tmp/osa-gmsh-micro-benchmark-report.json`
- Expected report path：`/tmp/osa-gmsh-micro-benchmark-report.json`
- Recorded evidence：`validation/gmsh/gmsh_micro_benchmark_2026-05-20.md`
- Review decision：`docs/optional_solver_approval_records/gmsh_micro_benchmark_review_2026-05-20.md`
- Cleanup：review 后移除 `/tmp/osa-gmsh-micro-benchmark-output/`，除非维护者要求保留。
- Risk：只验证 syntax/path smoke，不验证 optical correctness。
- Non-claims：no production-grade physical validation；no formal convergence proof。

### Optiland

- Solver：Optiland
- 状态：2026-05-20 已按单独批准的 Optiland-only run 执行并通过；maintainer
  review 接受为 optional manual ray/path smoke evidence，未来再次运行 Optiland
  需要重新批准。
- Readiness profile：`current` 或可 import `optiland` 的 Python profile
- 批准后需要的 env var：
  - `OSA_RUN_OPTIONAL_OPTILAND_VALIDATION=1`
- 审批短语：
  - `I approve running the optional Optiland micro-benchmark for optical-spec-agent.`
- 命令模板：
  - `OSA_RUN_OPTIONAL_OPTILAND_VALIDATION=1 ./scripts/run_optional_solver_micro_benchmarks.sh`
- Expected artifacts：
  - `/tmp/osa-optiland-micro-benchmark-output/optiland_preview.py`
  - `/tmp/osa-optiland-micro-benchmark-output/optiland_validation_result.json`
  - `/tmp/osa-optiland-micro-benchmark-report.json`
- Expected report path：`/tmp/osa-optiland-micro-benchmark-report.json`
- Cleanup：review 后移除 `/tmp/osa-optiland-micro-benchmark-output/` 和 report，除非要求保留。
- Risk：只验证 ray/backend path smoke，不验证 lens design。
- Non-claims：no production-grade physical validation；no formal convergence proof。

### Meep

- Solver：Meep / PyMeep
- 状态：decision packet 已准备；approval pending；execution authorized: no；
  executed: no
- Readiness profile：`osa-solvers`
- 批准后需要的 env vars：
  - `OSA_SOLVER_PYTHON=<path to solver Python>`
  - `OSA_SOLVER_READINESS_PROFILE=osa-solvers`
  - `OSA_RUN_OPTIONAL_MEEP_VALIDATION=1`
- 审批短语：
  - `I approve running the optional Meep micro-benchmark for optical-spec-agent using OSA_SOLVER_PYTHON=<path>.`
- 命令模板：
  - `OSA_SOLVER_PYTHON=<path> OSA_SOLVER_READINESS_PROFILE=osa-solvers OSA_RUN_OPTIONAL_MEEP_VALIDATION=1 ./scripts/run_optional_solver_micro_benchmarks.sh`
- Expected artifacts：
  - `/tmp/osa-meep-micro-benchmark-output/meep_preview.py`
  - `/tmp/osa-meep-micro-benchmark-output/meep_validation_result.json`
  - `/tmp/osa-meep-micro-benchmark-report.json`
- Expected report path：`/tmp/osa-meep-micro-benchmark-report.json`
- Cleanup：review 后移除 `/tmp/osa-meep-micro-benchmark-output/` 和 report，
  除非要求保留。
- Risk：tiny PyMeep path smoke only，不是 FDTD accuracy 或 convergence evidence。
- Non-claims：no production-grade physical validation；no formal convergence proof。

### MPB

- Solver：MPB through `meep.mpb`
- Readiness profile：`osa-solvers`
- 批准后需要的 env vars：
  - `OSA_SOLVER_PYTHON=<path to solver Python>`
  - `OSA_SOLVER_READINESS_PROFILE=osa-solvers`
  - `OSA_RUN_OPTIONAL_MPB_VALIDATION=1`
- 审批短语：
  - `I approve running the optional MPB micro-benchmark for optical-spec-agent using OSA_SOLVER_PYTHON=<path>.`
- 命令模板：
  - `OSA_SOLVER_PYTHON=<path> OSA_SOLVER_READINESS_PROFILE=osa-solvers OSA_RUN_OPTIONAL_MPB_VALIDATION=1 ./scripts/run_optional_solver_micro_benchmarks.sh`
- Expected artifacts：
  - `/tmp/osa-mpb-validation/mpb_preview.py`
  - `/tmp/osa-mpb-validation/mpb_validation_result.json`
  - `/tmp/osa-mpb-validation/mpb_validation_report.json`
- Expected report path：`/tmp/osa-mpb-validation/mpb_validation_report.json`
- Cleanup：review 后移除 `/tmp/osa-mpb-validation/`，除非要求保留。
- Risk：tiny band path smoke only，不是 band convergence evidence。
- Non-claims：no production-grade physical validation；no formal convergence proof。

### Elmer

- Solver：Elmer / ElmerSolver
- Readiness profile：`deferred-elmer`
- 当前授权 env vars：无
- 审批短语：
  - `I approve running the optional Elmer micro-benchmark for optical-spec-agent.`
- 命令模板：
  - Deferred；没有可维护 `ElmerSolver` 安装路径和新的明确批准前不要运行。
- Expected artifacts：
  - `/tmp/osa-elmer-validation/case.sif`
  - `/tmp/osa-elmer-validation/elmer_validation_report.json`
- Expected report path：`/tmp/osa-elmer-validation/elmer_validation_report.json`
- Cleanup：等安装路径存在后再定义。
- Risk：Elmer 仍是 Level 2 + Level-3-ready，安装 deferred。
- Non-claims：no Elmer Level 3 claim；no production-grade physical validation；
  no formal convergence proof。

## 明确未批准

- PyPI publication
- TestPyPI upload
- tag 或 GitHub release 创建
- `v1.0.0` release
- not approved: production-grade physical validation claim
- not approved: formal convergence proof claim
