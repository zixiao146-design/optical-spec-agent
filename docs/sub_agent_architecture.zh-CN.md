# 子智能体架构

Agent Studio 现在提供一个本地确定性的子智能体协作轨迹。这个轨迹用来把
agent workflow 可视化，但不会引入自主外部 agent、外部 LLM 调用、solver
执行、上传、tag 或 release 操作。

当前角色：
- SpecAgent：理解用户意图或 OpticalSpec，并识别缺失字段。
- MaterialAgent：从本地预览材料库推荐材料。
- GeometryAgent：识别几何类型和必要几何字段。
- AdapterAgent：推荐开源优先的 adapter/tool，并解释限制。
- WorkflowAgent：生成本地预览工作流计划，默认不执行求解器。
- EvidenceAgent：附加验证证据和成熟度说明。
- SafetyAgent：检查不过度声明、不默认运行 solver/LLM、不出现发布控制。
- RecommendationAgent：总结下一步建议。

输入/输出：
- 输入可以是本地文本、spec-like JSON object 或本地 example_id。
- 输出是 AgentTrace，包含多个 AgentStep 和最终建议。
- 每一步包含 `step_index`、`stage`、输入摘要、输出摘要、diagnostics、
  recommended next actions、confidence、status、safety notes 和 evidence refs。
- 示例专用轨迹可通过 `POST /api/examples/{example_id}/agent-trace` 生成。

安全边界：
- 默认不调用外部 LLM。
- 默认不执行外部求解器。
- 不需要网络访问。
- 不声明生产级物理验证。
- 不声明形式化收敛证明。

前端可视化：
- Agent Studio 提供“子智能体协作”页面。
- 页面把每个子智能体显示为多智能体协作时间线。
- 示例库可以为内置光学设计案例生成对应的协作轨迹。
- 页面保持预览和验证边界可见。

Agent 命令中心：
- `POST /api/agent-session` 将同一组子智能体角色包装成面向自然语言目标的任务会话。
- 任务会话包含光学意图、选中的设计案例、计划步骤、本地产物、权限门控、最终建议和下一步建议。
- 权限门控默认阻断外部求解器、外部 LLM、上传、PyPI 发布、tag 和 release 动作。
