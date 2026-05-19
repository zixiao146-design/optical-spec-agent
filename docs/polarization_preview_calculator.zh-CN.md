# 偏振预览计算器

偏振预览计算器提供确定性的 Jones calculus 工具，用于本地偏振片和波片设计
推理。它是 design-assist 计算器，不是矢量电磁仿真。

Endpoint：`POST /api/optics/polarization-jones`

## 支持的预览

- `linear_polarization(angle_deg)`
- `jones_linear_polarizer(input_jones, angle_deg)`
- `jones_waveplate(input_jones, retardance_rad, fast_axis_deg)`
- `summarize_polarization_state(jones_vector)`

## 输入

API 可以接收显式双分量 Jones vector，也可以通过 `input_angle_deg` 生成线偏振
输入态。Jones 分量可以是数字、`[real, imag]` 或 `{real, imag}` 对象。

## 假设

- Jones vector 表示相干双分量偏振态。
- 偏振片是理想器件。
- 波片是理想、空间均匀、预览中不随波长变化的器件。
- 不包含退偏、孔径效应、镀膜、色散或完整矢量场传播。

## 参考 sanity cases

- 0 度线偏振约为 `[1, 0]`。
- 90 度线偏振约为 `[0, 1]`。
- 45 度输入通过 0 度理想偏振片，强度约为 `cos^2(45 deg) ~= 0.5`。
- 45 度快轴半波片把水平输入旋转到垂直方向，忽略全局相位。
- 四分之一波片对合适的 45 度输入引入接近 `pi/2` 的相对相位。

JSON 参考算例位于 `examples/optics_reference_cases/polarization/`；综合参考策略见
[`fiber_polarization_reference_cases.zh-CN.md`](fiber_polarization_reference_cases.zh-CN.md)。

## 限制

这只是 preview/design-assist 证据。

- 默认不执行外部求解器。
- 默认不调用外部 LLM。
- 不声明生产级物理验证。
- 不声明形式化收敛证明。
- 真实偏振器件行为需要用经过验证的 Jones/Mueller 测量或矢量电磁仿真确认。
