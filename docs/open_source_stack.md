# optical-spec-agent 开源工具栈技术选型

> **状态**: 路线规划文档，不反映当前仓库已实现的功能。
> 所有工具均尚未接入 optical-spec-agent，本文档定义未来方向。

---

## 1 项目原则

| 原则 | 含义 |
|------|------|
| **Python-first** | 优先选择提供 Python API 或 Python 绑定的工具，降低 agent 调用门槛 |
| **Open-source first** | 仅接入 OSI 认可的开源许可证项目，主线不依赖商业软件 |
| **macOS-friendly** | 核心工具必须在 macOS (ARM + x86) 上可通过 pip / conda / homebrew 安装运行 |
| **Scriptable / agent-friendly** | 工具必须支持纯脚本驱动（CLI 或 Python API），不依赖 GUI 操作 |
| **Modular over monolithic** | 各工具通过适配器（adapter）独立接入，互不耦合，可按需组合 |

---

## 2 商业软件替代路线

### 2.1 Zemax / CODE V → 成像光学 + 序列光线追迹

**商业软件定位**: 透镜设计、像差优化、MTF 分析、序列光线追迹。

**开源替代策略**: 不追求 1:1 替代 Zemax 的全局优化器，而是覆盖"定义光学系统 → 追迹 → 评价"这一核心链路。

| 替代工具 | 覆盖范围 |
|----------|----------|
| **Optiland** | 透镜系统定义、序列追迹、像差分析、MTF/点列图 — 最接近 Zemax 核心功能 |
| **RayOptics** | 读取 .seq / .zmx 文件、序列追迹、基于 dygraph 的简单可视化 — 兼容已有 Zemax 文件 |
| **Raypier** | 非序列追迹与光谱渲染，偏重 illumination — 可补充非序列场景 |

**结论**: Optiland 为主线替代，RayOptics 负责文件兼容，Raypier 补充非序列。

---

### 2.2 LightTools → 非序列光线追迹 + 照明设计

**商业软件定位**: 照明系统设计、杂散光分析、非序列光线追迹、光谱渲染。

**开源替代策略**: 当前没有单一开源工具能完全覆盖 LightTools 的照明设计流程，但可组合实现。

| 替代工具 | 覆盖范围 |
|----------|----------|
| **Raypier** | 非序列追迹、光谱渲染、光源建模 — 最接近 LightTools 的核心 |
| **Optiland** | 可扩展的非序列模式（未来版本） |
| **Meep** (近场) + **远场变换** | 对于散射/衍射类照明问题，可用 FDTD 计算近场再外推远场 |

**结论**: Raypier 为主替代；对于复杂照明问题，可能需要多工具组合，此方向为候选而非主线。

---

### 2.3 COMSOL → FEM 多物理场

**商业软件定位**: 有限元多物理场耦合（电磁、热、力、流体）、GUI 驱动建模。

**开源替代策略**: 用专业 FEM 求解器替代 COMSOL 的电磁模块，不追求"一个软件做所有物理场"。

| 替代工具 | 覆盖范围 |
|----------|----------|
| **Elmer** | 开源多物理场 FEM，支持电磁（麦克斯韦方程）、热传导、结构力学 — 最接近 COMSOL 广度 |
| **GetDP** | 通用 PDE 求解器，通过 .pro 脚本定义方程，灵活性极高 — 适合自定义物理方程 |
| **FEniCS** (备选) | Python 驱动的 FEM 框架，适合高度定制化的 PDE 求解 — 学习曲线较陡 |

**结论**: Elmer 为主线 FEM 工具，GetDP 作为高灵活性备选。两者均通过 Gmsh 生成网格。

---

### 2.4 Meep → 已确定为主线 FDTD

Meep 已在项目 roadmap (v0.3) 中规划为第一个适配器，无需替代。

---

## 3 开源工具栈分层

```
┌─────────────────────────────────────────────────────┐
│             Post-processing / Optimization           │
│         (numpy, scipy, matplotlib, PyVista)          │
├─────────────────────────────────────────────────────┤
│           Lens / Imaging Optics (Sequential)         │
│          Optiland (主线) / RayOptics (兼容)          │
├─────────────────────────────────────────────────────┤
│      Non-sequential Ray Tracing / Illumination       │
│             Raypier (候选) / Optiland 扩展           │
├─────────────────────────────────────────────────────┤
│          Eigenmode / Band Structure                  │
│                    MPB (主线)                        │
├─────────────────────────────────────────────────────┤
│           Electromagnetic Simulation                 │
│           Meep FDTD (主线) / Elmer FEM (主线)        │
├─────────────────────────────────────────────────────┤
│          CAD / Geometry / Meshing                    │
│        Gmsh (主线) / FreeCAD (辅助)                 │
└─────────────────────────────────────────────────────┘
```

---

## 4 各层详细说明

### 4.1 CAD / Geometry / Meshing

#### Gmsh

| 项目 | 说明 |
|------|------|
| **定位** | 三维有限元网格生成器 + CAD 几何内核 |
| **许可证** | GPL-2.0-or-later |
| **为什么适合 agent** | 提供 Python API (`gmsh` 包)，可用脚本定义几何、设置网格参数、导出多种格式；CLI 可无头运行 |
| **macOS** | 支持，`pip install gmsh` 或 `conda install -c conda-forge gmsh` |
| **脚本 vs GUI** | 完全可脚本驱动；GUI 可选 |
| **在 agent 中的角色** | 所有 FEM 类任务（Elmer / GetDP）的前置网格生成器；也可为 Meep 生成复杂几何的 STL/GMSH 文件供导入 |
| **Repo** | https://gitlab.onelab.info/gmsh/gmsh |

#### FreeCAD

| 项目 | 说明 |
|------|------|
| **定位** | 通用参数化 CAD，支持光学元件建模 |
| **许可证** | LGPL-2.1-or-later |
| **为什么适合 agent** | 提供 Python 控制台 + Headless 模式；可通过 `freecad.cmd` CLI 执行 Python 脚本；支持 STEP/IGES/STL 导出 |
| **macOS** | 支持，Homebrew `brew install freecad` 或 conda |
| **脚本 vs GUI** | 支持 Headless 脚本模式（`freecadcmd`），但 API 稳定性一般 |
| **在 agent 中的角色** | 当 Gmsh 的几何脚本不足以描述复杂机械结构时使用；负责参数化 CAD 建模，导出几何给 Gmsh 或直接给求解器 |
| **Repo** | https://github.com/FreeCAD/FreeCAD |

---

### 4.2 Electromagnetic Simulation

#### Meep (FDTD)

| 项目 | 说明 |
|------|------|
| **定位** | 时域有限差分 (FDTD) 电磁仿真 |
| **许可证** | GPL-2.0-or-later |
| **为什么适合 agent** | 纯 Python API (`import meep`)；几何、材料、源、监视器全部通过 Python 对象定义；输出为 numpy 数组；MPI 并行可用 |
| **macOS** | 支持，`pip install meep` 或 `conda install -c conda-forge pymeep` |
| **脚本 vs GUI** | 纯脚本，无 GUI 依赖 |
| **在 agent 中的角色** | 主线 FDTD 求解器；负责纳米光子、plasmonics、超表面、散射、波导等频域/时域电磁问题；v0.3 adapter 的目标工具 |
| **Repo** | https://github.com/NanoComp/meep |

#### Elmer (FEM)

| 项目 | 说明 |
|------|------|
| **定位** | 开源多物理场有限元求解器 |
| **许可证** | GPL-2.0-or-later（核心），部分模块 LGPL |
| **为什么适合 agent** | 通过 `.sif` (Solver Input File) 文本文件定义问题；`ElmerSolver` CLI 无头运行；Python 可通过模板生成 `.sif` + 调用 CLI |
| **macOS** | 支持，`brew install elmer` 或从源码编译；conda 可用 `elmerfem` 包 |
| **脚本 vs GUI** | ElmerGUI 为可选前端，核心完全 CLI 驱动 |
| **在 agent 中的角色** | 主线 FEM 求解器；负责波导模式分析、电磁散射 FEM、热-光耦合等 Meep FDTD 不擅长的问题；与 Gmsh 形成 "Gmsh 建模 → Elmer 求解" 链路 |
| **Repo** | https://github.com/ElmerCSC/elmerfem |

---

### 4.3 Eigenmode / Band Structure

#### MPB (MIT Photonic Bands)

| 项目 | 说明 |
|------|------|
| **定位** | 光子晶体能带结构计算（频域特征模求解） |
| **许可证** | GPL-2.0-or-later |
| **为什么适合 agent** | 提供 Python API (`import meep` 中的 `MPBData` 或独立 `mpb`)；晶格、介电常数全部通过 Scheme 或 Python 脚本定义 |
| **macOS** | 支持，`conda install -c conda-forge mpb` |
| **脚本 vs GUI** | 纯脚本，无 GUI |
| **在 agent 中的角色** | 主线能带计算工具；负责光子晶体带隙分析、波导色散计算；与 Meep 同属 NanoComp 生态，材料定义互通 |
| **Repo** | https://github.com/NanoComp/mpb |

---

### 4.4 Lens / Imaging Optics (Sequential)

#### Optiland

| 项目 | 说明 |
|------|------|
| **定位** | Python 序列光线追迹库，支持透镜系统定义、像差分析、优化 |
| **许可证** | MIT |
| **为什么适合 agent** | 纯 Python，`pip install optiland` 即可；API 为强类型的 Python 对象（`Optic`, `Surface`, `Lens`），天然适合程序化调用；内置优化器 |
| **macOS** | 支持，纯 Python 无系统依赖 |
| **脚本 vs GUI** | 纯脚本，无 GUI |
| **在 agent 中的角色** | 主线成像光学工具；替代 Zemax 的序列追迹、像差分析、MTF 计算、透镜优化功能；通过 adapter 接入 spec → optic definition 链路 |
| **Repo** | https://github.com/HarrisonKramerOptics/optiland |

#### RayOptics

| 项目 | 说明 |
|------|------|
| **定位** | Python 序列光线追迹，支持读取 CODE V (.seq) 和 Zemax (.zmx) 文件 |
| **许可证** | BSD-3-Clause |
| **为什么适合 agent** | 纯 Python；核心为 `opticalmodel` 对象模型，可脚本创建和操作；支持导入已有商业软件设计文件 |
| **macOS** | 支持，纯 Python |
| **脚本 vs GUI** | 脚本 API 完整，Qt GUI 为可选前端 |
| **在 agent 中的角色** | 文件兼容层 — 当用户需要读取已有 Zemax / CODE V 设计文件时使用；不作为主线建模工具（Optiland 更适合新设计） |
| **Repo** | https://github.com/messier16/rayoptics |

---

### 4.5 Non-sequential Ray Tracing / Illumination

#### Raypier

| 项目 | 说明 |
|------|------|
| **定位** | 非序列光线追迹与光谱渲染，偏重照明设计 |
| **许可证** | MIT |
| **为什么适合 agent** | Rust 核心 + Python 绑定；通过 Python API 定义光源、光学元件、探测器；光谱渲染能力是独特优势 |
| **macOS** | 支持，`pip install raypier` |
| **脚本 vs GUI** | 脚本 API 为主 |
| **在 agent 中的角色** | 候选非序列追迹工具；替代 LightTools 的基础照明分析；当前项目成熟度有限，标记为候选而非主线 |
| **Repo** | https://github.com/bd4/rc-raypier |

---

### 4.6 FEM Flexible Solver (备选)

#### GetDP

| 项目 | 说明 |
|------|------|
| **定位** | 通用 PDE 求解器，通过 .pro 脚本自定义弱形式 |
| **许可证** | GPL-2.0-or-later |
| **为什么适合 agent** | 与 Gmsh 深度集成（同一开发团队）；`.pro` 脚本为纯文本，Python 可模板化生成；适合定义非标准 PDE（如非线性光学、耦合方程） |
| **macOS** | 支持，`brew install getdp` 或 conda |
| **脚本 vs GUI** | 纯 CLI |
| **在 agent 中的角色** | 备选 FEM 工具 — 当 Elmer 的内置方程不够灵活时使用；Gmsh + GetDP 为官方推荐的组合 |
| **Repo** | https://gitlab.onelab.info/getdp/getdp |

---

### 4.7 Post-processing / Optimization

此层不指定单一工具，使用 Python 科学计算生态：

| 工具 | 用途 |
|------|------|
| **numpy** | 数组运算，所有求解器输出的基础 |
| **scipy.optimize** | 参数优化、曲线拟合 (Lorentzian 等) |
| **matplotlib** | 静态图表（光谱、能带图、场分布） |
| **PyVista** | 三维场分布可视化（基于 VTK） |
| **scikit-learn** (备选) | 如果未来需要 ML 辅助优化或代理模型 |

---

## 5 工具一览表

| 工具 | 层 | 许可证 | Python API | macOS | 脚本优先 | 状态 |
|------|----|--------|------------|-------|----------|------|
| **Meep** | 电磁仿真 (FDTD) | GPL-2.0 | 原生 | ✅ | ✅ | 主线 |
| **MPB** | 能带/特征模 | GPL-2.0 | 原生 | ✅ | ✅ | 主线 |
| **Gmsh** | 几何/网格 | GPL-2.0 | 原生 | ✅ | ✅ | 主线 |
| **Elmer** | 电磁仿真 (FEM) | GPL-2.0 | CLI+SIF | ✅ | ✅ | 主线 |
| **Optiland** | 成像光学 | MIT | 原生 | ✅ | ✅ | 主线 |
| **RayOptics** | 文件兼容 | BSD-3 | 原生 | ✅ | ✅ | 主线（兼容层） |
| **FreeCAD** | 参数化 CAD | LGPL-2.1 | Headless | ✅ | 部分 | 辅助 |
| **GetDP** | 通用 FEM | GPL-2.0 | CLI+.pro | ✅ | ✅ | 备选 |
| **Raypier** | 非序列追迹 | MIT | 绑定 | ✅ | ✅ | 候选 |

---

## 6 结论：主线开源栈定义

### 主线栈 (Primary Stack)

| 角色 | 工具 | 接入优先级 |
|------|------|-----------|
| **FDTD 电磁仿真** | Meep | P0 — roadmap v0.3 已规划 |
| **能带/特征模** | MPB | P1 — 与 Meep 同生态，接入成本低 |
| **FEM 多物理场** | Elmer | P1 — 补充 FDTD 不覆盖的 FEM 需求 |
| **几何/网格** | Gmsh | P1 — Elmer 前置依赖 |
| **成像光学/序列追迹** | Optiland | P2 — 开启光学设计方向 |
| **商业文件兼容** | RayOptics | P2 — 读取 .zmx/.seq |
| **后处理** | numpy/scipy/matplotlib/PyVista | P0 — 所有求解器共用 |

### 候选/备选 (Secondary)

| 角色 | 工具 | 说明 |
|------|------|------|
| **通用 FEM** | GetDP | Elmer 不够灵活时的备选 |
| **参数化 CAD** | FreeCAD | 复杂机械结构建模时启用 |
| **非序列追迹/照明** | Raypier | 项目成熟度待观察，LightTools 替代的当前最优选 |

### 不纳入主线的方向

| 排除项 | 原因 |
|--------|------|
| Zemax / CODE V | 商业闭源，许可证限制自动化 |
| LightTools | 商业闭源 |
| COMSOL | 商业闭源，Java API 不适合 agent |
| Lumerical | 商业闭源（roadmap v0.4 原计划接入，建议替换为 Elmer） |
| FEniCS | 功能强大但学习曲线陡峭，API 变动较大，作为远期备选 |

### 对 roadmap 的影响

README roadmap 已按开源主线调整。变更要点：

- v0.4 和 v0.5 不再是 Lumerical / COMSOL adapter，改为 MPB 和 Gmsh+Elmer
- 新增 v0.6 Optiland / RayOptics 成像光学方向
- LLM parser 推迟到 v0.7，优先完成 spec hardening 和第一个 solver adapter
- v0.8 才开始 multi-agent orchestration

详见 [README.md Roadmap](../README.md#roadmap)。

---

## 附录 A：安装快速参考

```bash
# 主线工具
pip install meep          # FDTD (或 conda install pymeep)
pip install gmsh          # 几何/网格
pip install optiland      # 成像光学
pip install rayoptics     # 文件兼容

# MPB (conda 优先)
conda install -c conda-forge mpb

# Elmer
brew install elmer        # macOS

# 候选工具
pip install raypier       # 非序列追迹
brew install freecad      # 参数化 CAD
brew install getdp        # 通用 FEM

# 后处理
pip install numpy scipy matplotlib pyvista
```

---

## 附录 B：工具间数据流

```
                    optical-spec-agent
                          │
                    spec JSON
                          │
            ┌─────────────┼─────────────┐
            ▼             ▼             ▼
         Meep          Gmsh         Optiland
        (FDTD)      (几何/网格)    (成像光学)
            │             │             │
            │        ┌────┴────┐        │
            │        ▼         ▼        │
            │     Elmer     GetDP       │
            │     (FEM)    (备选)       │
            │        │                  │
            ▼        ▼                  ▼
      numpy arrays  .vtu/.dat     ray tables
            │        │                  │
            └────────┼──────────────────┘
                     ▼
              Post-processing
         (scipy, matplotlib, PyVista)
```
