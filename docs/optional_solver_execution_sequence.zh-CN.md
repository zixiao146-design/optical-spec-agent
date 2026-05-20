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
   - Review 状态：已接受为 optional manual mesh-generation smoke evidence；
     见 `docs/optional_solver_approval_records/gmsh_micro_benchmark_review_2026-05-20.md`。
2. Optiland second。
   - 检查本地 Python/package ray-preview 路径。
   - Optiland 后暂停并 review artifact path。
   - 状态：2026-05-20 已按 Optiland-only 批准执行并通过；见
     `validation/optiland/optiland_micro_benchmark_2026-05-20.md`。
   - Review 状态：接受为 optional manual ray/path smoke evidence；见
     `docs/optional_solver_approval_records/optiland_micro_benchmark_review_2026-05-20.md`。
   - 范围：仅作为 optional manual ray/path smoke evidence，不是透镜设计验证。
3. Meep third。
   - 需要 `OSA_SOLVER_PYTHON` 指向 `osa-solvers` 等 solver Python profile。
   - 状态：2026-05-20 已按 Meep-only 批准执行并通过；见
     `validation/meep/meep_micro_benchmark_2026-05-20.md`。
   - Review 状态：接受为 optional manual PyMeep/FDTD smoke evidence；见
     `docs/optional_solver_approval_records/meep_micro_benchmark_review_2026-05-20.md`。
   - Meep 后暂停并 review PyMeep report，再考虑 MPB。
4. MPB fourth。
   - 需要 `OSA_SOLVER_PYTHON` 和 `meep.mpb`。
   - Decision packet:
     `docs/optional_solver_approval_records/mpb_micro_benchmark_decision_packet.md`。
   - 如果 `meep.mpb` Python import path 可用，则不要求 MPB CLI。
   - 状态：2026-05-20 已按 MPB-only 批准执行并通过；见
     `validation/mpb/mpb_micro_benchmark_2026-05-20.md`。
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
已接受的 Gmsh review 本身不授权 Optiland；Optiland 只是在单独 approval
record 后执行。已接受的 Optiland review 本身不授权 Meep；Meep 只是在单独
approval record 后执行。已接受的 Meep 证据不授权 MPB；MPB 只是在单独
approval record 后执行。MPB 证据目前只记录为 optional manual MPB/band-structure
smoke evidence，已 review 并接受；它不授权 Elmer、未来 Gmsh/Optiland/Meep/MPB
rerun、PyPI/TestPyPI upload、tag 创建或 release 创建。

Gmsh、Optiland、Meep、MPB 的 optional solver evidence loop 现在已经关闭。
未来任何 rc8/PyPI/v1.0 决策前，应查看 `docs/optional_solver_evidence_summary.zh-CN.md`
和 `docs/rc8_backend_readiness_review.zh-CN.md`。Elmer 仍 deferred 且不是 Level 3。
