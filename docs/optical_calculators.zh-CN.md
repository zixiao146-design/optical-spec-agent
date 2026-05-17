# 光学预览计算器

后端现在包含轻量的本地光学设计预览计算器。这些计算器是确定性的
Python design-assist 工具，不运行外部求解器，不调用外部 LLM，也不联网查询
材料数据库。

## 计算器

| 计算器 | Endpoint | 用途 |
| --- | --- | --- |
| 薄膜叠层预览 | `POST /api/optics/thin-film` | 简单层状结构的近法向 transfer-matrix 估计。 |
| 近轴透镜预览 | `POST /api/optics/paraxial-lens` | 薄透镜成像距离和放大率估计。 |
| 高斯光束预览 | `POST /api/optics/gaussian-beam` | 瑞利长度、光束半径、曲率半径和 Gouy 相位估计。 |
| 波导 V-number 预览 | `POST /api/optics/waveguide-estimate` | 标量 slab 波导 V-number 和单模倾向估计。 |

## 假设

- 薄膜估计使用调用者提供的预览 n/k 数值。
- 薄膜数值估计当前使用法向入射 transfer matrix。
- 近轴透镜估计假设小角度、不包含像差和孔径效应。
- 高斯光束估计假设理想基模高斯光束，介质折射率为 1.0。
- 波导估计只提供标量 slab 波导方向性判断，不求解矢量本征模。

## 限制

这些计算器仅用于本地预览和设计辅助，不是生产级仿真验证。

- 不声明生产级物理验证。
- 不声明形式化收敛证明。
- 默认不执行外部求解器。
- 默认不调用外部 LLM。
- 用户必须在做物理结论前自行验证材料数据、边界条件和数值方法。

示例请求位于 `examples/optics_calculators/`。

