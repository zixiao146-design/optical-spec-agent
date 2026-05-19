# 材料库

材料库是一个本地预览材料目录，用于光学设计辅助。它帮助 Agent Studio
为示例和工作流计划推荐 starter materials，但它不是生产级光学常数数据库。

当前状态：
- Current public prerelease: v0.9.0rc7
- Current main development version: 0.9.0rc8.dev0
- API contract version: 0.1
- 材料库状态：本地预览 / 设计辅助
- PyPI：未发布

当前包含：
- air
- water
- sio2
- si
- si3n4
- tio2
- al2o3
- au
- ag
- ito
- gaas
- glass_bk7_preview
- glass_fused_silica_preview

推荐规则：
- nanoparticle plasmonics -> Au、Ag、SiO2、water、air
- dielectric metasurface -> TiO2、Si3N4、Si、SiO2
- waveguide -> Si、SiO2、Si3N4
- thin film coating -> SiO2、TiO2、Al2O3
- lens/ray optics -> BK7 preview、fused silica preview、air
- photonic crystal band -> Si、GaAs、SiO2、air

材料溯源：
- 每个 starter material 都暴露 `provenance_type`、`source_note`、
  `wavelength_validity_note`、`known_limitations`、`requires_user_verification`
  和 `production_grade_optical_constants=false`。
- 数值 n/k 只是近似预览常数，除非未来条目明确记录更强的审核溯源。
- `POST /api/materials/diagnose` 会针对一个材料/应用组合返回适用性 rationale、
  warnings、missing context 和 recommended verification。
- 目录策略见 `docs/material_provenance_policy.zh-CN.md`。

安全边界：
- 材料值只是近似预览/设计辅助提示。
- 做物理结论前，用户必须独立核验材料常数。
- 不声明生产级物理验证。
- 不声明形式化收敛证明。
- 默认不执行外部求解器。
- 默认不调用外部 LLM。
- 不联网查询外部材料数据库。

前端使用：
- Agent Studio 提供“材料库”页面。
- 页面展示本地材料记录和材料建议。
- 页面会在适用时把材料和示例库中的案例关联起来。
- 页面必须清楚显示材料数据为 preview-only。
