# 光纤耦合预览计算器

光纤耦合预览计算器使用标量 Gaussian 模式重叠估计，为本地设计提供方向性
参考。它是确定性的 Python 计算，不执行外部求解器。

Endpoint：`POST /api/optics/fiber-coupling`

## 输入

- `wavelength_nm`
- `waist_input_um`
- `waist_fiber_um`
- `lateral_offset_um`
- `angular_tilt_mrad`

## 近似公式

预览把耦合效率拆成三个有界因子：

- 模式尺寸失配：
  `eta_w = (2 w_in w_f / (w_in^2 + w_f^2))^2`
- 横向偏移惩罚：
  `eta_d = exp(-2 d^2 / (w_in^2 + w_f^2))`
- 角度倾斜惩罚：使用标量 Gaussian 相位重叠估计

最终 `coupling_efficiency_estimate` 会限制在 `[0, 1]`。

## 假设

- 输入光束和光纤模式都近似为圆对称标量 Gaussian 模式。
- 不包含偏振重叠、Fresnel 损耗、NA 截断、像差和模式求解器效应。
- 完全光腰匹配、零偏移、零倾角是本地 sanity case。

## 限制

这只是 preview/design-assist 证据。

- 默认不执行外部求解器。
- 默认不调用外部 LLM。
- 不声明生产级物理验证。
- 不声明形式化收敛证明。
- 真实耦合效率需要用经过验证的模式重叠、BPM、测量或求解器工作流确认。
