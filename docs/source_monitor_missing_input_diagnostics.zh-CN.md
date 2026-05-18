# 光源/监测器缺失输入诊断

本文档说明后端如何报告光源、监测器和观测量的缺失输入。

## 必要输入

不同 requirement template 的必要输入不同，常见字段包括：

- 光源类型
- 波长或波长范围
- 偏振
- 入射方向
- 光腰或模式编号
- 监测观测量
- 监测区域
- 波长/频率采样

## 默认假设

后端会显式记录默认假设。例如：

- 纳米颗粒散射默认使用法向入射的平面波式光源。
- 纳米颗粒散射默认 400-900 nm 预览波段。
- 纳米颗粒散射默认 `linear_x` 偏振。
- 薄膜镀膜默认法向入射和反射/透射监测器。
- 高斯光束聚焦默认使用近轴标量公式。

这些默认值只表示可以安全预览，不表示可以安全运行外部求解器。

## 诊断输出

`OpticalLanguageDiagnostics` 报告：

- `missing_required_inputs`
- `default_assumptions_applied`
- `ambiguity_notes`
- `blocking_questions`
- `safe_to_preview`
- `safe_to_run_solver`

`safe_to_preview` 可以为 true，同时 `safe_to_run_solver` 仍为 false。

## API

- `POST /api/optical-language/infer`
- `POST /api/optical-language/diagnose`
- `POST /api/agent-session`

Agent session 也会记录工具调用：

- `optical_language.infer_source_monitor`
- `optical_language.diagnose_missing_inputs`

## 安全边界

默认不执行外部求解器。默认不调用外部 LLM。不联网查询材料数据库。
诊断输出是 preview/design-assist，不声明生产级物理验证，也不声明形式化收敛证明。
