# 光学计算器参考算例

后端光学计算器现在包含本地数值 sanity check。这些检查让
preview/design-assist 计算器更有用，但它们不是生产级物理验证，也不是
形式化收敛证明。

## 质量字段

计算器响应包含：

- `quality.quality_level`：当前为 `sanity_checked_preview`
- `quality.reference_case`：适用时记录公式 sanity case
- `quality.assumptions`
- `quality.limitations`
- `quality.warnings`
- `quality.valid_input_range`
- `production_grade_validation_claimed=false`
- `formal_convergence_proof_claimed=false`

响应也保留顶层 `assumptions`、`limitations`、`warnings`，方便 API 和未来前端展示。

## 参考算例

### 薄膜单界面

法向入射空气到玻璃界面：

`R = |(n0 - ns) / (n0 + ns)|^2`

当 `n0=1.0`、`ns=1.5` 时，反射率约为 `0.04`。无损界面下
`R + T ~= 1`。

### 四分之一波长增透膜

理想单层增透膜起点：

- `n_coating = sqrt(n0 * ns)`
- `d = lambda / (4 * n_coating)`

在 `lambda=550 nm`、`n0=1.0`、`ns=1.5` 的简化法向入射模型下，目标波长反射率接近零。

### Gaussian 光束

Gaussian 光束 sanity check 使用：

- `z_R = pi * w0^2 / lambda`
- `w(z) = w0 * sqrt(1 + (z / z_R)^2)`
- `w(0) = w0`
- `w(z_R) = w0 * sqrt(2)`

实现假设理想基模 Gaussian 光束、近轴传播、介质折射率为 1.0。

### 近轴透镜

薄透镜 sanity case 使用：

`1/f = 1/s + 1/s'`

当 `f=50 mm`、`s=100 mm` 时，预期像距为 `s'=100 mm`，放大率为 `-1`。

ABCD 参考矩阵：

- 自由空间：`[[1, d], [0, 1]]`
- 薄透镜：`[[1, 0], [-1/f, 1]]`

双透镜 relay sanity check 覆盖简化 `4f` 约定：
`f1=f2`、`separation=f1+f2`，物体位于第一片透镜前焦平面。

### 波导 V-number

标量平板波导 sanity check 使用：

`V = (2*pi / lambda) * thickness * sqrt(n_core^2 - n_clad^2)`

单模判断只是预览取向，使用 `V < pi`。如果 `n_core <= n_clad`，API 返回稳定错误诊断，
纯 Python helper 会抛出 `ValueError`。

## 失败模式

计算器会拒绝负波长、零物理层厚度、无效折射率、无效 sweep 点数、无法导模的波导折射率组合。
API endpoint 保持稳定错误响应，并保留安全标记。

## 示例文件

参考 JSON 算例位于 `examples/optics_reference_cases/`。

## 安全边界

- 不执行外部求解器。
- 不调用外部 LLM。
- 不联网查询材料数据库。
- 不声明生产级物理验证。
- 不声明形式化收敛证明。
