# AGENTS.md

## Project identity

This project is `optical-spec-agent`.

It is not a general chatbot and not a full optical simulation platform yet.
Current goal: convert natural-language optical simulation requests into a structured, provenance-aware `OpticalSpec`, validate missing/inferred/confirmed fields, and translate supported specs into solver-specific scripts.

The main current pipeline is:

```text
natural language input
→ RuleBasedParser
→ OpticalSpec
→ SpecValidator
→ CLI/API output
→ MeepAdapter
→ generated Meep Python script
```

## 项目定位

这个项目是 `optical-spec-agent`。

它现在不是通用聊天机器人，也还不是完整的光学仿真平台。
当前目标是把自然语言光学仿真需求转换成带 provenance 的结构化 `OpticalSpec`，明确字段是 `confirmed / inferred / missing`，再把受支持的 spec 翻译成 solver 脚本。

当前主链路是：

```text
natural language input
→ RuleBasedParser
→ OpticalSpec
→ SpecValidator
→ CLI/API output
→ MeepAdapter
→ generated Meep Python script
```

## Current priority

Do not expand scope unless explicitly asked.

The current development priority is v0.3 reliability:

- improve semantic extraction for one trusted Meep nanoparticle-on-film case
- fix material parsing, especially SiO2 vs Si
- fix dimension extraction, especially particle diameter, film thickness, and gap thickness
- add semantic benchmark
- add adapter-level readiness checks
- keep Meep script generation honest about defaults and limitations

## 当前优先级

除非被明确要求，否则不要主动扩 scope。

当前开发重点是 v0.3 reliability：

- 把一个可信的 Meep nanoparticle-on-film 核心案例语义提取做稳
- 修复材料解析，重点是 `SiO2` 和 `Si`
- 修复尺寸提取，重点是粒子直径、金膜厚度、gap 厚度
- 增加 semantic benchmark
- 增加 adapter-level readiness checks
- 让 Meep 脚本生成对默认值和限制保持诚实

## Important files

- `src/optical_spec_agent/models/spec.py`
- `src/optical_spec_agent/models/base.py`
- `src/optical_spec_agent/parsers/rule_based.py`
- `src/optical_spec_agent/validators/spec_validator.py`
- `src/optical_spec_agent/services/spec_service.py`
- `src/optical_spec_agent/adapters/meep/translator.py`
- `src/optical_spec_agent/adapters/meep/template.py`
- `src/optical_spec_agent/cli/main.py`
- `benchmarks/`
- `tests/`

## Coding rules

- Prefer small, reviewable changes.
- Do not rewrite the entire parser.
- Do not add LLM parsing yet.
- Do not add new solver adapters yet.
- Do not add UI work yet.
- Do not silently hide missing physical parameters behind defaults.
- If a default is used, record it and report it clearly.
- Keep confirmed / inferred / missing provenance meaningful.

## 编码约定

- 优先做小范围、容易 review 的修改。
- 不要重写整个 parser。
- 先不要接入 LLM parsing。
- 先不要新增其他 solver adapter。
- 先不要做 UI。
- 不要用默认值静默掩盖缺失的物理参数。
- 如果使用默认值，必须记录并清楚报告。
- 保持 `confirmed / inferred / missing` 的 provenance 有实际意义。

## Testing

Before finishing code changes, run:

```bash
pytest
python benchmarks/run_benchmark.py --mode key_fields
python benchmarks/run_semantic_benchmark.py
```

If parser behavior is intentionally changed, treat exact snapshot benchmark updates as a separate explicit decision:

```bash
python benchmarks/run_benchmark.py --mode exact
```

## 测试要求

完成代码修改前，至少运行：

```bash
pytest
python benchmarks/run_benchmark.py --mode key_fields
python benchmarks/run_semantic_benchmark.py
```

如果 parser 行为被有意修改，`exact` snapshot benchmark 是否更新应作为单独、明确的决定：

```bash
python benchmarks/run_benchmark.py --mode exact
```
