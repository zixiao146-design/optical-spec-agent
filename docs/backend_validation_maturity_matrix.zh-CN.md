# 后端验证成熟度矩阵

本文档汇总 `0.9.0rc8.dev0` 后端证据级别。这里的成熟度是保守的
maintainer 视角：所有条目都是 preview/design-assist 证据，不声称生产级物理
验证，也不声称形式化收敛证明。

## 成熟度级别

| 级别 | 含义 |
| --- | --- |
| `documented_preview` | 行为和限制已有文档，但不是物理验证结果。 |
| `fixture_guarded_preview` | 用 fixture、API 形状或 metadata diff 检查守住行为。 |
| `sanity_checked_preview` | 本地解析计算器有参考 sanity case 和 failure-mode 测试。 |
| `benchmark_checked_preview` | 场景 benchmark 检查路由、诊断、缺失输入和阻断动作。 |
| `optional_manual_solver_validated` | 个别 adapter 可有手动 solver 验证，但默认不运行外部 solver。 |
| `production_grade_not_claimed` | 明确边界：当前不声称生产级验证。 |

## 当前矩阵

| 范围 | 组件 | 当前级别 | 证据 | 限制 |
| --- | --- | --- | --- | --- |
| 材料 | material library | `documented_preview` | provenance 文档和测试 | 用户必须自行验证常数；不是生产级 optical constants database。 |
| 需求 | design requirement templates | `fixture_guarded_preview` | 需求 fixture 和匹配测试 | 仅确定性 heuristic；歧义目标会生成问题。 |
| 需求 | natural-language to optical-language | `fixture_guarded_preview` | 歧义匹配和缺失输入测试 | 默认不调用外部 LLM；confidence 只是路由证据。 |
| 计算器 | thin-film | `sanity_checked_preview` | 单界面和 quarter-wave AR 参考 case | 仅 transfer-matrix preview。 |
| 计算器 | paraxial | `sanity_checked_preview` | thin-lens、ABCD 和 relay 参考 case | 仅一阶光学。 |
| 计算器 | Gaussian beam | `sanity_checked_preview` | Rayleigh range 和 beam-radius 参考 case | 仅标量 paraxial 模型。 |
| 计算器 | waveguide | `sanity_checked_preview` | V-number 和 sweep 参考 case | 仅 slab-waveguide 近似。 |
| 计算器 | fiber coupling | `sanity_checked_preview` | Gaussian overlap 参考 case | 仅标量 Gaussian mode-overlap 近似。 |
| 计算器 | polarization | `sanity_checked_preview` | Jones polarizer 和 waveplate 参考 case | 仅 Jones calculus preview。 |
| 光学语言 | source/monitor diagnostics | `fixture_guarded_preview` | source/monitor inference fixture 和测试 | monitor 记录只是 preview metadata。 |
| 光学语言 | observable diagnostics | `fixture_guarded_preview` | observable taxonomy fixture 和测试 | observable 匹配不是计算出的物理结果。 |
| Adapter | adapter-native source/monitor mapping | `fixture_guarded_preview` | adapter mapping fixture 和测试 | 真实 adapter 结果需要单独批准运行 solver。 |
| Adapter | adapter golden coverage | `fixture_guarded_preview` | golden case 和 strict metadata diff | metadata 检查不是 solver monitor 输出。 |
| 可选 solver 验证 | Gmsh/Meep/MPB/Optiland micro-benchmark plan | 已记录 pilot 为 `optional_manual_solver_validated` | `validation/solver_validation_micro_benchmarks.json`、已有 2026-05-14 手动报告、2026-05-20 Gmsh-only evidence record 和 `scripts/run_optional_solver_micro_benchmarks.sh` | 仅显式 opt-in；默认 pytest、smoke、quality gates 和 release gates 不运行 solver。Gmsh 证据只是 mesh path smoke，不证明光学正确性。 |
| 可选 solver 验证 | Elmer micro-benchmark plan | `documented_preview` / deferred | `validation/elmer/elmer_install_deferred_2026-05-15.md` 和 Elmer optional pilot 文档 | Elmer 仍是 Level 2 + Level-3-ready；不声称 Level 3。 |
| 应用域 | domain benchmarks | `benchmark_checked_preview` | 19 pass / 0 warn / 0 fail 场景集 | benchmark 检查确定性行为，不证明物理正确性。 |
| Agent | sub-agent task sessions | `fixture_guarded_preview` | audit 脚本和 tool-call ledger 测试 | 角色是本地确定性后端角色。 |
| Agent | tool-call ledger | `fixture_guarded_preview` | ledger 测试和 evidence pack | ledger 记录本地工具调用和被阻断的外部动作。 |
| 前端 | Agent Studio | `documented_preview` | UI smoke 和文档 | 只是 UI/demo surface，不是验证证据。 |

## 不声称的内容

- 不声称生产级物理验证。
- 不声称形式化收敛证明。
- 默认不声称真实 solver monitor result。
- 默认不执行外部 solver。
- Optional solver-backed micro-benchmarks 必须显式设置 opt-in 环境变量，且不属于默认 pytest、smoke、quality gates 或 release gates。
- Optional solver readiness 现在可通过
  [`optional_solver_micro_benchmark_approval_matrix.zh-CN.md`](optional_solver_micro_benchmark_approval_matrix.zh-CN.md)、
  [`optional_solver_micro_benchmark_approval_record_template.zh-CN.md`](optional_solver_micro_benchmark_approval_record_template.zh-CN.md)、
  [`optional_solver_micro_benchmark_execution_packet.zh-CN.md`](optional_solver_micro_benchmark_execution_packet.zh-CN.md)
  和 [`optional_solver_execution_sequence.zh-CN.md`](optional_solver_execution_sequence.zh-CN.md)
  和 `scripts/check_optional_solver_readiness.py` 审查；该 readiness 层默认仍不执行 solver。
- Solver readiness 与 profile/环境相关。`OSA_SOLVER_PYTHON` 可以把 import probe
  指向 `osa-solvers` 等专用 solver Python；Gmsh 等 CLI 工具仍从当前 `PATH`
  探测。见 [`optional_solver_environment_profiles.zh-CN.md`](optional_solver_environment_profiles.zh-CN.md)。
- 默认不需要外部 LLM。
- Elmer 仍是 Level 2 + Level-3-ready；Level 3 deferred。

运行：

```bash
python scripts/audit_validation_claims.py
```

该审计会阻断不安全的验证声称，同时允许明确否定形式。
