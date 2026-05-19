# 领域 Benchmark 结果策略

应用领域 benchmark 结果是 backend-readiness 信号，不是生产级验证。它帮助维护者
检查本地确定性匹配、材料/模板覆盖、计算器/adapter 预期、缺失输入诊断和安全边界
是否稳定。
该策略覆盖 positive/明确、ambiguous/歧义、underconstrained/输入不足、unsupported/不支持
以及 unsafe_or_blocked/需要阻断的场景类型。

## 如何理解结果

- `pass` 表示本地预览行为符合场景预期。
- `warn` 表示后端保持安全，但该领域仍是部分覆盖、延期或刻意保留输入不足状态。
- `fail` 表示预期的安全、匹配、诊断或工具调用行为发生变化，需要审查。

warning 是有价值的：它防止部分覆盖被误解为完整光学设计验证。例如 fiber coupling 和
polarization optics 可以作为规划领域出现，但专用物理计算器或求解器验证仍属于未来工作。

## 不支持和商业工具请求

完整 Zemax 优化、完整 Lumerical FDTD 执行、真实 solver monitor 结果、生产可用处方文件、
生产级物理验证或形式化收敛证明请求，默认会被阻断或延期。后端可以推荐本地预览替代路径，
但不会执行外部求解器，不会调用外部 LLM，不要求 proprietary solver，不上传包，不创建
tag，也不创建 release。

## 安全默认行为

当场景存在歧义或输入不足时，后端应提出问题并暴露缺失输入，而不是静默选择不安全路径。
当场景不受支持时，后端应记录 blocked actions，并保持
`external_solver_executed=false`、`external_llm_required=false`、
`production_grade_validation_claimed=false` 和
`formal_convergence_proof_claimed=false`。

## 范围限制

benchmark 结果是 preview/design-assist 证据。它不验证材料常数，不证明真实求解器结果，
也不意味着 Elmer Level 3 validation。PyPI 发布、TestPyPI 上传、tag 创建、GitHub
release 创建和 v1.0.0 发布仍需要独立维护者批准。
