# 光学计算器案例集成

本文档记录本地预览计算器如何接入光学设计案例和 Agent Task Session。

## 当前案例映射

| 示例 / 目标类型 | 计算器调用 | 实际计算内容 | 不计算什么 |
| --- | --- | --- | --- |
| `thin_film_coating` | `optics.thin_film.spectrum`、`POST /api/optics/thin-film-spectrum`、`POST /api/optics/quarter-wave-ar` | 法向入射薄膜光谱扫描和四分之一波长减反膜起点。 | 不做材料色散拟合，不做角度/偏振完整镀膜设计，不声明生产级验证。 |
| `waveguide_mode` | `optics.waveguide.sweep`、`POST /api/optics/waveguide-sweep`、`POST /api/optics/waveguide-single-mode-range` | 标量 slab V-number 厚度扫描和可能单模厚度范围。 | 不求解矢量本征模，不验证 ridge/asymmetric 波导模式。 |
| `lens_raytrace_preview` | `optics.paraxial.two_lens_relay`、`POST /api/optics/two-lens-relay` | 理想薄透镜 relay 和 ABCD 摘要。 | 不做完整光线追迹，不做像差或玻璃优化。 |
| 高斯光束目标 | `optics.gaussian_beam.series`、`POST /api/optics/gaussian-beam-series`、`POST /api/optics/gaussian-beam-focus` | 光束传播采样和理想薄透镜聚焦估计。 | 不包含 M²、孔径截断、像差或实测光束验证。 |
| 纳米颗粒 / 超表面目标 | 材料和适配器预览 | 材料建议、适配器推荐、工作流和产物预览。 | 除非目标明确要求支持的计算器类型，否则不套用标量计算器。 |

## Tool-call ledger 行为

`POST /api/agent-session` 会返回 `tool_call_ledger`。当检测到支持的案例时，
对应计算器记录会以 `tool_kind=internal_python` 和 `executed=true` 记录下来。
外部求解器、外部 LLM、上传、发布、tag 和 release 记录仍保持 `executed=false`。

## 安全边界

所有计算器集成都保持本地、确定性和 preview/design-assist：

- 默认不执行外部求解器。
- 默认不调用外部 LLM。
- 不联网查询材料数据库。
- 不上传 PyPI/TestPyPI。
- 不创建 tag 或 GitHub release。
- 不声明生产级物理验证。
- 不声明形式化收敛证明。
