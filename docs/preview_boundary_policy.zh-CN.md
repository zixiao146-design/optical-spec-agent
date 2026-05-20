# Preview Boundary Policy

本文档定义 `0.9.0rc8.dev0` 后端证据的边界。当前后端可以作为确定性的
光学设计辅助工具，但所有证据仍必须保持 preview/design-assist 级别。

## Preview/Design-Assist 的含义

用户可以依赖后端完成：

- 将支持的光学设计目标确定性地路由到 template 和 application domain；
- 报告 critical / optional 缺失输入；
- 运行本地解析计算器，给出 sanity-checked preview；
- 生成 adapter-native source/monitor metadata preview；
- 默认阻断 external solver、external LLM、upload、tag 和 release 动作；
- 通过本地脚本和 API 响应暴露证据。

用户必须自行验证：

- 材料常数和波长相关数据；
- solver-specific source、monitor、mesh 和 boundary 设置；
- 物理精度、收敛性和容差；
- 生产 workflow 的适用性。

## 组件边界

| 组件 | 边界 |
| --- | --- |
| Materials | 本地 curated preview catalog；不是生产级 optical constants database。 |
| Calculators | sanity-checked analytic preview；不是生产级物理验证。 |
| Application domains | benchmark 检查确定性路由和诊断，不证明物理正确性。 |
| Source/monitor models | 仅 preview metadata；不声称真实 solver monitor result。 |
| Adapter mappings | adapter-native 语义预览；真实结果需要显式批准 solver execution。 |
| Optional solver micro-benchmarks | 仅手动、显式 opt-in；默认 tests、smoke、quality gates 和 release gates 不运行 solver。 |
| Optional solver readiness | profile-aware availability detection、approval matrix 和 execution approval packet；不执行 solver，也不授权 PyPI/TestPyPI upload、tag 或 release。 |
| Sub-agents | 确定性后端角色；不是独立自主服务。 |
| Frontend | UI/demo surface；不是验证证据。 |

## 发布边界

即使之后批准 PyPI publication，也不代表生产级物理验证。发布和打包状态与
物理验证、solver convergence、材料数据验证是分开的。

## 不声称

- 不声称生产级物理验证。
- 不声称形式化收敛证明。
- 不声称 guaranteed accuracy。
- 默认不执行 external solver。
- Optional solver-backed validation 只能手动显式 opt-in。
- Optional solver readiness check 不执行 solver binary，也不授权发布或 release 动作。
- Optional solver execution approval packet 和 pending records 只为未来 review 做准备；
  它们本身不授权 solver execution。
- 2026-05-20 已批准并执行的 Gmsh-only micro-benchmark 只记录为可选手动
  mesh generation smoke 证据，不是光学正确性证据；review decision 不批准
  Optiland、Meep、MPB、Elmer 或未来 Gmsh rerun。
- 2026-05-20 单独批准并执行的 Optiland-only micro-benchmark 已 review 接受为
  可选手动 ray/path smoke 证据，不是透镜设计验证；它不批准 Meep、MPB、Elmer
  或未来 Optiland rerun。
- 2026-05-20 单独批准并执行的 Meep-only micro-benchmark 使用
  `OSA_SOLVER_PYTHON`，review 后只接受为 optional manual PyMeep/FDTD smoke evidence；
  它不批准 MPB、Elmer 或未来 Meep rerun。
- 2026-05-20 单独批准并执行的 MPB-only micro-benchmark 使用
  `OSA_SOLVER_PYTHON` 和 `meep.mpb`，只记录为 optional manual MPB/band-structure
  smoke evidence，等待单独 review；它不批准 Elmer 或未来 MPB rerun。
- `OSA_SOLVER_PYTHON` 可用于把 import-only probe 指向专用 solver Python；
  Gmsh 等 CLI 工具仍从当前 `PATH` 探测。
- 默认不调用 external LLM。
- Elmer Level 3 仍然 deferred。
