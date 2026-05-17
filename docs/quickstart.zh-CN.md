# Quickstart

## 1. 你将运行什么

这个 quickstart 会启动本地 Agent Studio demo：解析 optical spec、验证 spec、
选择 adapter、生成 workflow plan、预览 solver input scaffold，并查看 validation
evidence。

这是一个 local-first、preview-first 的 agent demo，使用 Local Agent API 和 Agent
Studio frontend MVP。

## 2. 这个 Quickstart 不会做什么

- 不默认运行外部 solver。
- 不默认调用外部 LLM。
- 不上传或发布 PyPI/TestPyPI。
- 不创建 tag/release。
- 不声称 production-grade physical validation。
- 不声称 formal convergence proof。
- 不复制外部网站内容、品牌或资产。

## 3. 前置条件

- Python 3.11。
- Node/npm。
- 本仓库的本地 checkout。
- 当前公开 prerelease: v0.9.0rc6。
- 当前 main development version: 0.9.0rc7.dev0。

## 4. 一条命令准备环境

创建一次性本地 demo venv 并安装 frontend 依赖：

```bash
./scripts/bootstrap_demo_env.sh
```

默认 venv 路径：

```bash
/tmp/osa-agent-studio-demo
```

## 5. 运行本地 Demo

激活环境并启动 quickstart：

```bash
source /tmp/osa-agent-studio-demo/bin/activate
./scripts/run_quickstart_demo.sh
```

如需只运行 smoke 并退出：

```bash
OSA_QUICKSTART_NO_HOLD=1 ./scripts/run_quickstart_demo.sh
```

可选 visual smoke 仍然是手动项：

```bash
OSA_QUICKSTART_WITH_VISUAL=1 OSA_QUICKSTART_NO_HOLD=1 ./scripts/run_quickstart_demo.sh
```

## 6. 打开 Agent Studio

- Frontend: http://127.0.0.1:5173
- API health: http://127.0.0.1:8000/api/health
- API docs: http://127.0.0.1:8000/docs

## 7. Guided Demo 步骤

1. Load example spec。
2. Parse locally。
3. Validate。
4. View adapter matrix。
5. Generate workflow plan。
6. Preview artifact。
7. Review validation evidence。
8. Readiness / next actions。

Frontend 的 guided demo panel 会显示每一步对应的 Local Agent API endpoint。

## 8. 成功标志

你应该看到：

- API connected。
- Package version `0.9.0rc7.dev0`。
- `api_contract_version` `0.1`。
- No solver executed。
- No external LLM called。
- Preview-only warnings。
- Adapter evidence summary。
- PyPI not published。
- 没有 tag/release controls。

## 9. Troubleshooting

API 启动、frontend 启动、端口占用、npm、Playwright、CORS 和 fixture mode
问题见 `docs/agent_studio_demo_troubleshooting.md`。
