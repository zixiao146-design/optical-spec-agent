# Optional Solver Micro-benchmark Approval Matrix

本矩阵用于维护者在运行可选 solver-backed micro-benchmark 之前做审查。它本身不授权
执行 solver。默认 pytest、smoke、quality gates、release gates 和 package build
都不会运行外部 solver。

缺失 solver 不阻塞默认检查。PyPI/TestPyPI 发布、tag 创建和 GitHub release 与本矩阵
无关，仍需要单独批准。这些检查只属于 preview/design-assist 证据；不声称生产级物理验证，
也不声称形式化收敛证明。

Readiness 与 profile/环境相关。默认 profile 使用当前 Python 和当前 `PATH`；
维护者也可以设置 `OSA_SOLVER_PYTHON` 和
`OSA_SOLVER_READINESS_PROFILE=osa-solvers`，探测专用 solver Python，例如本地
`osa-solvers` conda 环境。该检查仍然只是 import/path detection，不是 solver 执行。

| Solver | 当前状态 | 可用性检测 | Opt-in env var | 脚本路径 | 预期输入 fixture | 预期输出 artifact | 风险 / 限制 | 需要明确批准 | 默认执行 | 生产级声明 | 形式化收敛声明 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Gmsh | 2026-05-20 已按 Gmsh-only 批准执行并通过；review 已接受为 optional manual mesh-generation smoke evidence | 当前 `PATH` 中的 `command -v gmsh`；可选 `gmsh` Python import probe | `OSA_RUN_OPTIONAL_GMSH_VALIDATION=1` | `scripts/run_optional_gmsh_validation.sh` | `examples/specs/gmsh_preview.json` | `/tmp/osa-gmsh-micro-benchmark-output/gmsh_preview.msh` 和 `/tmp/osa-gmsh-micro-benchmark-report.json` | 只验证 mesh 路径，不验证光学正确性 | 2026-05-20 仅批准、执行并 review Gmsh；未来再次运行需重新批准 | no | no | no |
| Meep | 2026-05-20 已按 Meep-only 批准执行并通过；review 接受为 optional manual PyMeep/FDTD smoke evidence | 当前 Python 或 `OSA_SOLVER_PYTHON` 中的 `meep` import probe；推荐 profile 为 `osa-solvers` | `OSA_RUN_OPTIONAL_MEEP_VALIDATION=1` | `scripts/run_optional_meep_validation.sh` | `examples/specs/missing_wavelength_meep_preview.json` | `/tmp/osa-meep-micro-benchmark-output/` artifact 和 `/tmp/osa-meep-micro-benchmark-report.json` | 只验证微型 PyMeep 路径，不是 production FDTD validation；即使探测到 `meep.mpb`，MPB 仍是单独 decision | 2026-05-20 仅批准、执行并 review Meep，且使用 `OSA_SOLVER_PYTHON=/opt/homebrew/Caskroom/miniforge/base/envs/osa-solvers/bin/python`；未来再次运行需重新批准 | no | no | no |
| MPB | 已有窄范围手动报告，候选 ready | 当前 Python 或 `OSA_SOLVER_PYTHON` 中的 `meep.mpb` import probe；可选 `mpb` CLI path | `OSA_RUN_OPTIONAL_MPB_VALIDATION=1` | `scripts/run_optional_mpb_validation.sh` | `examples/specs/mpb_preview.json` | `/tmp/osa-mpb-validation/mpb_validation_result.json` 和报告 JSON | 只验证微型 band 路径，不是 band convergence 证据 | yes | no | no | no |
| Optiland | 2026-05-20 已按 Optiland-only 批准执行并通过；review 接受为 optional manual ray/path smoke evidence | 当前 Python 或 `OSA_SOLVER_PYTHON` 中的 `optiland` import probe，可选 CLI path | `OSA_RUN_OPTIONAL_OPTILAND_VALIDATION=1` | `scripts/run_optional_optiland_validation.sh` | `examples/specs/optiland_preview.json` | `/tmp/osa-optiland-micro-benchmark-output/optiland_validation_result.json` 和 `/tmp/osa-optiland-micro-benchmark-report.json` | 只验证微型 ray/backend 路径，不是透镜设计验证 | 2026-05-20 仅批准、执行并 review Optiland；未来再次运行需重新批准 | no | no | no |
| Elmer | deferred | 仅 `command -v ElmerSolver` | `OSA_RUN_OPTIONAL_ELMER_VALIDATION=1` | `scripts/run_optional_elmer_validation.sh` | 未来本地 `.sif` fixture | `/tmp/osa-elmer-validation/elmer_validation_report.json` | 等待可维护的 ElmerSolver 安装路径；Elmer 仍是 Level 2 + Level-3-ready | yes | no | no | no |

批准必须明确且针对具体 solver。批准模板见
[`optional_solver_micro_benchmark_approval_record_template.zh-CN.md`](optional_solver_micro_benchmark_approval_record_template.zh-CN.md)。
readiness 状态见
[`optional_solver_micro_benchmark_readiness_status.md`](optional_solver_micro_benchmark_readiness_status.md)。
环境 profile 见
[`optional_solver_environment_profiles.zh-CN.md`](optional_solver_environment_profiles.zh-CN.md)。
未来执行审批包见
[`optional_solver_micro_benchmark_execution_packet.zh-CN.md`](optional_solver_micro_benchmark_execution_packet.zh-CN.md)，
pending per-solver records 位于
[`optional_solver_approval_records/`](optional_solver_approval_records/)，一次只运行一个
solver 的顺序见 [`optional_solver_execution_sequence.zh-CN.md`](optional_solver_execution_sequence.zh-CN.md)。
Gmsh review record：
[`optional_solver_approval_records/gmsh_micro_benchmark_review_2026-05-20.md`](optional_solver_approval_records/gmsh_micro_benchmark_review_2026-05-20.md)。
它只接受 Gmsh mesh-generation smoke evidence，不批准 Optiland、Meep、MPB、
Elmer、PyPI/TestPyPI upload、tag 创建或 release 创建。
Optiland approval record：
[`optional_solver_approval_records/optiland_micro_benchmark_approval_2026-05-20.md`](optional_solver_approval_records/optiland_micro_benchmark_approval_2026-05-20.md)。
Optiland review record：
[`optional_solver_approval_records/optiland_micro_benchmark_review_2026-05-20.md`](optional_solver_approval_records/optiland_micro_benchmark_review_2026-05-20.md)。
它只接受 optional manual ray/path smoke evidence，不批准 Meep、MPB、Elmer、
未来 Gmsh 或 Optiland rerun、PyPI/TestPyPI upload、tag 创建或 release 创建。
Meep approval record：
[`optional_solver_approval_records/meep_micro_benchmark_approval_2026-05-20.md`](optional_solver_approval_records/meep_micro_benchmark_approval_2026-05-20.md)。
Meep evidence record：
[`../validation/meep/meep_micro_benchmark_2026-05-20.md`](../validation/meep/meep_micro_benchmark_2026-05-20.md)。
Meep review record：
[`optional_solver_approval_records/meep_micro_benchmark_review_2026-05-20.md`](optional_solver_approval_records/meep_micro_benchmark_review_2026-05-20.md)。
它只接受 optional manual PyMeep/FDTD smoke evidence，不批准 MPB、Elmer、
未来 Gmsh/Optiland/Meep rerun、PyPI/TestPyPI upload、tag 创建或 release 创建。
Meep decision packet：
[`optional_solver_approval_records/meep_micro_benchmark_decision_packet.md`](optional_solver_approval_records/meep_micro_benchmark_decision_packet.md)。
它记录必需的 `OSA_SOLVER_PYTHON` profile、命令、artifact 和 non-claims，用于
已批准的 Meep-only run。
