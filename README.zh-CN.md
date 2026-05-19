# optical-spec-agent

[English](README.md) | [简体中文](README.zh-CN.md)

> 开源仿真工具链优先的光学仿真工作流 agent：将中英文光学仿真需求编译为
> 经过校验的 OpticalSpec JSON，并生成 solver-native input scaffold。

## 项目定位

**optical-spec-agent** 是一个开源仿真工具链优先的光学仿真工作流 agent，
也是一个连接“自然语言光学仿真需求”和“可执行光学
求解器输入”的规格编译层。用户可以用中文或英文描述仿真任务，项目会生成
结构化、经过校验的 OpticalSpec JSON，并可进一步生成 Meep 脚本或
MPB/Gmsh/Elmer/Optiland 的 solver-native input scaffold。

它不是求解器。默认情况下，它生成 spec、脚本、adapter scaffold、诊断报告和
workflow artifact；它不会默认运行外部 solver，也不提供 production-grade
physical validation。

默认 quickstart 不要求 Zemax、Lumerical、COMSOL 或 proprietary Ansys tools。
外部 solver 是可选项，默认不运行；外部 LLM 也是可选项，默认不需要。
PyPI 仍未发布；TestPyPI 已上传并验证 `0.9.0rc6.dev0`。

## Quickstart

面向第一次使用的本地 Agent Studio walkthrough 见
`docs/quickstart.zh-CN.md`：

```bash
./scripts/bootstrap_demo_env.sh
source /tmp/osa-agent-studio-demo/bin/activate
./scripts/run_quickstart_demo.sh
```

Quickstart 会打开 Agent Studio `http://127.0.0.1:5173` 和 Local Agent API docs
`http://127.0.0.1:8000/docs`，并引导用户完成 Load example spec、Parse locally、
Validate、View adapter matrix、Generate workflow plan、Preview artifact、Review
validation evidence 和 Readiness / next actions。它保持 local-first、preview-first：
不上传、不发布、不创建 tag/release、不默认执行 solver、不默认调用外部 LLM、不声称
production-grade physical validation，也不声称 formal convergence proof。

Agent Studio 前端支持 English / 中文界面切换；中文环境会默认显示中文，也可以在
侧边栏手动切换。中文 guided demo、中文安全边界和中文 quickstart prompt 见
`docs/frontend_i18n_zh_CN.md` 与
`examples/quickstart/zh_nanoparticle_prompt.txt`。中文手把手教程见
`docs/agent_studio_chinese_guided_tutorial.md`，中文术语表见
`docs/frontend_chinese_terminology.md`。API JSON 字段名、adapter tool names 和
`api_contract_version` 保持英文稳定。

当前光学设计方向扩展加入了 `docs/example_gallery.zh-CN.md` 示例库、
本地预览 `docs/material_library.zh-CN.md` 材料库、`examples/optical_design/`
光学设计示例，以及 `docs/agent_trace_timeline.zh-CN.md` 多智能体协作轨迹 /
`docs/sub_agent_architecture.zh-CN.md` 子智能体协作架构。Agent Studio 中可以看到 SpecAgent、MaterialAgent、
GeometryAgent、AdapterAgent、WorkflowAgent、EvidenceAgent、SafetyAgent 和
RecommendationAgent 的协作贡献。新增 `docs/agent_command_center.zh-CN.md`
Agent 命令中心会把自然语言光学设计目标转换成确定性的本地任务会话：光学意图、设计案例、agent 计划、权限门控、产物、证据和下一步建议。后端现在还记录
`docs/tool_call_reality_matrix.md` tool-call reality matrix、
`docs/backend_functionality_status.md` 后端能力状态、
`docs/backend_capability_report.zh-CN.md` 后端能力报告、
`docs/backend_evidence_review_pack.zh-CN.md` 后端证据审查包、
`docs/backend_validation_maturity_matrix.zh-CN.md` 后端验证成熟度矩阵、
`docs/preview_boundary_policy.zh-CN.md` preview 边界策略、
`docs/solver_validation_micro_benchmarks.zh-CN.md` 可选 solver-backed micro-benchmark 规划、
`docs/design_case_cross_checks.zh-CN.md` 设计案例交叉检查，并加入
`docs/optical_calculators.zh-CN.md` 本地光学预览计算器：薄膜叠层、近轴透镜、高斯光束、
波导 V-number、光纤耦合 mode overlap 和 Jones 偏振预览。
计算器层现在还包含面向案例的薄膜光谱、四分之一波长 AR、高斯光束序列/聚焦、
近轴系统/双透镜 relay、波导厚度扫描/单模范围，以及
`docs/fiber_coupling_preview_calculator.zh-CN.md` 光纤耦合和
`docs/polarization_preview_calculator.zh-CN.md` 偏振预览 helper，见
`docs/optical_calculator_case_integration.zh-CN.md`。参考 sanity cases 和响应
quality 字段见 `docs/optical_calculator_reference_cases.zh-CN.md`，其中
`docs/fiber_polarization_reference_cases.zh-CN.md` 专门记录光纤耦合和 Jones 偏振
sanity checks。这些计算器只用于
design-assist 预览，不运行外部求解器、不调用外部 LLM，也不声明生产级验证。
后端能力报告会说明哪些子智能体和内部工具在样例 session 中实际执行，
哪些计算器只是 sanity-checked preview，以及哪些外部 solver/LLM/upload/tag/release
动作仍被默认阻断。
验证成熟度矩阵会把计算器、材料、应用域、adapter metadata、sub-agent session 和
前端 UI/demo surface 分级，但不会把任何条目升级为生产级物理验证或形式化收敛证明。
可选 solver-backed micro-benchmark 规划提供微型开源 solver 检查的手动路径，但
`scripts/run_optional_solver_micro_benchmarks.sh` 默认不执行 solver，只有显式设置
`OSA_RUN_OPTIONAL_*_VALIDATION=1` 并获得批准后才进入 solver-backed run。
证据审查包可以通过
`python scripts/generate_backend_evidence_pack.py --json-out /tmp/osa-backend-evidence-pack.json --markdown-out /tmp/osa-backend-evidence-pack.md`
生成，也可以用 `./scripts/smoke_backend_evidence_pack.sh` 冒烟检查；它只是维护者审查产物，
不是 release、upload、tag 或发布动作。
维护者 `docs/backend_evidence_review_decision.md` 决策记录说明：后端证据已足以支撑
`v0.9.0rc7` release draft，且 `v0.9.0rc7` 已发布为当前 GitHub prerelease。
PyPI 发布、`0.9.0rc8.dev0` 的 TestPyPI 上传、未来 `v0.9.0rc8` tag 以及
`v1.0.0` 批准仍保持分离，且尚未授权。
后端还加入 `docs/design_requirement_templates.zh-CN.md` 设计需求模板和
`docs/natural_language_to_optical_language.zh-CN.md` 自然语言到光学语言映射层。
这些确定性模板把首次使用的自然语言目标连接到光学意图、必需输入、默认假设、
材料/几何选择、预期计算器或适配器、工具调用账本和预览产物，不使用外部 LLM。
rc8.dev0 后端进一步把材料溯源和歧义需求处理显式化：见
`docs/material_provenance_policy.zh-CN.md`、`docs/ambiguous_requirement_matching.zh-CN.md`
和 `docs/missing_input_diagnostics.zh-CN.md`。材料记录会暴露 provenance、
适用性 warning 和用户验证标记；有歧义的自然语言目标会返回候选模板和追问，
而不是直接采取不安全的求解器动作。材料库仍然只是 preview/design-assist，
不是生产级光学常数数据库。
后端还新增 `docs/application_domain_registry.zh-CN.md` 应用领域注册表和
`docs/material_template_cross_checks.zh-CN.md` 材料-模板交叉检查，把十个光学领域
连接到本地材料、需求模板、计算器/适配器、缺失输入问题和 preview-only 证据边界。
这些领域现在还通过 `docs/application_domain_benchmarks.zh-CN.md` 应用领域
benchmark 场景集进行检查，覆盖明确、歧义、输入不足、不支持和需要阻断的光学设计请求。
evaluator 会检查预期 domain/template 匹配、材料/计算器/adapter 行为、缺失输入问题和
阻断动作，同时不运行求解器、不调用外部 LLM。此前 fiber coupling 和 polarization
warning 场景现在通过确定性 preview 计算器变为通过；真实耦合验证和矢量电磁偏振验证
仍不属于默认后端路径。
Adapter-native golden preview cases 位于 `examples/adapter_native_golden/`，
文档见 `docs/adapter_native_golden_cases.zh-CN.md`。它们会检查 Meep、MPB、
Gmsh、Elmer 和 Optiland 的 source/monitor/observable fragments 以及严格
expected metadata 是否和本地 API 响应一致，但不运行求解器。覆盖矩阵见
`docs/adapter_native_golden_coverage_matrix.zh-CN.md`，也可通过
`GET /api/adapter-native-golden-coverage` 读取。
示例库会把示例、材料建议、适配器推荐、工作流计划、产物预览、验证证据和下一步建议串起来。这些能力仍保持 preview-first：默认不执行外部
solver、默认不调用外部 LLM、材料值不是生产级光学常数，也不会提供
PyPI/TestPyPI 上传或 GitHub tag/release 控制。

核心主线：

```text
自然语言需求
  -> parser: rule / llm / hybrid
  -> OpticalSpec JSON
  -> validation
  -> adapter-generate / meep-generate
  -> solver-native input scaffold
  -> optional Meep local execution
  -> diagnose / workflow report / replay / human review checklist
```

## 发布状态

当前公开 release candidate 是 `v0.9.0rc7`。当前 `main` 的 development version 是
`0.9.0rc8.dev0`。`v0.9.0rc8` tag 和 GitHub release 尚未创建；`0.9.0rc8.dev0`
不是公开 release，也不是 final stable `1.0`。

`v0.6` 到 `v0.9` 的能力属于 preview/scaffold/evaluation capabilities：

- `v0.6`: 本地 post-hoc physical diagnostics。
- `v0.7`: 多求解器 adapter MVP scaffold。
- `v0.8`: LLM parser foundation，默认使用 deterministic mock provider。
- `v0.9`: 本地同步 workflow orchestration。

`v0.9.0rc7` tag 和 GitHub prerelease 已由维护者确认后创建，并作为当前
release candidate supersede `v0.9.0rc6`。不要移动 `v0.9.0rc1`、`v0.9.0rc2`、
`v0.9.0rc3`、`v0.9.0rc4`、`v0.9.0rc5`、`v0.9.0rc6` 或 `v0.9.0rc7` tag。未来 post-release fix 应使用新的 RC tag。PyPI 仍未发布；
TestPyPI 已通过手动 Trusted Publishing 上传 `0.9.0rc6.dev0`，但 `0.9.0rc8.dev0`
尚未上传到 TestPyPI；这不授权正式 PyPI 发布。

面向 `v1.0` 的公共契约边界见：
`docs/cli_contract.md`、`docs/schema_contract.md`、
`docs/adapter_support_matrix.md`、`docs/workflow_preview_contract.md`、
`docs/validation_boundary.md`、`docs/validation_gate.md`、`docs/packaging_gate.md`、
`docs/open_source_solver_strategy.md`、`docs/proprietary_solver_policy.md`、
`docs/external_solver_policy.md`、`docs/external_llm_policy.md` 和
`docs/pypi_publication_decision.md`。PyPI 发布仍是 not granted，见
`docs/publication_decision_record.md`；TestPyPI 成功状态不授权正式 PyPI 发布。
rc8.dev0 后端路线和能力差距审计见：
`docs/rc8_backend_roadmap.md`、`docs/rc8_capability_gap_audit.md` 和
`docs/rc8_to_v1_0_decision_path.md`。这些文档用于继续 v1.0 readiness/backend
engineering，不准备 `v0.9.0rc8` release draft，不授权 PyPI/TestPyPI 上传，
不创建 tag/release，也不提供 production-grade physical validation 或 formal
convergence proof。
v1.0 public contract freeze 已获 maintainer approval，并记录在：
`docs/v1_0_public_contract_freeze_status.md`。freeze package 包括：
`docs/v1_0_public_contract_freeze_confirmation.md`、
`docs/v1_0_contract_frozen_surface.md`、
`docs/v1_0_contract_non_goals.md` 和
`docs/v1_0_breaking_change_policy.md`。该 freeze 不授权 PyPI 发布、tag 创建、
GitHub release 创建或 `v1.0.0` 发布。
v1.0 compatibility 和 evidence 跟踪见 `docs/v1_0_compatibility_policy.md`、
`docs/validation_evidence_manifest.md`、`docs/adapter_maturity_model.md`、
`docs/open_source_solver_validation_plan.md`、`docs/open_solver_validation_harness.md`、
`docs/gmsh_optional_validation_pilot.md`、
`docs/gmsh_level3_readiness.md`、
`validation/gmsh/gmsh_validation_pilot_2026-05-14.md`、
`docs/meep_optional_validation_pilot.md`、
`docs/meep_level3_readiness.md`、
`validation/meep/meep_validation_pilot_2026-05-14.md`、
`docs/mpb_optional_validation_pilot.md`、
`docs/mpb_level3_readiness.md`、
`validation/mpb/mpb_validation_pilot_2026-05-14.md`、
`docs/optiland_optional_validation_pilot.md`、
`docs/optiland_level3_readiness.md`、
`validation/optiland/optiland_validation_pilot_2026-05-14.md`、
`docs/elmer_optional_validation_pilot.md`、
`docs/elmer_level3_readiness.md`、
`validation/elmer/elmer_install_deferred_2026-05-15.md`、
`docs/manual_solver_validation_report_template.md`、`docs/pytest_marker_policy.md`、
`docs/offline_user_journey.md`、`docs/error_model.md`、
`docs/migration_notes_pre_v1.md`、`docs/v1_0_public_contract_freeze.md`、
`docs/v1_0_public_contract_freeze_checklist.md`、
`docs/public_contract_manifest.json`、`docs/public_contract_change_checklist.md`、
`examples/e2e/README.md` 和 `examples/examples_manifest.json`。
当前 rc7 release draft readiness 和发布 gate 见 `docs/release_readiness_v0.9.0rc7.md`、
`docs/testpypi_upload_approval_v0.9.0rc7.md`，以及历史 rc6 release 记录：
`docs/release_readiness_v0.9.0rc6.md`、
`docs/github_release_draft_v0.9.0rc6.md`、`docs/release_notes_v0.9.0rc6.md`、
`docs/testpypi_upload_approval_v0.9.0rc6.md`、
`docs/post_release_status_v0.9.0rc6.md`、
`docs/rc6_development_plan.md`、`docs/v1_0_gap_audit.md`、
`docs/v1_0_decision_matrix.md`、`docs/testpypi_upload_attempt_v0.9.0rc6.dev0.md`、
`docs/testpypi_status_v0.9.0rc6.dev0.md`、
`docs/testpypi_trusted_publishing.md`、
`docs/testpypi_dry_run_gate.md` 和
`docs/v1_0_stability_gate.md`。
PyPI publication readiness 与发布后验证计划见
`docs/pypi_publication_readiness_checklist.md` 和
`docs/pypi_post_publication_verification_plan.md`；当前建议仍是不发布 PyPI。
v1.0.0 planning package 见 `docs/v1_0_release_criteria.md`、
`docs/v1_0_release_plan.md`、`docs/rc_to_v1_0_transition_path.md`、
`docs/v1_0_pypi_decision_gate.md`、
`docs/v1_0_post_release_verification_plan.md` 和
`docs/agent_studio_frontend_roadmap.md`。Agent Studio frontend/API roadmap
包含当前本地 MVP 与后续 Phase 2 规划，不是 v1.0.0 release blocker。
Local Agent API readiness 见 `docs/api_agent_contract.md` 和
`docs/cli_api_parity.md`。该 API 为未来 Agent Studio frontend 暴露
health/version、adapter registry、schema、parse、validate、workflow-plan、
adapter-preview、validation evidence 和 readiness/status；本地 frontend MVP
已在 `frontend/` 中实现。
API 默认仍不运行外部 solver、不调用外部 LLM、不依赖 proprietary solver、
不要求网络、不声称 production-grade physical validation，也不声称 formal
convergence proof。
API response models 定义在 `src/optical_spec_agent/api/models.py`，稳定错误模型
见 `docs/api_error_model.md`，API versioning 见
`docs/api_versioning_policy.md`，request validation contract 见
`docs/api_request_validation_contract.md`，frontend fixture examples 位于
`examples/api/`。本地启动指南、frontend handoff spec 和可复制的 curl 示例见
`docs/api_local_launch_guide.md`、`docs/frontend_handoff_spec.md` 和
`docs/api_curl_examples.md`；API smoke 与 fixture consistency 检查脚本为
`scripts/smoke_agent_api.sh` 和 `scripts/check_api_fixtures.py`。Agent Studio
frontend MVP planning package 见 `docs/frontend_mvp_product_spec.md`、
`docs/frontend_information_architecture.md`、`docs/frontend_api_mapping.md`、
`docs/frontend_mvp_user_flows.md`、
`docs/frontend_mvp_acceptance_criteria.md`、`docs/frontend_safety_policy.md`
和 `docs/frontend_mvp_implementation_plan.md`。Agent Studio frontend MVP 已在
`frontend/` 中实现为本地 React + Vite + TypeScript app，运行说明见
`docs/frontend_mvp_runbook.md`，本地 demo QA checklist 见
`docs/frontend_mvp_qa_checklist.md`。交互加固包括 fixture loading 按钮、API
mode indicator、diagnostics panel、recommended next actions 和可折叠 JSON
payload；Playwright visual smoke 为手动/可选检查，见
`docs/frontend_visual_smoke_plan.md`、`docs/frontend_visual_smoke_runbook.md`
和 `scripts/smoke_frontend_visual.sh`，不属于默认 release gate。本地 maintainer
demo package 见 `docs/agent_studio_demo_runbook.md`、
`docs/agent_studio_demo_checklist.md`、`docs/agent_studio_demo_storyboard.md`、
`docs/agent_studio_demo_troubleshooting.md` 和 `scripts/demo_agent_studio.sh`；
它把 API 启动、frontend 启动、smoke checks、可选 visual smoke 和 guided
walkthrough 串在一起，但不上传、不创建 tag/release、不运行 solver、不调用外部 LLM。
本地 demo review 与后续 hardening backlog 见
`docs/agent_studio_demo_feedback.md` 和 `docs/frontend_hardening_backlog.md`。
Quickstart onboarding 见 `docs/quickstart.md` 和 `docs/quickstart.zh-CN.md`，
对应脚本为 `scripts/bootstrap_demo_env.sh` 和 `scripts/run_quickstart_demo.sh`。
中文本地化状态见 `docs/frontend_i18n_zh_CN.md`；中文手把手教程和术语表见
`docs/agent_studio_chinese_guided_tutorial.md` 与
`docs/frontend_chinese_terminology.md`。
它使用 Local Agent API，默认 API base 为
`http://127.0.0.1:8000`，不提供 upload、publish、tag、release、solver-run、
external LLM、login、cloud 或 production deployment 控件。API 断开时 UI 会进入
明确标注的 demo fixture mode；demo mode 不是 live validation。frontend smoke
脚本为 `scripts/smoke_frontend_mvp.sh`。当前
`api_contract_version` 为 0.1。该 API 仍是 frontend-readiness / candidate API，
不是单独冻结的 v1.0 API contract。这项 API/frontend 工作不触发 PyPI 发布，也不
改变当前版本或 release 状态。
一键本地质量门禁、文档地图、v1.0 readiness scorecard 和 maintainer decision
log 见 `docs/quality_gates.md`、`docs/README.md`、
`docs/v1_0_readiness_scorecard.md` 和 `docs/maintainer_decision_log.md`。
CI/local gate parity、release dry-run、secrets/token hygiene 和 maintainer
operations checklist 见 `docs/ci_quality_gate_parity.md`、
`docs/release_dry_run_operations.md`、`docs/secrets_and_token_hygiene.md` 和
`docs/maintainer_operations_checklist.md`。
`ci.yml` 是自动 push/PR gate；benchmark 和 extended-test workflows 仅手动运行。
release dry-run 与 TestPyPI Trusted Publishing 也仅手动运行，默认 CI 不会发布、
上传、创建 tag 或创建 release。
本地 package publication preflight 脚本为 `scripts/testpypi_preflight.sh`；
它只做 build、metadata、wheel install 和 CLI 检查，不上传任何 artifact。

## 快速概览

| 能力 | 当前状态 |
|---|---|
| 自然语言解析 | 支持中英文 rule-based parser，默认 parser 为 `rule` |
| OpticalSpec | Pydantic v2 model、schema、validation、missing field tracking |
| Provenance | 字段级 confirmed / inferred / missing 状态和 derivation note |
| Meep | 生成 preview / research-preview / smoke 脚本 |
| Meep execution | 可选本地 harness，仅在显式 `meep-run` 时运行 |
| v0.6 diagnostics | `diagnose` 生成 mesh/flux/execution/preview artifact |
| v0.7 adapter | `adapter-list` / `adapter-generate`，生成多求解器 scaffold |
| v0.8 LLM parser | provider-agnostic foundation + deterministic mock provider |
| v0.9 workflow | `workflow-plan` / `workflow-run` / `workflow-replay` / `workflow-report` |
| Release engineering | tests、benchmarks、docs/CLI/release/artifact checks、build dry-run |

## 为什么需要这个项目

光学仿真任务通常包含几何、材料、源、边界条件、网格、sweep、监视器和后处理
等多层信息。人类自然语言描述往往不完整，而 solver 输入需要严格结构化。

optical-spec-agent 的目标是成为中间的“规格编译器”：

- 输入：自然语言光学仿真需求。
- 输出：结构化 OpticalSpec JSON。
- 约束：每个关键字段都有状态、来源和缺失提示。
- 下游：可生成 Meep 脚本、多求解器 scaffold、诊断报告和 workflow run。

## 当前能力范围

当前 release candidate 覆盖的是工程化链路，而不是物理结果证明：

- 可以把自然语言任务转换成 OpticalSpec。
- 可以验证 spec 是否缺少关键字段。
- 可以生成 solver-native input scaffold。
- 可以进行 post-hoc diagnostics。
- 可以用 deterministic mock provider 评估 LLM parser foundation。
- 可以把 parse / validate / generate / diagnose / report 串成同步 workflow。

但它不证明仿真物理正确，不证明收敛，不替代人工建模审查。

## 已实现能力

- 中英文关键词与正则规则解析。
- Pydantic v2 validation。
- Provenance tracking：confirmed / inferred / missing。
- Meep script generation。
- optional Meep execution harness。
- `diagnose` physical diagnostics。
- `adapter-list` / `adapter-generate`。
- MPB / Gmsh / Elmer / Optiland MVP scaffold。
- LLM parser foundation with mock provider。
- Conservative hybrid parser。
- `llm-eval` benchmark。
- `workflow-plan` / `workflow-run` / `workflow-replay` / `workflow-report`。
- Release engineering checks。

## 尚未完成 / 明确限制

- 不是 solver。
- 不提供 production-grade physical validation。
- 不提供 formal convergence proof。
- 不默认运行外部 solver。
- 不默认调用外部 LLM。
- external solver / external LLM 都是可选项，默认测试不需要它们。
- adapter outputs 是 MVP/scaffold，不是 production-ready solver input。
- workflow 是本地同步编排，不是 autonomous cloud execution。
- Meep physical candidate 仍需要人工诊断和收敛研究。
- LLM parser 只抽取 candidate spec，不解释 solver result，也不验证物理正确性。
- Optiland 支持是 scaffold-level，因为当前 OpticalSpec 没有完整 sequential lens prescription。
- Gmsh/Elmer 需要更丰富的 FEM geometry/material/boundary schema 才能进入生产使用。

## 安装

```bash
git clone https://github.com/zixiao146-design/optical-spec-agent.git
cd optical-spec-agent
pip install -e ".[dev]"
```

需要 Python 3.11+。

## 快速开始

## 离线示例

完整的无网络、无外部 solver、无外部 LLM、无 proprietary solver 默认依赖的
端到端路径见 `docs/offline_user_journey.md` 和 `examples/e2e/README.md`。

`examples/` 目录中的 fixture 是当前 `0.9.0rc8.dev0` main 和公开
`v0.9.0rc7` RC 线的本地示例证据：

```bash
optical-spec validate examples/specs/minimal_nanoparticle.json
optical-spec parse examples/specs/minimal_nanoparticle.json --json
optical-spec workflow-plan examples/workflows/local_preview_request.json --json
```

这些命令不需要网络，不运行外部 solver，不调用外部 LLM，也不上传
PyPI/TestPyPI artifact。

```bash
optical-spec parse \
  "用 Meep FDTD 仿真 80 nm 金纳米球放在 100 nm 金膜上，中间 SiO2 gap 为 5 nm，平面波正入射，波长范围 400-900 nm，输出散射谱，提取共振波长和 FWHM。" \
  --output outputs/hero_spec.json

optical-spec validate outputs/hero_spec.json

optical-spec meep-generate outputs/hero_spec.json \
  --mode research-preview \
  --output outputs/hero_meep_research.py
```

如果本地安装了 Meep，可以显式运行：

```bash
optical-spec meep-check
optical-spec meep-run outputs/hero_meep_research.py \
  --workdir runs/hero \
  --expected-mode research-preview \
  --timeout 300
```

`meep-run` 是可选本地 execution harness，不是 full solver automation。

## CLI 使用

最小本地 quickstart：

```bash
# 查看本地 CLI surface
optical-spec --help

# 导出 schema，不需要网络服务
optical-spec schema --output outputs/schema.json

# 使用默认 rule parser 解析并验证
optical-spec parse \
  "用 Meep FDTD 仿真金纳米球-金膜 gap plasmon，输出散射谱和 FWHM。" \
  --output outputs/quickstart_spec.json
optical-spec validate outputs/quickstart_spec.json

# 查看 adapter scaffold，不运行外部 solver
optical-spec adapter-list --json

# 规划本地 workflow，不执行 solver
optical-spec workflow-plan \
  "用 MPB 计算二维光子晶体 band diagram，输出前 8 条能带。" \
  --parser hybrid \
  --llm-provider mock \
  --tool mpb
```

这些命令都走本地 deterministic 路径。外部 solver 和外部 LLM provider 都是可选项，
默认测试和 quickstart 不需要它们。

基础命令：

```bash
optical-spec parse "研究金纳米球-金膜体系中 gap 从 5 到 25 nm 变化对散射谱主峰线宽和退相位时间的影响，使用 Meep FDTD，提取共振波长、FWHM 和 T2。" \
  --output outputs/my_spec.json

optical-spec validate outputs/my_spec.json
optical-spec schema --output outputs/schema.json
optical-spec example all
```

Parser 模式：

```bash
optical-spec parse "..." --parser rule
optical-spec parse "..." --parser llm --llm-provider mock
optical-spec parse "..." --parser hybrid --llm-provider mock
optical-spec parse "..." --parser hybrid --llm-provider mock \
  --parser-report-output outputs/parser_report.json
```

`rule` 是默认模式。`mock` provider 是 deterministic test provider，不代表真实外部
LLM 能力。

## Meep 生成模式

```bash
optical-spec meep-generate outputs/my_spec.json \
  --mode preview \
  --output outputs/meep_preview.py

optical-spec meep-generate outputs/my_spec.json \
  --mode research-preview \
  --output outputs/meep_research.py

optical-spec meep-generate outputs/my_spec.json \
  --mode smoke \
  --output outputs/meep_smoke.py
```

模式含义：

- `preview`: 快速生成结构和脚本预览。
- `research-preview`: 生成 reference / structure runs、CSV/JSON/PNG artifact 逻辑。
- `smoke`: 结构验证用的低成本脚本。

Au library research-preview 曾经存在 NaN/Inf 和 timeout 风险；相关诊断保存在
`docs/local_meep_*_v0.6.md`。不要把 research-preview 输出直接当作生产级物理结论。

## v0.6 物理诊断

`diagnose` 是 post-hoc diagnostics，不运行 Meep，不生成 Meep 脚本，也不证明
convergence。

```bash
optical-spec diagnose outputs/my_spec.json \
  --output-dir outputs \
  --create-demo-spec-if-missing

optical-spec diagnose outputs/my_spec.json \
  --output-dir outputs \
  --run-dir runs/demo \
  --json
```

默认输出：

- `mesh_report.csv`
- `flux_report.csv`
- `execution_diagnostics.json`
- `diagnostic_preview.png`

如果 `run-dir` 缺少 `stdout.txt`、`stderr.txt`、`execution_result.json` 或
`run_manifest.json`，diagnostics 会记录 missing artifacts，而不是崩溃。

## v0.7 多求解器 Adapter

通用 adapter CLI：

```bash
optical-spec adapter-list
optical-spec adapter-list --json

optical-spec adapter-generate outputs/my_spec.json \
  --tool auto \
  --output outputs/generated_input.py

optical-spec adapter-generate outputs/my_spec.json \
  --tool mpb \
  --output outputs/mpb_band.py

optical-spec adapter-generate outputs/my_spec.json \
  --tool gmsh \
  --output outputs/geometry.geo

optical-spec adapter-generate outputs/my_spec.json \
  --tool elmer \
  --mesh outputs/geometry.msh \
  --output outputs/case.sif

optical-spec adapter-generate outputs/my_spec.json \
  --tool optiland \
  --output outputs/optiland_design.py
```

这些 adapter 只生成 solver-native input scaffold，不运行 MPB、Gmsh、Elmer 或
Optiland。`adapter-generate` 是通用入口；`meep-generate` 是保留的 Meep 专用入口。

## v0.8 LLM Parser Foundation

v0.8 提供 provider-agnostic LLM parser architecture：

- `LLMParserConfig`
- `BaseLLMClient`
- deterministic `MockLLMClient`
- prompt builder
- JSON extraction / repair
- fallback to rule parser
- conservative hybrid merge
- parser report

运行 mock benchmark：

```bash
optical-spec llm-eval benchmarks/llm_cases.json \
  --parser hybrid \
  --llm-provider mock \
  --report outputs/llm_eval_report.json
```

限制：

- 默认不调用外部 LLM。
- mock provider 只是 deterministic test infrastructure。
- LLM parser 只抽取 spec，不验证物理正确性。
- 所有 LLM 输出仍需 schema normalization、Pydantic validation 和 SpecValidator。

## v0.9 Workflow Orchestration

Workflow 是本地同步编排层，不是后台队列、云执行或自治 solver 系统。

```bash
optical-spec workflow-plan \
  "用 Meep FDTD 仿真金纳米球-金膜 gap plasmon，扫 gap 5 到 25 nm，输出散射谱和 FWHM。" \
  --parser rule \
  --tool auto

optical-spec workflow-run \
  "用 MPB 计算二维光子晶体 band diagram，扫 Γ-X-M-Γ k 点，输出前 8 条能带。" \
  --parser hybrid \
  --llm-provider mock \
  --tool mpb \
  --output-dir outputs/workflows/mpb_demo \
  --no-execute

optical-spec workflow-replay outputs/workflows/mpb_demo/workflow_run.json \
  --output-dir outputs/workflows/mpb_demo_replay

optical-spec workflow-report outputs/workflows/mpb_demo/workflow_run.json \
  --output outputs/workflows/mpb_demo/report.md
```

典型 artifact：

- `workflow_run.json`
- `workflow_plan.json`
- `workflow_summary.md`
- `workflow_summary.json`
- `human_review_checklist.md`
- step JSON files
- generated input scaffold

Workflow 评价的是工程链路完整性，不是物理正确性。

## Python SDK

```python
from optical_spec_agent.services.spec_service import SpecService
from optical_spec_agent.parsers.llm import LLMParserConfig, MockLLMClient

svc = SpecService(
    parser="hybrid",
    llm_config=LLMParserConfig(provider="mock"),
    llm_client=MockLLMClient(),
)

spec = svc.process("用 MPB 计算二维光子晶体 band diagram，输出前 8 条能带。")
print(spec.model_dump())
```

## API

FastAPI endpoints 包括：

- `GET /health`
- `POST /parse`
- `POST /validate`
- `GET /schema`
- `POST /workflow/plan`
- `POST /workflow/run`
- `POST /workflow/report`

示例：

```bash
uvicorn optical_spec_agent.api.app:app --reload
```

API 默认不运行 solver。`/parse` 可以选择 `parser=rule|llm|hybrid`，mock provider
可用于 deterministic local tests。

## Demo Gallery

示例输出位于：

- `examples/outputs/demo_gap_plasmon_sweep.json`
- `examples/outputs/demo_asymmetric_cross.json`
- `examples/outputs/demo_comsol_waveguide.json`

重新生成 demo：

```bash
python scripts/regenerate_demo_outputs.py
```

这些 demo 是 parser/spec 示例，不是 solver 结果。

## Schema 设计

OpticalSpec 将任务拆成主要 section：

- `task`
- `physics`
- `geometry_material`
- `simulation`
- `output`
- provenance / missing fields / validation status

字段状态：

- `confirmed`: 用户明确表达。
- `inferred`: 规则或 parser 保守推断。
- `missing`: 信息不足，需要人工补充。

Schema stability policy 见 `docs/schema_stability.md`。

## 测试

```bash
pytest -q
make check
```

默认测试不要求安装 Meep、MPB、Gmsh、Elmer、Optiland，也不要求外部 LLM API。

## Benchmark

```bash
python benchmarks/run_benchmark.py --mode key_fields
python benchmarks/run_semantic_benchmark.py
python benchmarks/run_semantic_benchmark.py --report outputs/semantic_benchmark_report.json

python benchmarks/run_llm_benchmark.py \
  --cases benchmarks/llm_cases.json \
  --parser hybrid \
  --llm-provider mock \
  --report outputs/llm_eval_report.json

python benchmarks/run_workflow_benchmark.py \
  --cases benchmarks/workflow_cases.json \
  --output-dir outputs/workflow_benchmark \
  --report outputs/workflow_benchmark_report.json
```

Benchmark 检查解析、semantic routing、mock LLM parser 和 workflow 完整性；它们不
验证真实物理结果。

## Release Engineering / 质量门禁

```bash
OSA_SMOKE_VENV=/tmp/osa-smoke-rc4-dev ./scripts/smoke_release.sh
python scripts/check_cli_surface.py
python scripts/check_docs_consistency.py
python scripts/check_release_readiness.py --report outputs/release_readiness_report.json
python scripts/check_artifact_contracts.py
python -m build
twine check dist/*
```

GitHub Actions 覆盖 deterministic local gates、docs checks、manual benchmarks 和
release dry-run。默认 CI 不依赖外部 solver 或外部 LLM。

`v0.9.0rc6` 的 GitHub prerelease 已完成验证。后续 RC 应继续使用
`scripts/smoke_release.sh` 和 `docs/release_engineering_playbook.md` 记录的流程。
该流程不发布 PyPI、不上传 `dist/`，也不移动已有 tag。
从当前 RC 线走向 `v1.0` 的剩余门槛见 `docs/v1_0_readiness_plan.md`。

## Roadmap

- v0.5: packaged baseline / Meep execution harness。
- v0.6: local diagnostics。
- v0.7: multi-solver adapter MVP。
- v0.8: LLM parser foundation。
- v0.9: local synchronous workflow orchestration。
- v1.0: API stabilization、文档收口、release hardening。

## 发布候选说明：v0.9.0rc6

`v0.9.0rc6` 是当前 release candidate：

- 不是 final stable `1.0`。
- GitHub pre-release 已创建并验证：draft=false, prerelease=true。
- PyPI 发布需要单独批准。
- Release draft: `docs/github_release_draft_v0.9.0rc6.md`
- Post-release status: `docs/post_release_status_v0.9.0rc6.md`
- Release playbook: `docs/release_engineering_playbook.md`

## 已知限制

- 不提供 production-grade physical validation。
- 不提供 formal convergence proof。
- 不提供 full solver automation。
- external solvers 默认不运行。
- external LLM 默认不需要。
- adapter outputs 是 MVP/scaffold。
- workflow 是 local/synchronous preview。
- RC 不是 final `1.0` stability。
- Meep execution 仍是 optional/local。
- 真实研究使用前必须人工审查几何、材料模型、边界条件、网格、监视器和收敛性。

## 后端光学语言诊断

后端现在通过 `/api/optical-language/infer`、`/api/optical-language/diagnose`、
`/api/optical-language/observables/diagnose`、`/api/optical-language/adapter-mapping`
和 `/api/agent-session` 暴露确定性的光源/监测器推断、观测量诊断和适配器原生映射。
纳米颗粒散射预览默认是平面波式光源、400-900 nm 波段、`linear_x` 偏振，以及
散射/消光谱监测器。后端可以说明这些意图如何映射到 Meep、MPB、Gmsh、Elmer 或
Optiland 的预览语义。这些只是 preview/design-assist 假设，不是外部求解器执行后的
monitor 结果。

## License

MIT. See [LICENSE](LICENSE).
