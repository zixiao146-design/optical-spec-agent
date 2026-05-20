# 应用领域 Benchmark

应用领域 benchmark suite 会把本地 application domain registry 转换成可检查的
场景证据，用来验证后端如何处理明确、歧义、输入不足、不支持和需要阻断的光学
设计请求。

该 benchmark 是确定性、本地、preview/design-assist 证据。它不执行外部求解器，
不调用外部 LLM，不上传包，不创建 tag，也不创建 GitHub release。它不声称生产级
物理验证，也不声称形式化收敛证明。

## 场景类型

| 类型 | 目的 | 预期行为 |
| --- | --- | --- |
| `positive` | 已支持的本地预览领域 | 匹配预期 domain/template，并记录预期计算器或 adapter 行为。 |
| `ambiguous` | 多个光学领域都可能成立 | 保留候选领域并提出追问，而不是不安全地强行匹配。 |
| `underconstrained` | 能识别领域但缺少关键输入 | 报告关键/可选缺失输入并给出建议问题。 |
| `unsupported` | 请求需要不可用或 proprietary 执行 | 阻断或延期，并建议本地预览替代路径。 |
| `unsafe_or_blocked` | 请求要求过度声明或不安全证明 | 阻断生产级验证或形式化收敛证明声明。 |

## 覆盖范围

benchmark 数据位于 `examples/application_domain_benchmarks/`。正向场景覆盖：

- `nanoparticle_plasmonics`
- `thin_film_coating`
- `slab_waveguide`
- `photonic_crystal`
- `dielectric_metasurface`
- `lens_ray_optics`
- `gaussian_beam_focusing`
- `imaging_system_preview`
- `fiber_coupling_preview`
- `polarization_optics_preview`

额外场景覆盖波导/薄膜歧义、透镜/Gaussian 聚焦歧义、缺失焦距、缺失纳米颗粒半径
和材料、完整 Zemax 优化、完整 Lumerical FDTD，以及生产级验证请求。

## 评价标准

每个场景记录：

- 预期主 domain 和候选 domains
- 预期 confidence
- 预期 requirement template
- 预期材料、计算器和 adapter 行为
- 预期关键/可选缺失输入
- 预期追问
- 预期阻断动作
- preview-only 安全标记

evaluator 会把这些预期与本地确定性 domain matching、requirement matching、必要时
生成的 Agent Task Session 以及 tool-call ledger 对比。它不会执行求解器代码。

## API 和脚本

```bash
python scripts/evaluate_application_domain_benchmarks.py
```

API endpoints:

- `GET /api/application-domain-benchmarks`
- `GET /api/application-domain-benchmarks/{scenario_id}`
- `POST /api/application-domain-benchmarks/{scenario_id}/evaluate`
- `GET /api/application-domain-benchmark-results`

## Pass / Warn / Fail

- `pass`: 本地确定性预览行为符合预期。
- `warn`: 后端行为安全，但该场景代表部分覆盖或延期能力。
- `fail`: 后端缺失了预期匹配、追问、阻断动作或工具行为。

截至 `0.9.0rc8`，光纤耦合和偏振光学的 positive benchmark 已由确定性
预览计算器闭环：

- `fiber_coupling_preview_positive` 记录
  `optics.fiber_coupling.gaussian_mode_overlap`。
- `polarization_optics_preview_positive` 记录 `optics.polarization.jones`。

对应的计算器级 reference sanity cases 见
[`fiber_polarization_reference_cases.zh-CN.md`](fiber_polarization_reference_cases.zh-CN.md)。

除非未来新增有意延期的能力，benchmark suite 预期为
`19 pass / 0 warn / 0 fail`。

## 安全边界

benchmark suite 不证明真实 solver monitor 结果，不证明生产级物理验证，不证明形式化
收敛。外部求解器、外部 LLM、proprietary 工具、上传、tag 和 release 都不在默认
benchmark 路径中。
