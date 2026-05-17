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
- 每一步包含 diagnostics、recommended next actions、confidence 和 evidence refs。

安全边界：
- 默认不调用外部 LLM。
- 默认不执行外部求解器。
- 不需要网络访问。
- 不声明生产级物理验证。
- 不声明形式化收敛证明。

前端可视化：
- Agent Studio 提供“子智能体协作”页面。
- 页面把每个子智能体显示为卡片/时间线。
- 页面保持预览和验证边界可见。
