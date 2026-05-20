# 可选 Solver 执行顺序

可选 solver-backed micro-benchmark 只能在明确 solver-specific 批准后，一次
执行一个 solver。本文档只是 planning aid，不是执行批准。

## 推荐顺序

1. Gmsh first。
   - 风险最低，因为它只检查本地 `.geo` preview 到 `.msh` 的 CLI mesh
     generation 路径。
   - Gmsh 后暂停并 review report，再考虑下一个 solver。
   - 状态：2026-05-20 已按 Gmsh-only 批准执行并通过；见
     `validation/gmsh/gmsh_micro_benchmark_2026-05-20.md`。
2. Optiland second。
   - 检查本地 Python/package ray-preview 路径。
   - Optiland 后暂停并 review artifact path。
3. Meep third。
   - 需要 `OSA_SOLVER_PYTHON` 指向 `osa-solvers` 等 solver Python profile。
   - Meep 后暂停并 review PyMeep report，再考虑 MPB。
4. MPB fourth。
   - 需要 `OSA_SOLVER_PYTHON` 和 `meep.mpb`。
   - MPB 后暂停并 review band-path smoke report。
5. Elmer deferred。
   - 没有可维护的 `ElmerSolver` 安装路径前不要运行。
   - Elmer 仍是 Level 2 + Level-3-ready，不是 Level 3。

## Stop Conditions

- 选定 profile 中 solver 不可用。
- 审批短语没有明确命名 exact solver。
- 命令会设置多个 `OSA_RUN_OPTIONAL_*_VALIDATION=1`。
- 预期输出目录已有需要保留的 artifact。
- result report 缺少必需 safety fields。
- 任何步骤暗示 PyPI/TestPyPI upload、tag 创建、GitHub release 创建或
  `v1.0.0` release。

## 每个 Benchmark 后的 Review

- 阅读 solver-specific report JSON。
- 确认 `production_grade_validation_claimed=false`。
- 确认 `formal_convergence_proof_claimed=false`。
- 确认 benchmark 只使用被批准的 solver 和 environment。
- 决定保留或删除临时 artifacts。
- 在考虑下一个 solver 前，记录 manual validation follow-up。

不要在没有 separate approval 的情况下批量运行所有 solvers。
