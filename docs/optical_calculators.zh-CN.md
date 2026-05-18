# 光学预览计算器

后端现在包含轻量的本地光学设计预览计算器。这些计算器是确定性的
Python design-assist 工具，不运行外部求解器，不调用外部 LLM，也不联网查询
材料数据库。

## 计算器

| 计算器 | Endpoint | 用途 |
| --- | --- | --- |
| 薄膜叠层预览 | `POST /api/optics/thin-film` | 简单层状结构的近法向 transfer-matrix 估计。 |
| 薄膜光谱预览 | `POST /api/optics/thin-film-spectrum` | 对反射率、透射率和吸收估计做波长扫描。 |
| 四分之一波长 AR 设计 | `POST /api/optics/quarter-wave-ar` | 根据 `sqrt(n0 * ns)` 给出单层减反膜起点。 |
| 近轴透镜预览 | `POST /api/optics/paraxial-lens` | 薄透镜成像距离和放大率估计。 |
| 近轴系统预览 | `POST /api/optics/paraxial-system` | 组合自由空间和薄透镜 ABCD 元件。 |
| 双透镜 relay 预览 | `POST /api/optics/two-lens-relay` | 理想薄透镜的双透镜 relay 估计。 |
| 高斯光束预览 | `POST /api/optics/gaussian-beam` | 瑞利长度、光束半径、曲率半径和 Gouy 相位估计。 |
| 高斯光束序列 | `POST /api/optics/gaussian-beam-series` | 沿 z 方向生成光束半径采样。 |
| 高斯光束聚焦 | `POST /api/optics/gaussian-beam-focus` | 理想薄透镜的衍射极限聚焦估计。 |
| 波导 V-number 预览 | `POST /api/optics/waveguide-estimate` | 标量 slab 波导 V-number 和单模倾向估计。 |
| 波导厚度扫描 | `POST /api/optics/waveguide-sweep` | 对芯层厚度扫描 V-number。 |
| 波导单模范围 | `POST /api/optics/waveguide-single-mode-range` | 基于 `V < pi` 给出标量 slab 单模厚度范围。 |

## 假设

- 薄膜估计使用调用者提供的预览 n/k 数值。
- 薄膜数值估计当前使用法向入射 transfer matrix。
- 薄膜光谱扫描不自动加入材料色散；如需色散，需要调用者显式提供不同波长的
  n/k。
- 四分之一波长 AR 只是单层、法向入射的设计起点。
- 近轴透镜估计假设小角度、不包含像差和孔径效应。
- 近轴系统和双透镜 relay 使用理想薄透镜和均匀自由空间段。
- 高斯光束估计假设理想基模高斯光束，介质折射率为 1.0。
- 高斯聚焦假设准直高斯光束入射理想薄透镜，不包含 M^2、孔径截断和像差。
- 波导估计只提供标量 slab 波导方向性判断，不求解矢量本征模。
- 波导厚度扫描和单模范围只是标量方向性判断，不是本征模求解。

## 结果摘要

计算器响应包含 `status`、`result`、`assumptions`、`diagnostics` 和保守安全
字段。扫描类响应包含采样点数量和摘要字段，方便 agent session 展示“实际计算了什么”，
但不会把结果说成生产级物理验证。

## 限制

这些计算器仅用于本地预览和设计辅助，不是生产级仿真验证。

- 不声明生产级物理验证。
- 不声明形式化收敛证明。
- 默认不执行外部求解器。
- 默认不调用外部 LLM。
- 用户必须在做物理结论前自行验证材料数据、边界条件和数值方法。

示例请求位于 `examples/optics_calculators/`。
