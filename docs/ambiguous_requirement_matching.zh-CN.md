# 歧义需求匹配

需求匹配采用确定性的关键词逻辑，把自然语言目标映射到本地光学设计模板，
不会调用外部 LLM。

## 置信度级别

- `high`：一个设计族明显占优。
- `medium`：可以给出安全默认模板，但重要输入仍缺失。
- `low`：多个设计族都可能成立，或目标约束不足。
- `none`：没有匹配到支持的本地模板。

## 响应字段

`POST /api/design-requirements/match` 返回：

- `candidate_templates`
- `ambiguity_notes`
- `missing_disambiguation_inputs`
- `recommended_questions`
- `safe_default_template`
- `no_external_llm_used=true`

有歧义的目标会生成问题，而不是直接采取不安全的求解器动作。例如，
同时提到波导和薄膜的目标会返回两个候选设计族，并询问用户优先走哪条路径。

## 安全行为

- 默认不调用外部 LLM。
- 默认不执行外部求解器。
- 未知目标不会静默选择求解器路径。
- 结果保持 preview/design-assist，不声称生产级验证。

## Application Domain Coverage

The rc8.dev0 backend now includes `GET /api/application-domains`,
`POST /api/application-domains/match`, and `GET /api/application-domain-cross-checks`.
These local-only endpoints connect ten preview domains to material suitability,
requirement templates, expected calculators/adapters, missing-input questions,
and deferred capability notes. They do not execute solvers, call external LLMs,
or claim production-grade physical validation.
