# 应用领域注册表

应用领域注册表把常见光学设计领域映射到需求模板、材料适用性检查、
预期计算器、适配器预览路径和缺失输入问题。它是本地、确定性的
preview/design-assist 机制，不调用外部 LLM，不执行外部求解器，也不联网查询材料数据库。

## 已注册领域

| 领域 | 需求模板 | 材料 | 计算器 / 适配器路径 |
| --- | --- | --- | --- |
| `nanoparticle_plasmonics` | `nanoparticle_plasmonics` | Ag, Au, SiO2, air, water | Meep/Gmsh 预览元数据 |
| `thin_film_coating` | `thin_film_ar_coating` | SiO2, TiO2, Al2O3, BK7 preview | 薄膜光谱和四分之一波增透预览 |
| `slab_waveguide` | `slab_waveguide_single_mode` | Si, Si3N4, SiO2, air | 波导 V-number 扫描、MPB/Elmer 预览 |
| `photonic_crystal` | `photonic_crystal_band_preview` | Si, GaAs, SiO2, air | MPB 能带预览元数据 |
| `dielectric_metasurface` | `dielectric_metasurface_preview` | TiO2, Si3N4, Si, SiO2 | Meep/Gmsh 预览元数据 |
| `lens_ray_optics` | `paraxial_lens_imaging` | BK7 preview, fused silica preview, air | 近轴计算器和 Optiland 预览 |
| `gaussian_beam_focusing` | `gaussian_beam_focus` | air, fused silica preview | 高斯光束传播/聚焦预览 |
| `imaging_system_preview` | `paraxial_lens_imaging` | BK7 preview, fused silica preview, air | 近轴中继和 Optiland 预览 |
| `fiber_coupling_preview` | `gaussian_beam_focus`, `slab_waveguide_single_mode` | fused silica preview, SiO2, Si3N4 | 部分高斯/波导预览；耦合求解器推迟 |
| `polarization_optics_preview` | `dielectric_metasurface_preview` | TiO2, Si3N4, SiO2, fused silica preview | 部分元数据；专用偏振模型推迟 |

## API

- `GET /api/application-domains`
- `GET /api/application-domains/{domain_id}`
- `POST /api/application-domains/match`
- `GET /api/application-domains/{domain_id}/cross-check`
- `GET /api/application-domain-cross-checks`

## 安全边界

该注册表只记录预览级覆盖。材料常数仍是本地 starter 值，需要用户验证。
计算器和适配器路径是 design-assist 脚手架，不是生产级物理验证。
默认不需要、也不执行外部求解器或外部 LLM。

