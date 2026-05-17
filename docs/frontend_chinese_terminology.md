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

## 不翻译的内容

- API 字段名保持英文。
- API JSON keys 保持英文稳定。
- Adapter tool names are not translated.
- 工具名 `meep`, `gmsh`, `mpb`, `elmer`, `optiland` 不翻译。
- Package metadata 和 version strings 不翻译。

## 维护说明

- 中文 UI 文案可以继续打磨，但不能改变 API contract。
- `api_contract_version` 保持 `0.1`。
- 安全边界必须继续说明默认不执行外部求解器、默认不调用外部 LLM、不上传、不创建 tag/release、不声明生产级物理验证、不声明形式化收敛证明。
