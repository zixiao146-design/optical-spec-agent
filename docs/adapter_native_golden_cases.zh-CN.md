# Adapter 原生 Golden Preview Cases

这些 golden cases 用来证明 source、monitor 和 observable 意图如何映射到各个
adapter 的原生预览语义。它们是本地后端 fixture 和测试证据，不是真实求解器
监测结果，也不是生产级物理验证。

当前状态：

- 当前公开 prerelease：`v0.9.0rc7`
- 当前 main development version：`0.9.0rc8.dev0`
- PyPI：未发布
- TestPyPI：仅上传并验证过 `0.9.0rc6.dev0`

## 目的

golden cases 检查后端是否稳定保留这条路径：

```text
自然语言目标
-> source/monitor 推断
-> observable diagnostics
-> adapter-native source/monitor mapping
-> preview metadata
```

检查过程是本地、确定性的。它不会运行 Meep、MPB、Gmsh、ElmerSolver、
Optiland，不调用外部 LLM，不上传，不创建 tag，也不创建 GitHub release。

## Golden Cases

| Case | Adapter | Source 意图 | Monitor / observable 意图 | 预期原生预览语义 |
| --- | --- | --- | --- | --- |
| `meep_nanoparticle_scattering` | Meep | plane-wave-like broadband 400-900 nm, `linear_x` | scattering / extinction spectrum | `mp.Source`、broadband / `GaussianSource` metadata、flux / DFT monitor metadata |
| `mpb_photonic_crystal_band` | MPB | eigenmode / band context | band structure、mode frequencies | k-points、band frequencies、无 driven time-domain source |
| `gmsh_mesh_region` | Gmsh | 仅几何注释 | mesh region / physical groups | physical groups 和 mesh-region annotations；Gmsh 本身不计算光学 observable |
| `elmer_fem_boundary_source` | Elmer | FEM source / boundary placeholder | FEM output / result placeholder | boundary condition、source term、solver/output section placeholders |
| `optiland_lens_image_plane` | Optiland | ray bundle / object metadata | image plane、focal spot、ray fan | ray bundle、image plane、focal spot、spot diagram、ray fan preview metadata |

每个 case 位于 `examples/adapter_native_golden/`，包含：

- `request.json`
- `source_model.json`
- `monitor_model.json`
- `observable_diagnostics.json`
- `adapter_mapping.json`
- `expected_metadata.json`
- `expected_preview_fragments.txt`
- `README.md`

## 检查内容

`scripts/check_adapter_native_golden.py` 会读取每个 case，通过 FastAPI
`TestClient` 调用本地 `/api/optical-language/adapter-mapping` endpoint，并检查：

- source model fixture 与生成结果一致
- monitor model fixture 与生成结果一致
- observable diagnostics fixture 与生成结果一致
- adapter mapping fixture 与生成结果一致
- 严格 expected metadata 与 adapter name、source type、monitor type、
  observable kinds、native terms、preview-only flags 和 safety flags 一致
- expected fragments 出现在生成的 mapping metadata 中
- `external_solver_executed=false`
- `external_llm_required=false`
- `production_grade_validation_claimed=false`
- `formal_convergence_proof_claimed=false`

配套覆盖矩阵见 `docs/adapter_native_golden_coverage_matrix.zh-CN.md`，并通过
`GET /api/adapter-native-golden-coverage` 暴露。

运行：

```bash
python scripts/check_adapter_native_golden.py
```

可选 JSON 报告：

```bash
OSA_ADAPTER_NATIVE_GOLDEN_REPORT=/tmp/osa-adapter-native-golden.json \
  python scripts/check_adapter_native_golden.py
```

## Preview-Only 边界

这些 case 只是 adapter-native preview metadata，不是真实 solver monitor output。
真实 flux spectra、band diagrams、FEM field outputs、ray fans 或 focal spot
结果需要显式执行 solver，并需要单独验证证据。

不声明生产级物理验证。不声明形式化收敛证明。
