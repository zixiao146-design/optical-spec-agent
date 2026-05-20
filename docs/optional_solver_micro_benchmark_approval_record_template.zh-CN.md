# Optional Solver Micro-benchmark Approval Record Template

在运行任何可选 solver-backed micro-benchmark 之前使用本模板。填写本模板不代表批准
PyPI/TestPyPI 发布、tag 创建、GitHub release 创建或 `v1.0.0` 发布。

维护中的执行审批包见
[`optional_solver_micro_benchmark_execution_packet.zh-CN.md`](optional_solver_micro_benchmark_execution_packet.zh-CN.md)。
当前 pending/deferred records 位于
[`optional_solver_approval_records/`](optional_solver_approval_records/)。
请按 [`optional_solver_execution_sequence.zh-CN.md`](optional_solver_execution_sequence.zh-CN.md)
一次只运行一个 solver。

## 选择的 Solver

- Solver:
- Adapter:
- 本地环境 / 版本说明:
- 已审查的可用性检查:

## 必需批准语句

维护者批准语句必须是：

> I approve running the optional <solver> micro-benchmark for optical-spec-agent.

实际批准记录必须把 `<solver>` 替换为被选中的 solver。

## 明确未批准

- PyPI publication: not approved.
- TestPyPI upload: not approved.
- Tag or GitHub release creation: not approved.
- `v1.0.0` release: not approved.
- Production-grade physical validation claim: not approved.
- Formal convergence proof claim: not approved.

## 预期命令

批准后只设置被选中 solver 的 env var，例如：

```bash
OSA_RUN_OPTIONAL_<SOLVER>_VALIDATION=1 ./scripts/run_optional_solver_micro_benchmarks.sh
```

不要设置无关的 opt-in env vars。

## 预期输出

- `/tmp/osa-*-validation/` 下的 solver-specific report JSON。
- `validation/solver_validation_micro_benchmarks.json` 中列出的 solver input/output artifact。
- 显示 no upload、no tag、no release actions 的安全标记。

## 清理说明

- 不再需要时审查并删除临时 `/tmp/osa-*-validation/` 文件。
- 默认不要提交 solver 输出 artifact。
- 缺失 solver install 不阻塞默认开发。
