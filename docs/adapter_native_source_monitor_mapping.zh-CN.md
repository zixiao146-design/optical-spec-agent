# 适配器原生光源/监测器映射

Current public prerelease: v0.9.0rc6. Current main development version:
`0.9.0rc7.dev0`。

本文说明本地后端如何把光源、监测器和观测量意图映射到各个开源适配器族的
原生预览语义。这里的映射都是 preview/design-assist 元数据。默认不执行外部
求解器，不调用外部 LLM，不上传，不创建 tag/release，不声明生产级物理验证，
也不声明形式化收敛证明。

## 目的

当前后端的确定性路径是：

自然语言目标 -> 光源/监测器推断 -> 观测量诊断 -> 适配器原生预览映射 ->
适配器预览元数据 -> tool-call ledger -> 下一步建议。

这些映射用于说明将来真正 solver 设置需要什么，不是真实 solver monitor 结果。

## Meep

- 平面波式光源意图映射为 Meep source 元数据。
- 宽带波长范围映射为 GaussianSource 或 broadband pulse 预览元数据。
- 散射谱或消光谱映射为 flux / DFT flux monitor 元数据。
- 近场和远场请求映射为 DFT field / far-field monitor 元数据。
- 真实散射、消光、近场、远场或相位结果需要显式批准后执行 Meep；本后端默认不执行。

## MPB

- 时域光源语义不能直接用于 MPB。
- 模式光源或光子晶体目标映射为 eigenmode / band context 元数据。
- band structure 观测量映射为 k-point 和 band-frequency 元数据。
- 真实 band frequency 或 mode field 需要显式执行 MPB。

## Gmsh

- Gmsh 本身不计算光学观测量。
- 光源和监测器意图会保存在几何、网格区域和 Physical Surface / Volume 注释元数据中。
- mesh region 支持预览；光场、频谱和模式结果需要后续显式批准的外部求解器。

## Elmer

- 光源和监测器意图映射为 FEM source、边界条件、solver section 和输出占位符。
- 真实 FEM 光学/电磁场需要显式执行 ElmerSolver。Elmer 仍是 Level 2 +
  Level-3-ready；本任务不会把 Elmer 标为 Level 3。

## Optiland

- Gaussian 或 ray-style 光源意图映射为 object / ray bundle 元数据。
- focal spot、image plane、ray fan 观测量映射为 raytrace 输出元数据。
- 真实 raytrace 结果需要后续显式批准后执行 Optiland。

## Tool-Call Reality

Agent session 会把 `optical_language.diagnose_observable` 和
`optical_language.map_source_monitor_to_adapter` 记录为已执行的内部 Python
tool call。外部 solver 记录仍为 `executed=false`，并保持 blocked 或需要显式批准。

## 安全边界

不声明生产级物理验证。不声明形式化收敛证明。适配器原生光源/监测器映射只是本地
预览元数据，不代表已经执行过外部求解器。
