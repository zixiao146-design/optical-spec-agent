# 示例库

示例库让 Agent Studio 中的内置光学设计工作流更容易发现、加载和演示。

当前范围：
- 本地光学设计示例位于 `examples/optical_design/`。
- 示例库使用 `GET /api/examples` 和 `GET /api/examples/{example_id}`。
- 每个示例把设计目标、预览材料、适配器推荐、工作流重点、预期协作轨迹和下一步建议串起来。
- 示例只用于本地预览工作流。

包含的示例类型：
- nanoparticle_plasmonics
- thin_film_coating
- waveguide_mode
- photonic_crystal_band
- dielectric_metasurface_preview
- lens_raytrace_preview

工作流串联：
示例库 -> 加载示例 -> 材料建议 -> 适配器推荐 -> 多智能体协作轨迹 -> 工作流计划 -> 适配器产物预览 -> 验证证据 -> 下一步建议。

计算器串联：
- `thin_film_coating` 映射到薄膜光谱扫描和四分之一波长 AR 预览。
- `waveguide_mode` 映射到波导 V-number 厚度扫描和单模范围预览。
- `lens_raytrace_preview` 映射到近轴双透镜 relay 预览。
- 高斯光束目标映射到高斯光束传播序列和聚焦预览。
- 纳米颗粒和超表面示例默认保持材料/适配器/工作流预览，除非目标明确适合标量计算器。

安全边界：
- 默认不执行外部求解器。
- 默认不调用外部 LLM。
- 材料数据只是预览/设计辅助。
- 预览产物不代表生产级物理验证。
- 不声明形式化收敛证明。
- 前端不控制 PyPI/TestPyPI 上传、GitHub tag 或 GitHub release。
