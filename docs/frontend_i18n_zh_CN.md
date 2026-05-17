# Agent Studio 中文本地化

## 1. 当前状态

- Agent Studio 支持 English / 中文。
- API 字段名保持英文稳定。
- UI 文案、guided demo、安全边界支持中文。
- 中文手把手教程已加入前端和文档：
  `docs/agent_studio_chinese_guided_tutorial.md`。
- 中文术语表见 `docs/frontend_chinese_terminology.md`。
- Current main development version: 0.9.0rc7.dev0。
- PyPI 未发布。

## 2. 语言切换

- 前端使用 `LanguageSwitcher` 在 English / 中文之间切换。
- 语言偏好写入 `localStorage` key: `agent-studio-language`。
- 支持语言值：`zh-CN` / `en`。
- 如果没有本地偏好，中文浏览器环境默认显示中文，否则默认 English。

## 3. 中文安全边界

- 默认不执行外部求解器。
- 默认不调用外部 LLM。
- 预览产物不代表生产级物理验证。
- 不声明形式化收敛证明。
- 本界面不控制 PyPI/TestPyPI 上传，也不控制 GitHub tag/release。
- 本演示是本地优先、同步、预览优先的 Agent Studio。

## 4. 不翻译的内容

- API JSON keys
- adapter tool names: `meep`, `gmsh`, `mpb`, `elmer`, `optiland`
- package metadata
- version strings
- `api_contract_version`

## 5. 测试和维护

Tests guard the Chinese copy, English fallback copy, i18n dictionaries,
`LanguageSwitcher`, and the rule that API JSON fields and adapter tool names
remain stable.

## 6. Demo feedback

真实 maintainer demo feedback 已记录在
`docs/agent_studio_demo_feedback.md`。当前 P0 是公开演示前加入中文手把手教程；
页面逐项反馈目前未提供，后续 demo 再补，不编造。
