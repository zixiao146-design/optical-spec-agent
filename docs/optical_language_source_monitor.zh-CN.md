# 光学语言光源和监测器

本文档说明 Agent Studio 后端如何用本地确定性逻辑推断光源、监测器和观测量。

Current public prerelease: v0.9.0rc6。Current main development version:
`0.9.0rc7.dev0`。

## 目的

自然语言光学目标会先被转换为预览级光学语言：

自然语言目标 -> 光学意图 -> 光源模型 -> 监测器模型 -> 观测量 ->
缺失输入诊断。

默认不执行外部求解器。默认不调用外部 LLM。所有光源/监测器信息都是
preview/design-assist 元数据。

## 光源类型

- `plane_wave`：平面波式照明元数据。
- `gaussian_beam`：标量近轴高斯光束元数据。
- `mode_source`：本征模或导模上下文元数据。
- `broadband_pulse`：预留的宽带脉冲预览类型。
- `ray_bundle`：近轴透镜预览中的光线束。
- `unknown`：目标过于模糊时使用。

## 监测器类型

- `scattering_spectrum`：散射/消光谱预览。
- `reflectance_transmittance`：薄膜 R/T/A 预览。
- `near_field`：近场元数据。
- `far_field`：远场元数据。
- `mode_overlap`：模式重叠或 V-number 预览。
- `focal_spot`：焦斑/光腰预览。
- `image_plane`：近轴像面估计。
- `phase_profile`：超表面相位/远场预览元数据。
- `band_structure`：光子晶体能带预览元数据。
- `unknown`：观测量不清楚时使用。

## 默认示例

- `nanoparticle_plasmonics`：默认平面波式光源、400-900 nm 波段、
  `linear_x` 偏振、散射/消光谱监测器。
- `thin_film_ar_coating`：法向入射平面波、400-800 nm 扫描、
  反射/透射监测器。
- `gaussian_beam_focus`：高斯光束光源和焦斑监测器。
- `slab_waveguide_single_mode`：模式源元数据和模式/V-number 监测器。
- `photonic_crystal_band_preview`：本征模上下文和能带监测器。
- `paraxial_lens_imaging`：光线束和像面监测器。
- `dielectric_metasurface_preview`：平面波光源和相位/远场预览监测器。

## 安全边界

监测器定义只是元数据，不是外部求解器运行得到的 monitor 结果。
不声明生产级物理验证，也不声明形式化收敛证明。
