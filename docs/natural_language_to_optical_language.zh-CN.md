# 自然语言到光学语言

本文档定义后端如何把用户目标转换成光学设计语言。

## 映射路径

当前本地后端映射：

自然语言目标 -> 需求模板 -> 光学语言摘要 -> 设计案例 -> 材料/几何/适配器/计算器路径 -> 工具调用账本。

映射器是确定性的本地逻辑，不调用外部 LLM。

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

