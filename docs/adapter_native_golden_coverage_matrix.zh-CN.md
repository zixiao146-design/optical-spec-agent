# 适配器原生 Golden 覆盖矩阵

本文档总结本地 adapter-native golden preview case 对 source、monitor、
observable 和 adapter mapping 语义的覆盖情况。这些检查只是
preview/design-assist 证据，不执行 Meep、MPB、Gmsh、ElmerSolver、
Optiland，不调用外部 LLM，不上传，不创建 tag，也不创建 release。
不声明生产级物理验证。不声明形式化收敛证明。

## 覆盖矩阵

| 适配器 | Golden case | Source model | Monitor model | Observable diagnostics | 原生映射术语 | 真实结果需要 solver? | 已执行 solver? | Preview-only? |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Meep | `meep_nanoparticle_scattering` | plane wave，400-900 nm 宽带，linear x | scattering spectrum | scattering/extinction spectrum | `mp.Source`、broadband/GaussianSource metadata、flux/DFT monitor metadata | 是 | 否 | 是 |
| MPB | `mpb_photonic_crystal_band` | eigenmode/band context | band structure | band structure、mode frequency | k-points、band frequencies、eigenmode context | 是 | 否 | 是 |
| Gmsh | `gmsh_mesh_region` | source metadata only | mesh region / physical group | mesh region | physical groups、mesh-region annotations | 真实光学结果需要 Gmsh 之外的 solver | 否 | 是 |
| Elmer | `elmer_fem_boundary_source` | mode source placeholder | mode overlap/output placeholder | mode overlap、mode frequency | boundary condition placeholder、body force/source section、ResultOutputSolver placeholder | 是 | 否 | 是 |
| Optiland | `optiland_lens_image_plane` | ray bundle/object metadata | image plane | image plane、ray fan | ray bundle、image plane、focal spot、ray fan | 是 | 否 | 是 |

## 严格 Metadata Diff

每个 golden case 都包含 `expected_metadata.json`。检查脚本会比较：

- adapter name
- source type
- monitor type
- observable kinds
- required native terms
- `requires_solver_for_real_result`
- `external_solver_executed=false`
- `preview_only=true`
- 不声明生产级物理验证
- 不声明形式化收敛证明

脚本也保留旧的 expected fragment 检查，因此可以同时发现结构化 metadata
漂移和关键说明丢失。

运行：

```bash
python scripts/check_adapter_native_golden.py
```

当严格 metadata 检查通过时，脚本会输出
`ADAPTER NATIVE METADATA DIFF PASSED`。

## Backend Capability Report

同一份覆盖数据也通过以下入口暴露：

- `GET /api/adapter-native-golden-coverage`
- `GET /api/backend-capability-report`
- `scripts/generate_backend_capability_report.py`

报告会记录哪些适配器已覆盖、是否有已注册适配器缺少覆盖，以及每个
golden case 是否仍保持 preview-only 和 solver-free。

## 局限

Golden 覆盖只能证明预览语义稳定，不证明物理正确性。真实 flux、field、
band、FEM、mesh-coupled 或 ray-trace 结果需要显式执行 solver 并进行独立验证。
这些 golden case 不声明生产级物理验证，也不声明形式化收敛证明。
