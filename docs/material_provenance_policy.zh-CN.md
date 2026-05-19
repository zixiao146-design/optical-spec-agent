# 材料溯源策略

材料库是本地 preview/design-assist 目录，可用于 agent 规划、材料建议和
adapter 预览元数据，但不是生产级光学常数数据库。

## 溯源字段

每个材料记录包含：

- `provenance_type`：`curated_preview`、`placeholder`、`approximate_constant` 或 `user_must_verify`。
- `source_note`：本地 starter catalog 来源说明。
- `citation_note`：可选引用或人工审核说明。
- `wavelength_validity_note`：提醒用户验证色散和波长相关数据。
- `known_limitations`：该材料条目的预览限制。
- `suitable_for` / `not_suitable_for`：本地设计辅助提示。
- `requires_user_verification`：starter materials 始终为 true。
- `production_grade_optical_constants`：始终为 false。

## 适用性诊断

`POST /api/materials/diagnose` 会针对纳米颗粒等离激元、波导、薄膜镀膜、
透镜、光子晶体或超表面等应用给出确定性的本地适用性说明。

该接口返回 rationale、warnings、missing context 和 recommended verification。
它不会联网查询材料数据库，不会执行求解器，不会调用外部 LLM，也不会把预览常数升级为生产级证据。

## 边界

- 材料常数只是近似预览值。
- 用户必须独立验证波长相关 n/k 数据。
- 材料库不声称生产级物理验证。
- 材料库不声称形式化收敛证明。

## Application Domain Coverage

The rc8.dev0 backend now includes `GET /api/application-domains`,
`POST /api/application-domains/match`, and `GET /api/application-domain-cross-checks`.
These local-only endpoints connect ten preview domains to material suitability,
requirement templates, expected calculators/adapters, missing-input questions,
and deferred capability notes. They do not execute solvers, call external LLMs,
or claim production-grade physical validation.
