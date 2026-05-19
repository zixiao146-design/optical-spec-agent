# 缺失输入诊断

缺失输入诊断会区分 critical inputs 和 optional inputs，使后端可以生成安全的本地预览，
同时默认阻止求解器执行。

## 关键输入与可选输入

关键输入决定物理问题或一阶计算路径，例如：

- 纳米颗粒半径、材料、波长范围
- 薄膜目标波长和基底
- 波导芯层、包层、厚度、波长
- 透镜焦距和物距

可选输入提升预览质量，例如偏振、入射角、孔径、视场、背景介质或模式族。

## 默认值和问题

诊断会报告：

- `missing_critical_inputs`
- `missing_optional_inputs`
- `default_assumptions_applied`
- `ambiguity_notes`
- `blocking_questions`
- `safe_to_preview=true`
- `safe_to_run_solver=false`

后端可以在默认值可见的前提下生成 design-assist 预览，但这些默认值不等同于求解器执行批准。

## 边界

- 不执行外部求解器。
- 不调用外部 LLM。
- 默认假设显式、可审阅。
- 不声称生产级物理验证或形式化收敛证明。

## Application Domain Coverage

The rc8.dev0 backend now includes `GET /api/application-domains`,
`POST /api/application-domains/match`, and `GET /api/application-domain-cross-checks`.
These local-only endpoints connect ten preview domains to material suitability,
requirement templates, expected calculators/adapters, missing-input questions,
and deferred capability notes. They do not execute solvers, call external LLMs,
or claim production-grade physical validation.
