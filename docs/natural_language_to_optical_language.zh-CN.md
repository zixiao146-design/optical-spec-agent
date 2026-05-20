# 自然语言到光学语言

本文档定义后端如何把用户目标转换成光学设计语言。

## 映射路径

当前本地后端映射：

自然语言目标 -> 需求模板 -> 光学语言摘要 -> 设计案例 -> 材料/几何/适配器/计算器路径 -> 工具调用账本。

映射器是确定性的本地逻辑，不调用外部 LLM。对于有歧义或约束不足的目标，
它会返回 confidence、candidate templates、missing disambiguation inputs 和
recommended questions；未知目标不会静默选择求解器路径。

## 光学语言字段

- `physical_system`：光学系统类型，例如 `thin_film_stack`、`gaussian_beam`、`slab_waveguide`、`paraxial_lens_system`、`photonic_crystal`、`metasurface` 或 `nanoparticle_on_film`。
- `material_system`：本地预览材料候选。
- `geometry_model`：本地几何抽象，例如薄膜叠层、高斯光束、平板波导、ABCD 薄透镜系统、周期晶格、meta-atom 阵列或球-膜结构 scaffold。
- `solver_or_adapter_family`：开源优先适配器或本地计算器路径。
- `calculator_or_tool_path`：预期的确定性内部函数或 API 路由。
- `evidence_boundary`：结果能说明什么、不能说明什么。

## 示例

英文镀膜目标：

> Design a local preview for a single-layer anti-reflection coating on glass at 550 nm.

映射为：

- template：`thin_film_ar_coating`
- physical system：`thin_film_stack`
- tool path：`/api/optics/thin-film-spectrum` 和 `/api/optics/quarter-wave-ar`

中文纳米颗粒目标：

> 请为一个银纳米颗粒位于薄膜上的散射问题生成本地预览工作流。

映射为：

- template：`nanoparticle_plasmonics`
- physical system：`nanoparticle_on_film`
- tool path：材料库、agent trace、工作流预览、适配器预览

## 限制

- 匹配器是启发式规则，不是语义 AI。
- 未知目标会返回低置信度安全建议。
- 计算器输出仅用于 preview/design-assist。
- 默认不执行外部求解器，也不调用外部 LLM。
- 不声明生产级物理验证，也不声明形式化收敛证明。

## 光源和监测器步骤

光学语言路径现在包含确定性的光源/监测器推断：

- `source_model`：光源类型、波长范围、偏振、入射方向、光腰或模式编号。
- `monitor_model`：监测器类型、观测量、区域、采样和单位。
- `optical_language_diagnostics`：缺失输入、默认假设、歧义说明、阻断问题、
  `safe_to_preview` 和 `safe_to_run_solver=false`。

纳米颗粒散射预览默认使用平面波式光源、400-900 nm 波段、`linear_x` 偏振，
以及散射/消光谱监测器。这只是元数据，不是外部求解器 monitor 结果。

参见 `docs/optical_language_source_monitor.zh-CN.md` 和
`docs/source_monitor_missing_input_diagnostics.zh-CN.md`。

## 歧义与缺失输入

rc8 后端会区分关键缺失输入和可选缺失输入：

- `missing_critical_inputs`：有意义的求解器设置前需要明确的值。
- `missing_optional_inputs`：可提升预览质量的上下文。
- `recommended_questions`：确定性追问。

`safe_to_preview` 可以在本地 design-assist 预览中保持 true，但
`safe_to_run_solver` 默认仍为 false。见
`docs/ambiguous_requirement_matching.zh-CN.md` 和
`docs/missing_input_diagnostics.zh-CN.md`。

## Application Domain Coverage

The rc8 backend now includes `GET /api/application-domains`,
`POST /api/application-domains/match`, and `GET /api/application-domain-cross-checks`.
These local-only endpoints connect ten preview domains to material suitability,
requirement templates, expected calculators/adapters, missing-input questions,
and deferred capability notes. They do not execute solvers, call external LLMs,
or claim production-grade physical validation.
