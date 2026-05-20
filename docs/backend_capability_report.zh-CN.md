# 后端能力报告

Current public prerelease: v0.9.0rc7。Current main development version:
`0.9.0rc8.dev0`。

后端能力报告用于向维护者说明：当前本地 Agent Studio 后端到底能
import 什么、调用什么、执行了什么，以及默认阻断了什么。报告由
`scripts/generate_backend_capability_report.py` 生成，也可通过
`GET /api/backend-capability-report` 获取。

如果需要一个维护者审查包，把本报告、子智能体现实、tool-call reality、计算器证据、
设计案例交叉检查、source/monitor 诊断、adapter-native golden coverage 和被阻止的外部
动作汇总到一起，请使用
[`backend_evidence_review_pack.zh-CN.md`](backend_evidence_review_pack.zh-CN.md)。

## 报告证明什么

- package 版本为 `0.9.0rc8.dev0`；PyPI 未发布。
- 子智能体角色出现在真实的样例 `AgentTaskSession` trace 中。
- 内部工具是可 import、可调用、并记录在样例 `tool_call_ledger` 中的。
- 光学计算器是带参考 sanity case 的本地 preview/design-assist 工具，包括新增的
  光纤耦合和 Jones 偏振预览 helper。
- 光学设计示例会和 agent session、预期计算器调用、材料建议、适配器建议进行交叉检查。
- 外部 solver、外部 LLM、TestPyPI 上传、PyPI 发布、git tag、GitHub release
  默认不执行，或需要明确审批。

## 报告章节

1. `package`：包版本、公开候选版本、main 开发版本、TestPyPI 验证状态、PyPI 发布状态。
2. `sub_agents`：`SpecAgent`、`MaterialAgent`、`GeometryAgent`、
   `AdapterAgent`、`WorkflowAgent`、`EvidenceAgent`、`SafetyAgent`、
   `RecommendationAgent` 的执行现实。
3. `internal_tools`：材料库、示例注册表、agent trace builder、task session
   builder、adapter preview generator、workflow planner、光源/监测器推断、
   观测量诊断、适配器原生映射、adapter-native golden preview 检查、
   optical calculators。
4. `adapter_native_golden_coverage`：Meep、MPB、Gmsh、Elmer、Optiland 的
   adapter-native source/monitor golden preview 覆盖矩阵，包含严格 metadata
   diff 状态和 preview-only safety flags。
5. `optical_calculators`：thin-film、paraxial、Gaussian beam、waveguide、
   fiber coupling、polarization 预览计算器、API endpoint、参考 case、failure mode、
   `sanity_checked_preview` 质量级别。fiber coupling 现在包含 perfect match、
   waist mismatch、offset loss 和 tilt loss sanity cases；polarization 包含
   linear state、Malus-like polarizer、half-wave 和 quarter-wave Jones sanity cases。
6. `design_case_cross_checks`：每个光学设计示例的 pass/warning/fail 交叉检查。
7. `requirements_templates`：七个设计需求模板的中英文 goal、启发式匹配状态、
   预期工具、交叉检查状态和 preview-only 状态。
8. `optional_solver_micro_benchmarks`：manifest-backed 的可选 solver micro-benchmark
   规划；默认不执行 solver，必须显式 opt-in。
9. `blocked_external_actions`：solver、LLM、上传、发布、tag、release 默认不执行。

## 如何生成

```bash
python scripts/generate_backend_capability_report.py \
  --json-out /tmp/osa-backend-capability-report.json \
  --markdown-out /tmp/osa-backend-capability-report.md
```

烟测：

```bash
./scripts/smoke_backend_report.sh
```

维护者证据审查包：

```bash
python scripts/generate_backend_evidence_pack.py \
  --json-out /tmp/osa-backend-evidence-pack.json \
  --markdown-out /tmp/osa-backend-evidence-pack.md
./scripts/smoke_backend_evidence_pack.sh
```

也可以直接检查 adapter-native golden preview cases：

```bash
python scripts/check_adapter_native_golden.py
```

也可以在不运行 solver 的情况下检查 optional solver micro-benchmark planning：

```bash
python scripts/check_optional_solver_readiness.py
./scripts/run_optional_solver_micro_benchmarks.sh
```

readiness 脚本只检查 command/module availability，并且是 environment-aware：
默认使用当前 Python/当前 `PATH`；`OSA_SOLVER_PYTHON` 可以探测 `osa-solvers`
等专用 solver Python 中的 PyMeep 和 `meep.mpb`。只有显式设置
`OSA_RUN_OPTIONAL_*_VALIDATION=1` 后，才允许进入 solver-backed pilot 路径。
默认报告、默认 smoke 和默认质量门禁都不设置这些变量。审批矩阵和审批记录模板见
[`optional_solver_micro_benchmark_approval_matrix.zh-CN.md`](optional_solver_micro_benchmark_approval_matrix.zh-CN.md)
和
[`optional_solver_micro_benchmark_approval_record_template.zh-CN.md`](optional_solver_micro_benchmark_approval_record_template.zh-CN.md)。

覆盖矩阵也可以直接读取：

```bash
curl http://127.0.0.1:8000/api/adapter-native-golden-coverage
```

## 安全边界

- 内部工具现在包含光源/监测器推断、缺失输入诊断、观测量诊断和适配器原生
  光源/监测器映射。它们是本地 Python 调用，在 sample agent session 中会作为
  已执行的内部工具显示。
- Adapter-native golden cases 是针对本地 API 响应的 fixture 检查，包含严格
  metadata diff 和覆盖矩阵检查，但不是真实 solver monitor result。
- 默认不执行外部求解器。
- 默认不调用外部 LLM。
- 不执行上传。
- 不创建 tag。
- 不创建 release。
- 报告只作为 preview/design-assist 证据。
- 不声明生产级物理验证。
- 不声明形式化收敛证明。

## 验证成熟度

报告现在包含 `validation_maturity_summary`、`preview_boundary_summary`、
`optional_solver_micro_benchmarks` 和 `validation_claim_audit_available`。
这些字段链接到
[`backend_validation_maturity_matrix.zh-CN.md`](backend_validation_maturity_matrix.zh-CN.md)
和 [`preview_boundary_policy.zh-CN.md`](preview_boundary_policy.zh-CN.md)。
计算器证据仍是 `sanity_checked_preview`，应用域证据仍是
`benchmark_checked_preview`，adapter/source-monitor 证据仍是 fixture-guarded
preview metadata。

Optional solver-backed micro-benchmarks 见
[`solver_validation_micro_benchmarks.zh-CN.md`](solver_validation_micro_benchmarks.zh-CN.md)。
它们只能手动显式 opt-in，不属于默认 pytest/smoke/release gate，也不声明
生产级物理验证或形式化收敛证明。
readiness/approval 层新增
[`optional_solver_micro_benchmark_approval_matrix.zh-CN.md`](optional_solver_micro_benchmark_approval_matrix.zh-CN.md)、
[`optional_solver_micro_benchmark_approval_record_template.zh-CN.md`](optional_solver_micro_benchmark_approval_record_template.zh-CN.md)、
[`optional_solver_micro_benchmark_readiness_status.md`](optional_solver_micro_benchmark_readiness_status.md)、
[`optional_solver_environment_profiles.zh-CN.md`](optional_solver_environment_profiles.zh-CN.md)、
[`optional_solver_micro_benchmark_execution_packet.zh-CN.md`](optional_solver_micro_benchmark_execution_packet.zh-CN.md)、
[`optional_solver_execution_sequence.zh-CN.md`](optional_solver_execution_sequence.zh-CN.md)、
`optional_solver_approval_records/` 和 `scripts/check_optional_solver_readiness.py`；
它不授权 PyPI、TestPyPI、tag、release 或 solver execution 动作。
2026-05-20 已批准并执行的 Gmsh-only run 记录在
[`../validation/gmsh/gmsh_micro_benchmark_2026-05-20.md`](../validation/gmsh/gmsh_micro_benchmark_2026-05-20.md)，
并在
[`optional_solver_approval_records/gmsh_micro_benchmark_review_2026-05-20.md`](optional_solver_approval_records/gmsh_micro_benchmark_review_2026-05-20.md)
中被接受为可选手动 mesh-generation smoke 证据；该 run 未执行 Meep、MPB、
Optiland 或 Elmer，也不批准后续 solver 执行。另一个单独批准的
2026-05-20 Optiland-only run 记录在
[`../validation/optiland/optiland_micro_benchmark_2026-05-20.md`](../validation/optiland/optiland_micro_benchmark_2026-05-20.md)，
并在
[`optional_solver_approval_records/optiland_micro_benchmark_review_2026-05-20.md`](optional_solver_approval_records/optiland_micro_benchmark_review_2026-05-20.md)
中被接受为可选手动 ray/path smoke 证据；Meep、MPB 和 Elmer 仍未在这些任务中执行。

可通过 `GET /api/backend-validation-maturity` 或
`python scripts/audit_validation_claims.py` 检查这些边界。
