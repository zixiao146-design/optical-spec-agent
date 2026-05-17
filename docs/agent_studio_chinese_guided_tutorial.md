# Agent Studio 中文手把手教程

## 1. 目的

这个教程帮助中文用户从零开始完成一次本地 Agent Studio 工作流：加载示例规格、本地解析、验证规格、查看适配器矩阵、生成工作流计划、预览适配器产物，并查看验证证据和下一步建议。

## 2. 当前状态

- Current public prerelease: v0.9.0rc6
- Current main development version: 0.9.0rc7.dev0
- PyPI 未发布
- TestPyPI 仅验证过 0.9.0rc6.dev0
- 本教程不运行外部求解器
- 本教程不调用外部 LLM
- 本教程不上传 PyPI/TestPyPI
- 本教程不创建 tag/release

## 3. 教程步骤

### 1. 打开 Agent Studio

- 用户操作：运行 quickstart demo 后，在浏览器打开 `http://127.0.0.1:5173`。
- 预期看到的结果：Agent Studio 首页加载，左侧有页面导航和语言切换。
- 使用的 API endpoint：`GET /api/health`
- 安全边界说明：这是本地页面，不上传包，不创建 tag/release。

### 2. 查看 readiness / 系统状态

- 用户操作：停留在 Dashboard / Readiness，或打开 System Status。
- 预期看到的结果：看到 API 已连接、`api_contract_version`、当前公开候选版本、main development version、PyPI 未发布。
- 使用的 API endpoint：`GET /api/readiness`, `GET /api/version`, `GET /api/health`
- 安全边界说明：readiness 只是状态展示，不执行外部求解器。

### 3. 加载中文纳米颗粒示例

- 用户操作：进入 Spec Input，点击“加载中文纳米颗粒示例”。
- 预期看到的结果：中文自然语言规格填入文本框，并提示“示例已加载。点击本地解析后才会调用 API。”
- 使用的 API endpoint：无，加载示例不会调用 API。
- 安全边界说明：示例加载不是 live validation，不调用外部 LLM。

### 4. 本地解析规格

- 用户操作：点击“本地解析”。
- 预期看到的结果：解析结果和 diagnostics 显示在页面中。
- 使用的 API endpoint：`POST /api/parse`
- 安全边界说明：默认使用本地解析路径，不调用外部 LLM。

### 5. 验证规格

- 用户操作：在验证区使用 fixture 或 spec JSON，点击“验证 JSON”。
- 预期看到的结果：看到 valid / invalid 状态、diagnostics 和下一步建议。
- 使用的 API endpoint：`POST /api/validate`
- 安全边界说明：验证检查 schema 和完整性，不代表生产级物理验证。

### 6. 查看适配器矩阵

- 用户操作：打开 Adapter Matrix。
- 预期看到的结果：看到 Gmsh、Meep、MPB、Optiland、Elmer 的状态和证据摘要。
- 使用的 API endpoint：`GET /api/adapters`, `GET /api/validation-evidence`
- 安全边界说明：适配器矩阵只显示 metadata 和证据摘要，不运行外部求解器。

### 7. 生成工作流计划

- 用户操作：打开 Workflow Plan，加载 workflow fixture 后点击“生成工作流计划”。
- 预期看到的结果：看到 workflow steps、diagnostics 和 no-execute preview 边界。
- 使用的 API endpoint：`POST /api/workflow-plan`
- 安全边界说明：工作流计划是本地同步预览，默认不执行 solver。

### 8. 预览适配器产物

- 用户操作：打开 Artifact Preview，选择 `gmsh`、`meep`、`mpb`、`elmer` 或 `optiland`，点击“生成预览”。
- 预期看到的结果：看到 preview content 或 artifact summary。
- 使用的 API endpoint：`POST /api/adapter-preview`
- 安全边界说明：预览产物不是生产级物理验证，默认不执行外部求解器。

### 9. 查看验证证据和下一步建议

- 用户操作：打开 Validation Evidence，再回到 Dashboard 查看 recommended next actions。
- 预期看到的结果：看到 Gmsh / Meep / MPB / Optiland Level 3，Elmer deferred，以及下一步建议。
- 使用的 API endpoint：`GET /api/validation-evidence`, `GET /api/readiness`
- 安全边界说明：不声明形式化收敛证明，不声明生产级物理验证。

## 4. 完成标准

用户完成后应该理解：

- Agent 如何理解规格
- Agent 如何验证规格
- Agent 如何选择适配器
- Agent 如何生成 workflow plan
- Agent 如何生成 preview artifact
- 哪些验证已完成
- 哪些不是生产级验证
- 下一步该做什么

## 5. 不做什么

- 不默认运行 solver
- 不默认调用外部 LLM
- 不上传 PyPI/TestPyPI
- 不创建 tag/release
- 不声明生产级物理验证
- 不声明形式化收敛证明

## 6. 光学设计扩展步骤

新增材料库和子智能体协作后，公开演示前的中文教程还应引导用户完成：

### 10. 查看材料库和材料建议

- 用户操作：打开“材料库”，搜索 `sio2` 或输入 `nanoparticle plasmonics` 获取材料建议。
- 预期看到的结果：看到本地预览材料、用途建议和“非生产级光学常数”提示。
- 使用的 API endpoint：`GET /api/materials`, `POST /api/materials/suggest`
- 安全边界说明：材料库是本地预览/设计辅助，不联网查询材料数据库，不代表生产级材料常数。

### 11. 查看子智能体协作轨迹

- 用户操作：打开“子智能体协作”，加载 nanoparticle agent trace。
- 预期看到的结果：看到 SpecAgent、MaterialAgent、GeometryAgent、AdapterAgent、WorkflowAgent、EvidenceAgent、SafetyAgent 和 RecommendationAgent 的贡献。
- 使用的 API endpoint：`POST /api/agent-trace`
- 安全边界说明：子智能体协作轨迹是本地确定性预览，不调用外部 LLM，也不运行求解器。
