# Agent Studio 中文术语表

## 术语

| English term | 中文术语 |
| --- | --- |
| spec | 规格 |
| parse | 本地解析 |
| validate | 验证规格 |
| adapter | 适配器 |
| adapter matrix | 适配器矩阵 |
| workflow plan | 工作流计划 |
| artifact preview | 适配器产物预览 |
| validation evidence | 验证证据 |
| readiness | readiness / 就绪状态 |
| external solver | 外部求解器 |
| external LLM | 外部 LLM |
| production-grade physical validation is not claimed | 生产级物理验证 |
| formal convergence proof is not claimed | 形式化收敛证明 |
| material library | 材料库 |
| material catalog | 材料目录 |
| example gallery | 示例库 |
| optical design examples | 光学设计示例 |
| sub-agent collaboration | 子智能体协作 |
| agent trace | agent trace / 协作轨迹 |
| agent trace timeline | 多智能体协作轨迹 |
| input summary | 输入摘要 |
| output summary | 输出摘要 |
| evidence refs | 证据引用 |
| final recommendation | 最终建议 |
| Agent Command Center | Agent 命令中心 |
| optical intent | 光学意图 |
| design case | 设计案例 |
| task plan | 任务计划 |
| permission gates | 权限门控 |
| artifacts | 产物 |

## 不翻译的内容

- API 字段名保持英文。
- API JSON keys 保持英文稳定。
- Adapter tool names are not translated.
- 工具名 `meep`, `gmsh`, `mpb`, `elmer`, `optiland` 不翻译。
- Package metadata 和 version strings 不翻译。
- 材料 ID 例如 `sio2`, `si`, `au`, `ag` 保持英文/化学式稳定。
- 子智能体名称 `SpecAgent`, `MaterialAgent`, `GeometryAgent`, `AdapterAgent`,
  `WorkflowAgent`, `EvidenceAgent`, `SafetyAgent`, `RecommendationAgent` 不翻译。

## 维护说明

- 中文 UI 文案可以继续打磨，但不能改变 API contract。
- `api_contract_version` 保持 `0.1`。
- 安全边界必须继续说明默认不执行外部求解器、默认不调用外部 LLM、不上传、不创建 tag/release、不声明生产级物理验证、不声明形式化收敛证明。
