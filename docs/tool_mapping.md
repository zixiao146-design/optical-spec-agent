# 商业光学软件 → 开源工具栈映射表

> **核心立场**: 开源世界更适合"模块化工具栈"模式，不应追求单一软件完全替代商业软件。
> 对 agent 而言，脚本可控性比 GUI 一体化更重要。

---

## 1 映射总表

| 商业软件 | 开源候选 | 关系 | 项目优先级 |
|----------|----------|------|-----------|
| **Zemax** | Optiland, RayOptics | 多工具组合 | 主线 |
| **CODE V** | RayOptics, Optiland | 多工具组合 | 主线（兼容层） |
| **LightTools** | Raypier, Optiland | 部分替代 | 候选 |
| **COMSOL** | Elmer, Gmsh, GetDP | 多工具链 | 主线 |

> 下方逐行展开。每个映射都标注了"不是 1:1 平替"。

---

## 2 Zemax → Optiland + RayOptics

**定位**: Zemax 是序列光线追迹、透镜设计优化、像差分析的行业标准。

### 不是 1:1 平替

Zemax 是一个集成度极高的 GUI 应用，包含全局优化器、公差分析、非序列模式等。
开源候选需要多个工具组合才能覆盖其核心功能。

### 映射详情

| 维度 | Zemax | 开源替代 |
|------|-------|----------|
| 序列光线追迹 | 内置 | **Optiland** — 纯 Python，API 完整 |
| 像差分析 (Seidel, Zernike) | 内置 | **Optiland** — 支持 |
| MTF / 点列图 / 光扇图 | 内置 | **Optiland** — 支持常用评价函数 |
| 透镜优化 | 内置全局+局部优化器 | **Optiland** — 内置局部优化器；全局优化需自行组合 scipy |
| 读取 .zmx 文件 | 原生 | **RayOptics** — 专门做这个 |
| 公差分析 | 内置 | 无成熟开源替代 |
| 非序列模式 | 内置 | 不在此映射范围（见 LightTools） |

### 适合替代的任务

- 从零定义透镜系统并追迹评价
- 像差分析、MTF 计算
- 局部优化（damped least squares）
- 读取已有 Zemax 设计文件进行后续分析

### 明显不足

- 无内置全局优化器（需组合 scipy.optimize 或 optuna）
- 无公差分析模块
- 非序列追迹不在这两个工具范围内
- 光机结构分析缺失

### macOS & agent 适配

| 指标 | Optiland | RayOptics |
|------|----------|-----------|
| macOS | ✅ 纯 Python，无系统依赖 | ✅ 纯 Python |
| 脚本调用 | ✅ 原生 Python API | ✅ Python API |
| GUI 依赖 | 无 | 可选 Qt 前端 |
| 适合 agent | ✅ 非常适合 | ✅ 适合 |

### 本项目优先级

- **Optiland**: 主线 — v0.6 adapter 目标
- **RayOptics**: 主线（兼容层）— 读取 .zmx/.seq 文件

---

## 3 CODE V → RayOptics + Optiland

**定位**: CODE V 是高精度镜头设计软件，与 Zemax 形成竞争，偏重优化算法。

### 不是 1:1 平替

CODE V 的优化算法和公差分析在光学设计领域有独特优势，开源工具无法复制其算法深度。
映射策略与 Zemax 相同：用 Optiland 做新设计，RayOptics 读取已有 .seq 文件。

### 映射详情

| 维度 | CODE V | 开源替代 |
|------|--------|----------|
| 序列追迹 | 内置 | **Optiland** |
| 读取 .seq 文件 | 原生 | **RayOptics** — 直接支持 |
| 优化算法 | AUTO (全局) + 局部 | **Optiland** 局部 + scipy 组合 |
| 偏振追迹 | 内置 | **Optiland** 部分支持 |
| 干涉图分析 | 内置 | 无成熟替代 |

### 适合替代的任务

- 读取已有 CODE V 设计文件 (.seq)
- 基础序列追迹和像差评价
- 简单透镜优化

### 明显不足

- CODE V 的全局优化算法无法替代
- 干涉图、鬼像分析等专业功能无替代
- 偏振追迹覆盖不完整

### macOS & agent 适配

同 Zemax 映射（工具相同）。

### 本项目优先级

- **RayOptics**: 主线（兼容层）— .seq 文件读取
- **Optiland**: 主线 — 新设计

---

## 4 LightTools → Raypier + Optiland (部分)

**定位**: LightTools 是非序列光线追迹和照明设计的专业工具，用于光源建模、
杂散光分析、背光模组设计等。

### 不是 1:1 平替

这是四组映射中替代难度最高的。LightTools 的光源模型库、蒙特卡洛追迹、
照度分布计算在开源世界没有对等方案。Raypier 是目前最接近的方向，但项目成熟度有限。

### 映射详情

| 维度 | LightTools | 开源替代 |
|------|------------|----------|
| 非序列追迹 | 内置 | **Raypier** — Rust 核心 + Python 绑定 |
| 光谱渲染 | 内置 | **Raypier** — 光谱追迹是其特色 |
| 光源建模 | 丰富库 | **Raypier** — 需手动定义 |
| 照度分布 | 内置 | 需后处理（matplotlib / PyVista） |
| 杂散光分析 | 内置 | 无成熟替代 |
| 背光模组设计 | 内置 | 无替代 |

### 适合替代的任务

- 简单非序列追迹（光源 → 光学元件 → 探测器）
- 光谱渲染类问题
- Meep 近场 + 远场变换可补充部分散射/衍射照明问题

### 明显不足

- Raypier 项目较新，API 可能变动
- 无光源模型库，每个光源需手动定义
- 杂散光、背光模组等复杂照明问题暂无方案
- 无内置照度分析后处理

### macOS & agent 适配

| 指标 | Raypier |
|------|---------|
| macOS | ✅ pip install raypier |
| 脚本调用 | ✅ Python API |
| GUI 依赖 | 无 |
| 适合 agent | ⚠️ 可用但 API 稳定性待观察 |

### 本项目优先级

- **Raypier**: 候选 — 等待项目成熟度提升后再决定是否纳入主线

---

## 5 COMSOL → Elmer + Gmsh + GetDP

**定位**: COMSOL 是多物理场有限元平台，在光学领域主要用于波导模式分析、
电磁散射 FEM、热光耦合等。GUI 驱动，Java API 可编程。

### 不是 1:1 平替

COMSOL 的核心价值是"一个 GUI 建模所有物理场"。
开源策略是把各物理场拆给专业工具：Elmer 做多物理场 FEM，
Gmsh 做网格，GetDP 做自定义 PDE。
工具链更长，但每一步都可脚本化、可审计、可复现。

### 映射详情

| 维度 | COMSOL | 开源替代 |
|------|--------|----------|
| 几何建模 | 内置 CAD | **Gmsh** 脚本 / **FreeCAD** 参数化 CAD |
| 网格生成 | 内置 | **Gmsh** — 开源 FEM 网格的事实标准 |
| 电磁 FEM | AC/DC + RF 模块 | **Elmer** — Whitaker + vector Helmholtz solver |
| 热传导 | 传热模块 | **Elmer** — 内置热传导求解器 |
| 结构力学 | 固体力学模块 | **Elmer** — 内置弹性力学 |
| 多物理场耦合 | 拖拽式 GUI | **Elmer** — .sif 文件定义耦合 |
| 自定义 PDE | 弱形式输入 | **GetDP** — 专门做这个 |
| 后处理 | 内置 | **PyVista** / **matplotlib** |
| GUI | 内置（核心卖点） | 无对等替代（这是 feature，不是 bug） |

### 适合替代的任务

- 波导模式分析（Elmer vector Helmholtz）
- 电磁散射 FEM（与 Meep FDTD 互补）
- 热-光耦合分析（Elmer 多物理场）
- 自定义 PDE 求解（GetDP）

### 明显不足

- 无 COMSOL 式 GUI（建模完全脚本化，学习曲线不同）
- 物理场预设不如 COMSOL 丰富（需手动写方程）
- 材料/边界条件的图形化设置缺失
- 多物理场耦合配置比 COMSOL 繁琐（但更可复现）

### macOS & agent 适配

| 指标 | Elmer | Gmsh | GetDP |
|------|-------|------|-------|
| macOS | ✅ brew / conda | ✅ pip / conda | ✅ brew |
| 脚本调用 | ✅ CLI + .sif 文本 | ✅ Python API + CLI | ✅ CLI + .pro 文本 |
| GUI 依赖 | 可选 ElmerGUI | 可选 Gmsh GUI | 无 GUI |
| 适合 agent | ✅ .sif 模板化生成 | ✅ Python API 建模 | ✅ .pro 模板化生成 |

### 本项目优先级

- **Gmsh + Elmer**: 主线 — v0.5 adapter 目标
- **GetDP**: 备选 — Elmer 不够灵活时启用

---

## 6 核心观点总结

### 为什么"模块化工具栈"比"单一替代"更适合

| 维度 | 单一商业软件 | 模块化开源栈 |
|------|-------------|-------------|
| 覆盖范围 | 一个软件覆盖多物理场 | 每个领域用最专业的工具 |
| 自动化 | 受限于软件提供的 API | 每个环节都可脚本控制 |
| 可复现 | 依赖特定版本 GUI 操作 | 全流程文本化，git 可追踪 |
| 成本 | 高额许可证 | 零许可证成本 |
| 学习曲线 | 学一个 GUI | 学多个 CLI/API |
| agent 友好度 | 低 — GUI 流程难以自动化 | 高 — 每步都是函数调用 |

### 为什么脚本可控性 > GUI 一体化

对 optical-spec-agent 而言：
1. agent 生成的是文本（spec JSON → solver script），不是鼠标操作
2. 每步输出可被下游程序消费（script → stdout → parse）
3. 全流程可 git 版本化，可 CI/CD
4. GUI 的一体化对人类用户友好，对 agent 反而是障碍

---

## 7 结论：优先级排列

### 当前最优先支持（主线）

| 工具 | 替代方向 | Adapter 版本 |
|------|---------|-------------|
| **Meep** | Zemax/Lumerical 的 FDTD 部分 | v0.3 |
| **MPB** | 光子晶体能带计算 | v0.4 |
| **Gmsh + Elmer** | COMSOL FEM 链路 | v0.5 |
| **Optiland** | Zemax/CODE V 成像光学 | v0.6 |
| **RayOptics** | 读取 .zmx/.seq 文件 | v0.6 |

### 暂时保留在候选列表

| 工具 | 原因 |
|------|------|
| **Raypier** | 项目成熟度不足，等待 API 稳定 |
| **GetDP** | Elmer 主线先行，GetDP 在 Elmer 不够灵活时启用 |
| **FreeCAD** | 复杂几何的补充前端，Gmsh .geo 脚本够用时不需要 |

### 明确不纳入

| 工具 | 原因 |
|------|------|
| Zemax / CODE V / LightTools / COMSOL / Lumerical | 商业闭源，许可证限制自动化和分发 |
