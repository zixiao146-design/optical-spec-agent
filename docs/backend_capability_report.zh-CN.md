# 后端能力报告

Current public prerelease: v0.9.0rc6。Current main development version:
`0.9.0rc7.dev0`。

后端能力报告用于向维护者说明：当前本地 Agent Studio 后端到底能
import 什么、调用什么、执行了什么，以及默认阻断了什么。报告由
`scripts/generate_backend_capability_report.py` 生成，也可通过
`GET /api/backend-capability-report` 获取。

## 报告证明什么

- package 版本仍为 `0.9.0rc7.dev0`；PyPI 未发布。
- 子智能体角色出现在真实的样例 `AgentTaskSession` trace 中。
- 内部工具是可 import、可调用、并记录在样例 `tool_call_ledger` 中的。
- 光学计算器是带参考 sanity case 的本地 preview/design-assist 工具。
- 光学设计示例会和 agent session、预期计算器调用、材料建议、适配器建议进行交叉检查。
- 外部 solver、外部 LLM、TestPyPI 上传、PyPI 发布、git tag、GitHub release
  默认不执行，或需要明确审批。

## 报告章节

1. `package`：包版本、公开候选版本、main 开发版本、TestPyPI 验证状态、PyPI 发布状态。
2. `sub_agents`：`SpecAgent`、`MaterialAgent`、`GeometryAgent`、
   `AdapterAgent`、`WorkflowAgent`、`EvidenceAgent`、`SafetyAgent`、
   `RecommendationAgent` 的执行现实。
3. `internal_tools`：材料库、示例注册表、agent trace builder、task session
   builder、adapter preview generator、workflow planner、optical calculators。
4. `optical_calculators`：thin-film、paraxial、Gaussian beam、waveguide
   预览计算器、API endpoint、参考 case、failure mode、`sanity_checked_preview` 质量级别。
5. `design_case_cross_checks`：每个光学设计示例的 pass/warning/fail 交叉检查。
6. `blocked_external_actions`：solver、LLM、上传、发布、tag、release 默认不执行。

## 如何生成

```bash
python scripts/generate_backend_capability_report.py \
  --json-out /tmp/osa-backend-capability-report.json \
  --markdown-out /tmp/osa-backend-capability-report.md
```

烟测：

```bash
./scripts/smoke_backend_report.sh
```

## 安全边界

- 默认不执行外部求解器。
- 默认不调用外部 LLM。
- 不执行上传。
- 不创建 tag。
- 不创建 release。
- 报告只作为 preview/design-assist 证据。
- 不声明生产级物理验证。
- 不声明形式化收敛证明。
