# 专题：形变、流体、断裂与加工

这不是一条链路，而是任务中可能出现的物理情况。任务涉及这些情况时，每条链路都要补相应的能力：

- 走孪生路线（L1、L2，以及在它们之上运行的 L4、L6），仿真器本身要能表示形变、流体或断裂；
- 走学习路线（L7–L10），训练数据要包含这些现象，还要检查模型是否真的学到了。

原 L5「加工与形变过程模型」已并入本专题第 4 节。为了不打乱已有的交叉引用，L5 编号空着，其余链路编号不变。

报告中的相关章节：[形变与切削](../../report.html#deformation)（现象分类、切削的三个层次、验收指标）；[工厂仿真器实现](../../report.html#simulator)。

## 1. 工厂中会遇到的情况

| 情况 | 工厂中的例子 | 仿真里要表示的状态 |
|---|---|---|
| 一维形变 | 线束布线、带线插头插拔、软管连接 | 中心线形状、弯曲与扭转、与夹具的接触 |
| 二维形变 | 防护帘、包装膜、垫布 | 表面网格、自碰撞、褶皱 |
| 三维软体 | 密封圈、橡胶垫、软质工件 | 体网格或粒子，应力与应变 |
| 颗粒与弹塑性 | 切屑、粉末、可塑材料 | 大量粒子，塑性流动 |
| 液体 | 切削液、润滑油、涂胶、灌装 | 粒子或网格流场，自由液面 |
| 断裂、撕裂、切割 | 脆性件跌落开裂、软料切割 | 连通性改变、新表面、碎片 |
| 材料去除 | 铣、车、钻、去毛刺、打磨 | 工件占用域与去除体积；耦合时还有力、热和变形 |

表中的例子是本目录列举的，不来自文献。

## 2. 各链路要补的能力

| 链路 | 任务涉及上述情况时要补什么 | 参考 |
|---|---|---|
| L1 STEP 资产化＋物理仿真 | 换用或接入支持该材料的求解器（第 3 节）。STEP 只给几何：软体要生成四面体网格或粒子，并补弹性模量、泊松比、粘度、摩擦等参数 | 第 3 节 |
| L2 扫描配准与数字孪生 | 材料参数要用现场观测辨识；形变体的状态维度高、观测不全，运行时同步比刚体难 | PhysTwin 用视频做逆物理，辨识弹簧质点参数 [P21] |
| L3 扫描单体化生成资产 | 软体要从接触面上分离出来并指定材料；外部扫描看不到内部，切开或断裂后露出的新表面没有观测 | DecoupledGaussian [P93]；GaussianFluent 用生成先验补内部，补出的不等于测到的 [P47] |
| L4 PLC 联仿与离散事件 | 产线层不模拟材料，只需要工序时长、质量和报废概率，由第 4 节的加工代理或实测统计提供 | 第 4 节 |
| L6 仿真＋学习混合 | 形变和流体仿真慢，适合训练快速代理；材料参数不准时学残差 | GNS [P31]、MeshGraphNets [P32] |
| L7 三维动作条件动力学 | 点流和高斯可以直接表示形变；断裂和切割会产生新表面，点之间的对应关系会断开 | PointWorld 的实机任务包含可变形物体 [P44]；PhysTwin [P21]；PhysGaussian [P19] |
| L8 JEPA | 训练数据要来自能表示该现象的仿真器或现场；INTACT、SADL 还没有在这类任务上测试 | [L8](../L8_JEPA特征空间世界模型/README.md) 第 4 节「在仿真中训练 JEPA 世界模型」；DINO-WM [P07] |
| L9 潜变量模型式强化学习 | 切割、断裂不可逆，只能在仿真或学习式模型里试错。离线数据、用于规划时，DreamerV3 在绳和颗粒任务上的倒角距离为 2.49 和 1.05，DINO-WM 为 0.41 和 0.26（越小越好） | [P07] |
| L10 视频世界模型 | 能生成形变和流体的画面，但不保证材料守恒和物理一致 | — |
| L11 FWAM | 整厂层不看材料细节，只读工位层报告的时长、成功率、质量和报废概率 | 第 4 节 Idea 1、2 |

## 3. 仿真器能力对照

2026-11-22 按各项目的官方文档或 README 核对。"未见"表示在这些文档里没有找到，不等于一定不支持；选定前要按所用版本再核对一次。表格只列能力，不做排序。

### 3.1 通用仿真器

| 仿真器 | 绳、布、软体 | 颗粒与弹塑性 | 液体 | 切割、断裂（拓扑变化） | 出处 |
|---|---|---|---|---|---|
| MuJoCo 3 | flex／flexcomp：一维单元是胶囊（绳），二维是带半径的三角形（布、壳），三维是四面体（软体） | 未见 | 只有刚体在介质里受的流体力（设密度和粘度），流体本身没有状态 | 未见 | [Deformable objects](https://mujoco.readthedocs.io/en/stable/modeling.html#deformable-objects)、[flex 的维度](https://mujoco.readthedocs.io/en/stable/XMLreference.html#deformable-flex)、[流体力](https://mujoco.readthedocs.io/en/stable/computation/fluid.html) |
| Newton 1.7.0（基于 Warp） | SolverVBD：布、软体与刚体在同一求解器（实验性）；SolverStyle3D：布；SolverFeatherstone、SolverSemiImplicit：软体，布无自碰撞；SolverXPBD：软体为实验性 | SolverImplicitMPM：颗粒和弹塑性材料，支持压力相关屈服（Drucker–Prager）、粘性、剪胀、硬化与软化 | 求解器特性表未列 | 未见 | [求解器特性表](https://newton-physics.github.io/newton/1.7.0/solvers/index.html) [S29]、[SolverImplicitMPM](https://newton-physics.github.io/newton/1.7.0/api/_generated/newton.solvers.SolverImplicitMPM.html) |
| Isaac Lab／PhysX 5 | Isaac Lab 资产有 DeformableObject（文档举例：毛绒玩具、食物、布）和 CableObject | 未见 | PhysX 的 PBD 粒子系统可以模拟流体（SDK 示例 SnippetPBF、多材料 SnippetPBFMultiMat）；粒子布已弃用 | PhysX 可变形体因撕裂、切割改变拓扑时，要更新预计算的碰撞结构、质量与体积，以及仿真网格到碰撞网格的映射 [S6]；具体后端的限制见 [S7] | [Isaac Lab 资产 API](https://isaac-sim.github.io/IsaacLab/main/source/api/lab/isaaclab.assets.html)、[PhysX 粒子系统](https://nvidia-omniverse.github.io/PhysX/physx/5.8.0/docs/ParticleSystem.html)、[PhysX Deformable Volume](https://nvidia-omniverse.github.io/PhysX/physx/5.8.0/docs/DeformableVolume.html) |
| Genesis | FEM（软体）；PBD（布）；IPC（libuipc，示例为机器人遥操作布料） | MPM（示例：沙轮） | PBD 液体；SPH（示例：SPH 与刚体、SPH 与 MPM 耦合） | 示例 cut dragon：刚体刀具切开 MPM 弹性体 | [README](https://github.com/Genesis-Embodied-AI/genesis-world) 写明各求解器共享一个场景和状态；[cut_dragon.py](https://github.com/Genesis-Embodied-AI/genesis-world/blob/main/examples/coupling/cut_dragon.py) |
| SOFA | 以有限元为主的交互仿真，侧重医疗与机器人 | 未见 | 未见 | 支持动态拓扑变化（删除、增加、分离单元），如 `InciseAlongEdge()`、`subDivideTetrahedronsWithPlane()`；另有 SofaCarving 插件 | [拓扑文档](https://sofa-framework.github.io/doc/simulation-principles/topology/)、[sofa-framework/sofa](https://github.com/sofa-framework/sofa) |

### 3.2 专门的基准与研究代码

| 项目 | 覆盖的现象 | 形式与说明 | 出处 |
|---|---|---|---|
| SoftGym | 布、绳、液体（倒水、端水不洒、倒定量水） | 基于 NVIDIA FleX，需要编译 PyFleX；最近一次提交在 2022-11 | [arXiv 2011.07215](https://arxiv.org/abs/2011.07215)、[Xingyu-Lin/softgym](https://github.com/Xingyu-Lin/softgym) |
| AdaptiGraph | 材料自适应的图神经动力学 | DINO-WM 的绳任务出自这项工作，用 FleX 仿真；DINO-WM 编译 PyFleX 的方法也沿用它 [P07] | [arXiv 2407.07889](https://arxiv.org/abs/2407.07889)、[Boey-li/AdaptiGraph](https://github.com/Boey-li/AdaptiGraph) |
| PlasticineLab | 弹性与塑性形变（橡皮泥） | 可微物理，基于 DiffTaichi；最近一次提交在 2023-03 | [arXiv 2104.03311](https://arxiv.org/abs/2104.03311)、[hzaskywalker/PlasticineLab](https://github.com/hzaskywalker/PlasticineLab) |
| FluidLab | 液体、固体、气体 | FluidEngine 为多材料、全可微的物理引擎；最近一次提交在 2023-12 | [arXiv 2303.02346](https://arxiv.org/abs/2303.02346)、[zhouxian/FluidLab](https://github.com/zhouxian/FluidLab) |
| DaXBench | 液体、布、弹塑性及其混合 | 可微形变操作框架，基于 JAX；最近一次提交在 2023-11 | [arXiv 2210.13066](https://arxiv.org/abs/2210.13066)、[AdaCompNUS/DaXBench](https://github.com/AdaCompNUS/DaXBench) |
| DiSECt | 软材料切割 | 有限元＋SDF 接触＋连续损伤，可微，用于切割参数辨识和控制；不能直接外推到金属切削 [P46] | [NVlabs/DiSECt](https://github.com/NVlabs/DiSECt) |
| PhysGaussian | 弹性、金属（塑性）、断裂、沙、粘塑性（泡沫、凝胶） | 高斯＋MPM，主要用于生成物理驱动的动态 [P19] | [XPandora/PhysGaussian](https://github.com/XPandora/PhysGaussian) |
| GaussianFluent | 混合材料、脆性断裂、新的内部表面 | 补内部高斯，用连续损伤 MPM 求解 [P47] | P47 本地 PDF |
| PhysTwin | 绳、布、毛绒玩具、包裹 | 弹簧质点＋高斯外观，从视频辨识物理参数 [P21] | [Jianghanxiao/PhysTwin](https://github.com/Jianghanxiao/PhysTwin) |

自己写求解器时可用的 GPU 框架：[NVIDIA/warp](https://github.com/NVIDIA/warp)（Newton 构建在 Warp 上）、[taichi-dev/taichi](https://github.com/taichi-dev/taichi)（PlasticineLab 基于 DiffTaichi）。

### 3.3 选仿真器时要核对的事

- **与刚体、关节的双向耦合**：机器人和机床是刚体与关节，工件或线缆是形变体，两者要在同一场景里互相施力。Genesis 的 README 写明各求解器共享场景和状态；其他仿真器要看耦合文档或示例。
- **从快照复位与批量推演**：L1 把仿真器当世界模型用时依赖这两点。形变体的状态远大于刚体，要核对保存、恢复和并行环境的接口。
- **拓扑变化后的一致性**：切割、断裂之后，碰撞体、质量、约束和可视网格要同步更新 [S6]。
- **速度**：DINO-WM 报告，形变环境里仿真推进一步约 3.0 s（batch 1），而学到的模型前向一步约 0.014 s（batch 32，A6000）[P07]。在线 MPC 直接用形变仿真往往太慢，这是 L6、L8 用学习式模型的原因之一。
- **材料参数从哪里来**：实验标定、视频逆物理（PhysTwin [P21]）、或在仿真中随机化参数。
- **是否需要梯度**：做参数辨识或轨迹优化时，可微性有用。DiSECt、PlasticineLab、FluidLab、DaXBench 是可微的；Newton 特性表中 SolverFeatherstone 和 SolverSemiImplicit 标为"basic"可微 [S29]。
- **许可证与维护状态**：SoftGym、PlasticineLab、FluidLab、DaXBench 最近一次提交都在 2022–2023 年。SOFA 主体为 LGPL（applications/projects 和 applications/tutorials 为 GPL）；Newton 代码为 Apache-2.0。

## 4. 加工（材料去除）

本节是原 L5 的内容。在 FWAM 中，加工模型是工位层的工艺子模型：整厂层不直接预测切削，但需要它给出的加工时长、质量和报废概率，作为机床节点的属性。

### 思考

- 加工过程决定了整厂层最关心的两件事：工序时长和质量。切削本身的物理细节（切屑、热、磨损）对整厂层来说可以压缩成几个统计量。
- 切削可以分三个层次分别验证：几何去除；过程与结构耦合（力、热、变形）；细观材料与切屑（详见报告[形变与切削](../../report.html#deformation)一节）。几何去除最容易建模，可以先做。
- 第 3 节的通用仿真器里，切割示例都是软材料或弹性体（Genesis cut dragon、SOFA 切口、DiSECt）。金属铣削、车削的材料去除一般用专门的几何方法（dexel、体素、SDF），不在这些仿真器的示例里。

### Idea

1. **加工代理模型**：用精细的加工模型（或实测）生成数据，训练一个小代理，输入刀路、材料和刀具状态，输出时长、尺寸误差和报废概率。整厂层只调用这个代理。
2. **刀具磨损作为整厂状态**：把刀具磨损作为机床节点的属性，让整厂层在决定换刀时能预测它对后续质量的影响。

### 实施路线

1. 毛坯与刀具几何：工件 STEP 作为毛坯；刀路来自 NC 程序。
2. 材料去除：用 dexel、体素或 SDF 扫掠更新工件占用域（可参考 opencamlib）。
3. 力、热、变形：需要时耦合切削力、热流与结构变形模型。
4. 回写：在同步点同时更新几何版本、碰撞体与质量；工件 ID 不变。
5. 校准：用实测的力、温度、尺寸与表面质量校准。

算力：几何去除在 CPU 上即可；耦合有限元需要较多 CPU 时间，一般不用 GPU。

## 5. 验收要看什么

只看渲染效果不够。报告[形变与切削](../../report.html#deformation)一节列了完整清单，要点是：

- 几何：去除体积、残余形状、切口位置与宽度、碎片连通性；
- 物理：力—时间曲线、温升、位移与应变、卸载后的残余形变、断裂时刻、质量收支；
- 制造结果：尺寸与形位公差、表面质量、报废与返工；
- 拓扑与绑定：切开后碰撞体与可视形状一致，约束更新正确，子件与父件的关系可追溯。

## 6. 推荐文献

形变、断裂与切割：
- PhysGaussian [P19]、PhysTwin [P21]、DiSECt [P46]、GaussianFluent [P47]、DecoupledGaussian [P93]
- GaussianBench [P49]：检查高斯物理系统的状态、守恒和材料耦合

加工：
- Tri-Dexel 机器人铣削模拟器 [P48]：经铣削实验验证
- 热—力耦合 NC 模型 [P50]：预测宏观形状误差
- 工业过程 JEPA [P37]：注塑过程的动作推断，可作为学习式工艺代理的参考

学习式模型与仿真：
- DINO-WM [P07]：在 FleX 仿真的绳和颗粒任务上训练潜世界模型
- GNS [P31]、MeshGraphNets [P32]：粒子与网格物理的快速代理
- MuJoCo [P96]、Isaac Lab [P10]

基准：
- SoftGym，[arXiv 2011.07215](https://arxiv.org/abs/2011.07215)
- PlasticineLab，[arXiv 2104.03311](https://arxiv.org/abs/2104.03311)
- FluidLab，[arXiv 2303.02346](https://arxiv.org/abs/2303.02346)
- DaXBench，[arXiv 2210.13066](https://arxiv.org/abs/2210.13066)
- AdaptiGraph，[arXiv 2407.07889](https://arxiv.org/abs/2407.07889)

## 7. 参考项目

- 通用仿真器：[google-deepmind/mujoco](https://github.com/google-deepmind/mujoco)、[newton-physics/newton](https://github.com/newton-physics/newton)、[isaac-sim/IsaacLab](https://github.com/isaac-sim/IsaacLab)、[Genesis-Embodied-AI/genesis-world](https://github.com/Genesis-Embodied-AI/genesis-world)、[sofa-framework/sofa](https://github.com/sofa-framework/sofa)
- 基准：[Xingyu-Lin/softgym](https://github.com/Xingyu-Lin/softgym)、[Boey-li/AdaptiGraph](https://github.com/Boey-li/AdaptiGraph)、[hzaskywalker/PlasticineLab](https://github.com/hzaskywalker/PlasticineLab)、[zhouxian/FluidLab](https://github.com/zhouxian/FluidLab)、[AdaCompNUS/DaXBench](https://github.com/AdaCompNUS/DaXBench)
- 物理与高斯：[XPandora/PhysGaussian](https://github.com/XPandora/PhysGaussian)、[Jianghanxiao/PhysTwin](https://github.com/Jianghanxiao/PhysTwin)、[wangmiaowei/DecoupledGaussian](https://github.com/wangmiaowei/DecoupledGaussian)、[NVlabs/DiSECt](https://github.com/NVlabs/DiSECt)
- 加工几何：[aewallin/opencamlib](https://github.com/aewallin/opencamlib)、[CadQuery/cadquery](https://github.com/CadQuery/cadquery)、[tpaviot/pythonocc-core](https://github.com/tpaviot/pythonocc-core)
- 快速代理：[google-deepmind/deepmind-research](https://github.com/google-deepmind/deepmind-research)（learning_to_simulate、meshgraphnets 目录）
- 自写求解器：[NVIDIA/warp](https://github.com/NVIDIA/warp)、[taichi-dev/taichi](https://github.com/taichi-dev/taichi)

写于 2026-11-22。
