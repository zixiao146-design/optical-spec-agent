# 光纤耦合和偏振参考算例

光纤耦合与偏振预览计算器现在包含本地 reference sanity cases，使证据级别与
薄膜、近轴、Gaussian 光束和波导 helper 保持一致。

这些算例只用于 preview/design-assist。它们不执行外部求解器、不调用外部 LLM，
不声明生产级物理验证，也不声明形式化收敛证明。

## 光纤耦合

标量 Gaussian mode-overlap 预览把模式尺寸失配、横向偏移和角度倾斜拆成独立因子：

- `eta_w = (2 w_in w_f / (w_in^2 + w_f^2))^2`
- `offset_factor = exp(-2 dx^2 / (w_in^2 + w_f^2))`
- `tilt_factor ~= exp(-(pi w_eff theta / lambda)^2)`
- `eta = eta_w * offset_factor * tilt_factor`，并限制在 `[0, 1]`

参考算例：

- `fiber_gaussian_perfect_overlap`：腰斑匹配、零偏移、零倾斜，耦合效率接近 `1.0`。
- `fiber_gaussian_waist_mismatch`：腰斑失配会降低估计值。
- `fiber_gaussian_offset_loss`：非零横向偏移会降低估计值。
- `fiber_gaussian_tilt_loss`：非零角度倾斜会降低估计值。

失败模式会拒绝非有限或非正腰斑、非正波长、负横向偏移。

## 偏振

偏振预览使用理想两分量 Jones 计算：

- 线偏振：`[cos(theta), sin(theta)]`
- 理想偏振片：`P = |a><a|`
- 理想波片：旋转到局部轴、施加 retardance、再旋转回实验室坐标

参考算例：

- `jones_linear_0deg`：水平线偏振约为 `[1, 0]`。
- `jones_linear_90deg`：垂直线偏振约为 `[0, 1]`。
- `jones_linear_polarizer_malus`：45 度入射通过 0 度偏振片，强度接近
  `cos^2(45 deg) = 0.5`。
- `jones_half_waveplate_preview`：45 度快轴半波片把水平输入旋到垂直方向，
  忽略全局相位。
- `jones_quarter_waveplate_phase_preview`：四分之一波片对合适的 45 度输入引入
  接近 `pi/2` 的相对相位。

失败模式会拒绝 malformed Jones vector、零强度 Jones vector、非有限角度和非有限
retardance。

## 文件

参考 JSON 算例位于：

- `examples/optics_reference_cases/fiber_coupling/`
- `examples/optics_reference_cases/polarization/`

代表性 API fixtures 位于 `examples/api/`。

## 安全边界

- Calculator quality level 是 `sanity_checked_preview`。
- 输出只属于本地 preview/design-assist 证据。
- 不执行外部求解器。
- 不调用外部 LLM。
- 不声明生产级物理验证。
- 不声明形式化收敛证明。
