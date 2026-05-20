# 后端证据审查包

后端证据审查包是面向维护者的汇总文档，用来说明本地后端今天实际能证明什么。它是
preview/design-assist 审查产物，不是 production-grade / 生产级物理验证，不声明形式化收敛证明，也不会执行
外部求解器。

## 生成审查包

```bash
python scripts/generate_backend_evidence_pack.py \
  --json-out /tmp/osa-backend-evidence-pack.json \
  --markdown-out /tmp/osa-backend-evidence-pack.md
```

生成在 `/tmp` 下的 JSON/Markdown 只是审查产物，默认不提交。

## 冒烟检查

```bash
./scripts/smoke_backend_evidence_pack.sh
```

该脚本会确认生成的 JSON 和 Markdown 包含必要章节和安全标记。

## 审查决策

维护者审查决策记录在
[`backend_evidence_review_decision.md`](backend_evidence_review_decision.md)。
该决策说明后端证据已足以准备 `v0.9.0rc7` release draft。维护者随后已批准并完成
`v0.9.0rc7` GitHub prerelease；但 PyPI 发布、`0.9.0rc8.dev0` 的 TestPyPI 上传、
未来 `v0.9.0rc8` tag/release 工作以及 `v1.0.0` 发布批准仍保持分离，且尚未授权。

## 包含章节

- Package and release status：当前公开预发布版本、main 开发版本、PyPI/TestPyPI
  状态，以及没有 tag/release 动作。
- Sub-agent reality：每个确定性后端角色是否存在，并且是否在样例 session 中执行。
- Tool-call reality：已执行的内部工具、已执行的计算器工具，以及被阻止的外部动作。
- Optical calculators：薄膜、近轴、Gaussian beam、波导、光纤耦合和 Jones 偏振
  preview 计算器，以及 sanity reference cases 和 failure modes。光纤耦合覆盖
  perfect match、waist mismatch、offset loss 和 tilt loss；偏振覆盖线偏振态、
  Malus-like 偏振片投影、半波片旋转和四分之一波片相位。
- Design-case cross-checks：光学设计案例如何映射到预期计算器、适配器和 tool-call
  ledger。
- Source / monitor / observable diagnostics：确定性 source/monitor 推断、缺失输入诊断、
  observable taxonomy 和 adapter-native mapping。
- Adapter-native golden coverage：Meep、MPB、Gmsh、Elmer、Optiland 的 golden preview
  case，以及 metadata、fragment、safety 检查。
- Application-domain benchmarks：此前 fiber coupling 和 polarization 的 warning
  场景现在由确定性 preview 计算器覆盖，但真实耦合/矢量偏振验证仍需显式求解器或实验依据。
- Optional solver micro-benchmarks：manifest-backed 的微型开源 solver-backed
  检查规划，只能手动显式 opt-in。默认 evidence pack generation 不运行 solver。
- Optional solver readiness/approval：在任何 solver-backed micro-benchmark
  运行前记录 availability detection、预期 artifact、风险说明和明确批准语句。
  这不授权 PyPI、TestPyPI、tag 或 release 动作。
- Blocked or deferred capabilities：外部求解器、外部 LLM、发布、tag/release、Elmer
  Level 3、生产级验证、形式化收敛证明等被阻止或延后能力。
- Maintainer review questions：供维护者决定下一步审查或深化方向的问题。

## 如何解读状态

`pass` 表示本地确定性证据符合预期 preview contract。`warn` 表示能力有意保持部分实现或
延后。`fail` 表示本地证据检查与预期 contract 不一致。

## 限制

- 默认不执行外部求解器。
- Optional solver-backed micro-benchmarks 必须显式设置
  `OSA_RUN_OPTIONAL_*_VALIDATION=1`，且不属于默认 gate。
- Optional solver readiness 使用 `scripts/check_optional_solver_readiness.py`
  和 approval matrix/template；它不执行 solver。`OSA_SOLVER_PYTHON`
  可以把 import-only probe 指向 `osa-solvers` 等专用 solver Python。
- Optional solver execution approval packet、execution sequence 和
  per-solver pending/deferred records 只是 review aids；它们本身不授权 solver
  execution、PyPI/TestPyPI upload、tag 或 release。
- 2026-05-20 已批准并执行的 Gmsh-only run 只记录为可选手动 mesh generation
  smoke 证据，并已被 review 接受；该 run 未执行 Meep、MPB、Optiland 或 Elmer。
  2026-05-20 另一个单独批准的 Optiland-only run 只记录为可选手动 ray/path
  smoke 证据；Meep/MPB 需要 `OSA_SOLVER_PYTHON` 和单独批准；Elmer 仍
  deferred。
- 默认不调用外部 LLM。
- 不上传 TestPyPI/PyPI。
- 不创建 Git tag 或 GitHub release。
- adapter-native monitor metadata 只是 preview 元数据，不是真实 solver monitor result。
- 计算器输出是 sanity-checked preview/design-assist 结果，不是 production-grade / 生产级物理验证。

## 验证成熟度和 preview 边界

生成的 evidence pack 现在包含：

- `validation_maturity_summary`：对计算器、材料、应用域、adapter metadata、
  sub-agent session 和前端 UI/demo surface 的保守成熟度分级。
- `preview_boundary_summary`：说明每类证据证明什么，以及用户仍需自行验证什么。
- `optional_solver_micro_benchmarks`：记录可选手动 solver-backed micro-benchmark
  manifest、readiness/approval matrix availability、默认不执行 solver、明确批准要求，
  且不声称生产级验证。
- `validation_claim_audit_available`：记录
  `scripts/audit_validation_claims.py` 是后端证据 workflow 的一部分。

详见 [`backend_validation_maturity_matrix.zh-CN.md`](backend_validation_maturity_matrix.zh-CN.md)
和 [`preview_boundary_policy.zh-CN.md`](preview_boundary_policy.zh-CN.md)。
