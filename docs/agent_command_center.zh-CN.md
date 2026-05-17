# Agent 命令中心

## 目的

Agent 命令中心是 Agent Studio 中面向任务的本地光学设计入口。它把自然语言目标转换成确定性的本地任务会话：

```text
用户目标 -> 光学意图 -> 设计案例 -> 材料 -> 适配器 -> 工作流 -> 产物 -> 证据 -> 下一步建议
```

它借鉴 coding-agent 风格的任务会话体验，但不是任何外部产品的复制品，也不复制外部品牌、文案或设计资产。

## 当前状态

- Current public prerelease: v0.9.0rc6
- Current main development version: 0.9.0rc7.dev0
- API contract version: 0.1
- PyPI: 未发布
- v0.9.0rc7 tag: 未创建
- v1.0.0 tag: 未创建

## API

命令中心使用：

- `POST /api/agent-session`
- `GET /api/examples`
- `GET /api/materials`
- `POST /api/materials/suggest`
- `POST /api/workflow-plan`
- `POST /api/adapter-preview`
- `GET /api/validation-evidence`

`POST /api/agent-session` 接收本地目标、可选本地示例 ID 和可选语言提示，返回 Agent Task Session：任务计划、子智能体轨迹、权限门控、本地产物、证据和下一步建议。

## 任务会话

Agent Task Session 包含：

- `session_id`
- `user_goal`
- `optical_intent_summary`
- `selected_example_id`
- `design_case_summary`
- `plan_steps`
- `agent_trace`
- `artifacts`
- `permission_gates`
- `final_recommendation`
- `recommended_next_actions`

## 权限门控

默认允许：

- 本地解析规格
- 读取本地材料库
- 生成本地工作流计划
- 生成本地适配器预览

默认阻断或需要在 Agent Studio 之外显式批准：

- 外部求解器执行
- 外部 LLM 调用
- TestPyPI 上传
- PyPI 发布
- Git tag 创建
- GitHub release 创建

## 安全边界

- 默认不执行外部求解器。
- 默认不调用外部 LLM。
- 默认不依赖闭源求解器。
- 不提供 PyPI/TestPyPI 发布控制。
- 不提供 GitHub tag/release 控制。
- 不声明生产级物理验证。
- 不声明形式化收敛证明。
- 材料库仍是 preview/design-assist，做物理结论前必须独立核验。

