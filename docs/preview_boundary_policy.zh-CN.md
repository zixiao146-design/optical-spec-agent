# Preview Boundary Policy

本文档定义 `0.9.0rc8.dev0` 后端证据的边界。当前后端可以作为确定性的
光学设计辅助工具，但所有证据仍必须保持 preview/design-assist 级别。

## Preview/Design-Assist 的含义

用户可以依赖后端完成：

- 将支持的光学设计目标确定性地路由到 template 和 application domain；
- 报告 critical / optional 缺失输入；
- 运行本地解析计算器，给出 sanity-checked preview；
- 生成 adapter-native source/monitor metadata preview；
- 默认阻断 external solver、external LLM、upload、tag 和 release 动作；
- 通过本地脚本和 API 响应暴露证据。

用户必须自行验证：

- 材料常数和波长相关数据；
- solver-specific source、monitor、mesh 和 boundary 设置；
- 物理精度、收敛性和容差；
- 生产 workflow 的适用性。

## 组件边界

| 组件 | 边界 |
| --- | --- |
| Materials | 本地 curated preview catalog；不是生产级 optical constants database。 |
| Calculators | sanity-checked analytic preview；不是生产级物理验证。 |
| Application domains | benchmark 检查确定性路由和诊断，不证明物理正确性。 |
| Source/monitor models | 仅 preview metadata；不声称真实 solver monitor result。 |
| Adapter mappings | adapter-native 语义预览；真实结果需要显式批准 solver execution。 |
| Sub-agents | 确定性后端角色；不是独立自主服务。 |
| Frontend | UI/demo surface；不是验证证据。 |

## 发布边界

即使之后批准 PyPI publication，也不代表生产级物理验证。发布和打包状态与
物理验证、solver convergence、材料数据验证是分开的。

## 不声称

- 不声称生产级物理验证。
- 不声称形式化收敛证明。
- 不声称 guaranteed accuracy。
- 默认不执行 external solver。
- 默认不调用 external LLM。
- Elmer Level 3 仍然 deferred。

