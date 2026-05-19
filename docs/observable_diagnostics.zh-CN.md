# 观测量诊断

Current public prerelease: v0.9.0rc6. Current main development version:
`0.9.0rc7.dev0`。

观测量诊断会把推断出的监测器意图转成明确的预览观测量元数据。它会列出必需输入、
默认假设、适配器兼容性，以及真实结果是否需要外部求解器执行。该诊断默认不执行外部
求解器，也不调用外部 LLM。

## 观测量分类

- `scattering_spectrum`：FDTD 类工作流中的散射谱预览。
- `extinction_spectrum`：纳米颗粒案例中的消光谱预览。
- `reflectance`：薄膜或 FDTD monitor 中的反射率预览。
- `transmittance`：薄膜或 FDTD monitor 中的透射率预览。
- `absorptance`：基于 R/T/A 预览语义的吸收估计。
- `near_field`：局域近场元数据，通常对应 Meep 上下文中的 DFT field。
- `far_field`：远场投影元数据。
- `dft_field`：DFT field monitor 元数据。
- `band_structure`：MPB 风格的 band / k-point 元数据。
- `mode_frequency`：本征模式频率元数据。
- `mode_overlap`：波导或 mode-source overlap 元数据。
- `focal_spot`：Gaussian beam 或 raytrace 焦斑元数据。
- `image_plane`：paraxial 或 raytrace image plane 元数据。
- `ray_fan`：raytrace 光线扇形图元数据。
- `phase_profile`：超表面相位或波前元数据。
- `mesh_region`：Gmsh physical group / mesh region 元数据。
- `unknown`：目标不明确时的稳定回退。

## 必需输入

每个诊断都会携带必需输入，例如波长范围、偏振、监测区域、k-point path、image
plane、mode index 或 geometry region。如果目标中缺少某个值，后端会记录默认假设，
而不是默默声称已经得到真实结果。

## 预览与真实结果

支持预览表示后端可以描述该观测量，把它附着到 adapter preview，并记录到
tool-call ledger。真实光场、频谱、raytrace 或 band 结果通常需要显式批准后执行外部
求解器；默认不会产生真实 solver monitor result。

`examples/adapter_native_golden/` 中的 adapter-native golden cases 会检查
observable diagnostics 是否能稳定进入 Meep 纳米颗粒散射、MPB 光子晶体能带、
Gmsh 网格区域、Elmer FEM placeholder 和 Optiland 像面预览的 adapter mapping。
`docs/adapter_native_golden_coverage_matrix.zh-CN.md` 会记录每个 case 锁定的
observable kind 和 adapter-native mapping term。

## 安全边界

不声明生产级物理验证。不声明形式化收敛证明。观测量诊断是本地 design-assist 元数据，
应在任何可选 solver 设置之前由用户检查。
