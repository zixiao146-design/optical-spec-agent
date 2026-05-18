# 设计案例交叉检查

Current public prerelease: v0.9.0rc6。Current main development version:
`0.9.0rc7.dev0`。

设计案例交叉检查用于确认 `examples/optical_design/` 中的每个本地光学设计示例
都能被加载、转成确定性的 `AgentTaskSession`，并通过 `tool_call_ledger`
证明实际调用了哪些内部工具。

## 检查内容

每个示例会检查：

- `spec.json` 是否存在。
- `expected_agent_trace.json` 是否存在。
- 能否构建本地 agent task session。
- 是否生成材料建议。
- 是否生成适配器建议。
- 如果该设计族有标量预览计算器，是否记录了预期计算器调用。
- 安全 flags 是否保持 false。

## 示例到计算器映射

| 示例 | 预期计算器行为 |
| --- | --- |
| `thin_film_coating` | 应执行 `optics.thin_film` 预览。 |
| `waveguide_mode` | 应执行 `optics.waveguide` 预览。 |
| `lens_raytrace_preview` | 应执行 `optics.paraxial` 预览。 |
| `nanoparticle_plasmonics` | 材料 + 适配器 trace；不要求标量计算器。 |
| `photonic_crystal_band` | MPB/适配器 trace；不要求标量计算器。 |
| `dielectric_metasurface_preview` | 材料 + 适配器 trace；不要求标量计算器。 |

## 状态语义

- `pass`：必需文件存在，预期后端调用存在。
- `warning`：示例可用，但存在需要审阅的非阻断问题。
- `fail`：必需文件、session、材料建议、适配器建议或预期计算器调用缺失。

## 运行方式

API:

```bash
curl http://127.0.0.1:8000/api/design-case-cross-checks
```

烟测脚本:

```bash
./scripts/smoke_backend_report.sh
```

## 安全边界

交叉检查只属于 preview/design-assist。它不运行外部求解器，不调用外部 LLM，
不访问网络，不上传包，不创建 tag/release，不声明生产级物理验证，也不声明形式化收敛证明。
