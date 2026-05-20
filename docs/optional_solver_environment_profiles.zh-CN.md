# 可选 Solver 环境 Profile

可选 solver readiness 与运行环境相关。同一个 solver 可能在项目当前
Python 中不可用，但在维护者专用的 `osa-solvers` conda 环境中可以导入。

## Profile

| Profile | 用途 | 探测方式 | 默认执行 solver |
| --- | --- | --- | --- |
| `current` | 当前 Python 与当前 `PATH` | Python import 探测和命令路径探测 | 否 |
| `osa-solvers` | 维护者本地专用 solver conda 环境 | 通过 `OSA_SOLVER_PYTHON` 做 Python import 探测 | 否 |
| `homebrew-cli` | 当前 `PATH` 上的 `gmsh` 等 CLI 工具 | 只做命令路径探测 | 否 |
| `deferred-elmer` | Elmer 文档状态 | deferred command readiness | 否 |

## Solver Python

可以用 `OSA_SOLVER_PYTHON` 指定 solver 专用 Python：

```bash
OSA_SOLVER_PYTHON=/opt/homebrew/Caskroom/miniforge/base/envs/osa-solvers/bin/python \
OSA_SOLVER_READINESS_PROFILE=osa-solvers \
python scripts/check_optional_solver_readiness.py
```

脚本只会在该解释器中执行 `import meep`、`import meep.mpb` 等导入探测。
它不会运行 Meep、MPB、Gmsh、Optiland 或 Elmer 仿真。

## Solver 说明

- Gmsh readiness 通常基于当前 `PATH` 中的 `gmsh` CLI。
- Meep readiness 通常基于 Python 包 `meep`。
- MPB readiness 可以通过 `meep.mpb` Python 路径获得，即使没有 `mpb` CLI。
- Optiland readiness 可以基于 Python/package，也可能有 CLI。
- Elmer 仍然 deferred，直到存在可维护的 `ElmerSolver` 安装路径。

## 边界

- Profile 检查不会执行 solver。
- 缺少 solver 不阻塞默认检查。
- readiness detection 不是 solver 执行。
- solver-backed micro-benchmark 仍需要维护者明确批准。
- TestPyPI、PyPI、tag、release 与此无关，仍然单独 gate。
- 不声称生产级物理验证或形式化收敛证明。
