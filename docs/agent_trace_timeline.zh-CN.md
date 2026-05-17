# 多智能体协作轨迹

多智能体协作轨迹让 Agent Studio 中的本地子智能体协作更直观。

API：
- `POST /api/agent-trace`
- `POST /api/examples/{example_id}/agent-trace`

时间线角色：
- SpecAgent：理解意图和缺失字段。
- MaterialAgent：从本地材料预览库推荐材料。
- GeometryAgent：识别几何类型和需要补充的几何字段。
- AdapterAgent：推荐开源求解器优先的适配器路径。
- WorkflowAgent：生成本地、默认不执行的工作流计划。
- EvidenceAgent：附加验证证据和成熟度说明。
- SafetyAgent：检查不夸大、不运行求解器、不调用 LLM、不上传、不创建 tag/release。
- RecommendationAgent：给出下一步建议。

每个时间线步骤显示：
- step_index
- stage
- input_summary
- output_summary
- diagnostics
- evidence_refs
- recommended_next_actions
- safety_notes

该轨迹是本地确定性预览，不是自主外部 agent 系统；默认不调用外部 LLM，不运行外部求解器，不声明生产级物理验证，也不声明形式化收敛证明。

Agent 命令中心通过 `POST /api/agent-session` 复用这条轨迹，并在其上增加自然语言目标、光学意图摘要、选中的设计案例、任务计划步骤、产物、权限门控和下一步建议。
