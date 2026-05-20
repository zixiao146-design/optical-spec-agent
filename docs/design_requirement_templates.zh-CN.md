# 设计需求模板

本文档说明本地设计需求模板如何把自然语言光学目标映射成确定性的光学语言。这是 Agent Studio 和 Agent 命令中心的后端能力。

Current public prerelease: `v0.9.0rc7`
Current main release draft: `0.9.0rc8`
API contract version: `0.1`
PyPI：未发布

## 目的

需求模板让后端路径更清楚：

自然语言目标 -> 光学语言 -> 设计案例 -> 预期工具调用 -> 预览产物 -> 证据边界。

这个映射使用本地确定性启发式规则，不调用外部 LLM，不访问网络，也不执行外部求解器。

## 七个模板

| 模板 | 光学意图 | 预期工具/计算器路径 |
| --- | --- | --- |
| `thin_film_ar_coating` | 薄膜增透镀膜预览 | `optics.thin_film.spectrum`、四分之一波 helper |
| `gaussian_beam_focus` | 高斯光束传播/聚焦预览 | `optics.gaussian_beam.series`、聚焦 helper |
| `slab_waveguide_single_mode` | 平板波导单模估计 | `optics.waveguide.sweep`、单模厚度范围 helper |
| `paraxial_lens_imaging` | 近轴透镜成像预览 | `optics.paraxial.two_lens_relay`、薄透镜 helper |
| `photonic_crystal_band_preview` | 光子晶体能带预览 | MPB 适配器预览路径 |
| `dielectric_metasurface_preview` | 介质超表面预览 | Meep/Gmsh 适配器预览路径 |
| `nanoparticle_plasmonics` | 纳米颗粒散射预览 | Meep/Gmsh 适配器预览路径 |

## 匹配规则

匹配器只使用本地关键词启发式规则。例如：

- `coating`、`anti-reflection`、`thin film`、`增透`、`镀膜` -> `thin_film_ar_coating`
- `Gaussian`、`beam waist`、`Rayleigh`、`高斯光束`、`光腰` -> `gaussian_beam_focus`
- `waveguide`、`single mode`、`波导`、`单模` -> `slab_waveguide_single_mode`
- `lens`、`imaging`、`relay`、`透镜`、`成像` -> `paraxial_lens_imaging`
- `photonic crystal`、`band diagram`、`光子晶体`、`能带` -> `photonic_crystal_band_preview`
- `metasurface`、`metalens`、`超表面`、`超透镜` -> `dielectric_metasurface_preview`
- `nanoparticle`、`plasmonic`、`scattering`、`纳米颗粒`、`散射` -> `nanoparticle_plasmonics`

未知目标会返回 `none`/低置信度的安全结果，列出缺失输入和建议澄清步骤。
有歧义的目标会返回 candidate templates、ambiguity notes、missing
disambiguation inputs 和 recommended questions，而不是直接采取不安全的求解器动作。
见 `docs/ambiguous_requirement_matching.zh-CN.md`。

## 预期工具调用

每个匹配模板都期望：

- `requirements.match_template`
- `requirements.extract_optical_intent`
- `optical_language.infer_source_monitor`
- `optical_language.diagnose_missing_inputs`
- `material_catalog.suggest`
- `requirements.match_ambiguity_check`
- `optical_language.generate_disambiguation_questions`
- 有本地设计案例时执行 `example_registry.load`
- `agent_trace.build`
- `workflow_plan.preview`
- `adapter_preview.generate`

计算器支持的案例会额外记录对应的本地光学计算器调用。这些调用都是内部 Python 预览/设计辅助函数。

每个模板也包含：

- `source_model`
- `monitor_model`
- `required_source_inputs`
- `required_monitor_inputs`
- `default_source_assumptions`
- `default_monitor_assumptions`

这些字段让光源、监测器和观测量假设在工作流或适配器预览前显式可见。

## 安全边界

- 默认不执行外部求解器。
- 默认不调用外部 LLM。
- 不联网查询材料数据库。
- 不暴露 PyPI/TestPyPI 上传、tag 或 release 操作。
- 输出仅用于 preview/design-assist。
- 不声明生产级物理验证。
- 不声明形式化收敛证明。

## Application Domain Coverage

The rc8 backend now includes `GET /api/application-domains`,
`POST /api/application-domains/match`, and `GET /api/application-domain-cross-checks`.
These local-only endpoints connect ten preview domains to material suitability,
requirement templates, expected calculators/adapters, missing-input questions,
and deferred capability notes. They do not execute solvers, call external LLMs,
or claim production-grade physical validation.
