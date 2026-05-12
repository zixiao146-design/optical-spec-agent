# optical-spec-agent

[English](README.md) | [简体中文](README.zh-CN.md)

> 将中英文光学仿真需求编译为经过校验的 OpticalSpec JSON，并生成
> solver-native input scaffold。

## 项目定位

**optical-spec-agent** 是一个连接“自然语言光学仿真需求”和“可执行光学
求解器输入”的规格编译层。用户可以用中文或英文描述仿真任务，项目会生成
结构化、经过校验的 OpticalSpec JSON，并可进一步生成 Meep 脚本或
MPB/Gmsh/Elmer/Optiland 的 solver-native input scaffold。

它不是求解器。默认情况下，它生成 spec、脚本、adapter scaffold、诊断报告和
workflow artifact；它不会默认运行外部 solver，也不提供 production-grade
physical validation。

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

当前 package version 是 `v0.9.0rc1`。这是 release candidate，不是 final
stable `1.0`。

`v0.6` 到 `v0.9` 的能力属于 preview/scaffold/evaluation capabilities：

- `v0.6`: 本地 post-hoc physical diagnostics。
- `v0.7`: 多求解器 adapter MVP scaffold。
- `v0.8`: LLM parser foundation，默认使用 deterministic mock provider。
- `v0.9`: 本地同步 workflow orchestration。

GitHub pre-release 和 tag 需要维护者手动创建。PyPI 发布不在当前 release
candidate 准备任务范围内，除非后续单独批准。

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
python scripts/check_cli_surface.py
python scripts/check_docs_consistency.py
python scripts/check_release_readiness.py --report outputs/release_readiness_report.json
python scripts/check_artifact_contracts.py
python -m build
twine check dist/*
```

GitHub Actions 覆盖 deterministic local gates、docs checks、manual benchmarks 和
release dry-run。默认 CI 不依赖外部 solver 或外部 LLM。

## Roadmap

- v0.5: packaged baseline / Meep execution harness。
- v0.6: local diagnostics。
- v0.7: multi-solver adapter MVP。
- v0.8: LLM parser foundation。
- v0.9: local synchronous workflow orchestration。
- v1.0: API stabilization、文档收口、release hardening。

## 发布候选说明：v0.9.0rc1

`v0.9.0rc1` 是 release candidate：

- 不是 final stable `1.0`。
- GitHub pre-release / tag 需要维护者手动创建。
- PyPI 发布需要单独批准。
- Release draft: `docs/github_release_draft_v0.9.0rc1.md`
- Manual checklist: `docs/manual_release_checklist_v0.9.0rc1.md`
- Final gate: `docs/final_rc_gate_v0.9.0rc1.md`

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

## License

MIT. See [LICENSE](LICENSE).
