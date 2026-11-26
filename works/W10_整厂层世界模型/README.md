# W10 整厂层世界模型

> 阶段：S3 整厂层：预测与决策　·　总看板：[research_board.html](../research_board.html#W10)

在实体—关系图上，以派工、路由等整厂动作为条件，预测下一个事件的类型和时间，以及设备、工件、工单的状态变化。

| 上游（交付物） | 下游（交付物） | 所在闭环 |
|---|---|---|
| [W09（工位与机器人层世界模型）](../W09_工位与机器人层世界模型/README.md)：工位预测与自报告<br>[W12（子级技能与端口）](../W12_子级技能与端口/README.md)：技能事件与自报告<br>[W04（设备逻辑与事件日志）](../W04_设备逻辑与事件日志/README.md)：事件日志与显式仿真<br>[W11（反事实与主动数据）](../W11_反事实与主动数据/README.md)：反事实数据 | [W13（多机器人协作）](../W13_多机器人协作/README.md)：联合动作打分<br>[W14（整厂规划与调度）](../W14_整厂规划与调度/README.md)：整厂预测器<br>[W16（基准与评测）](../W16_基准与评测/README.md)：待评测模型 | ① 主动与反事实数据<br>④ 世界模型—策略协同<br>⑤ 跨层一致 |

## 1. 为什么要做

整厂状态不适合用像素表示：工厂太大，PLC 模式、工单和质量这类关键状态在画面里看不到（[L11](../../链路/L11_工厂级世界动作模型_FWAM/README.md) 1.2 节）。可借鉴的方向有四类：图与关系模型（Graph Networks [arXiv 1806.01261](https://arxiv.org/abs/1806.01261)、Interaction Networks [arXiv 1612.00222](https://arxiv.org/abs/1612.00222)、TGN [arXiv 2006.10637](https://arxiv.org/abs/2006.10637)）；事件时间模型（Neural Hawkes [arXiv 1612.09328](https://arxiv.org/abs/1612.09328)、Transformer Hawkes [arXiv 2002.09291](https://arxiv.org/abs/2002.09291)）；车队与多主体预测（DeepFleet [arXiv 2508.08574](https://arxiv.org/abs/2508.08574)、MAPF-World [arXiv 2508.12087](https://arxiv.org/abs/2508.12087)、COMBO [arXiv 2404.10775](https://arxiv.org/abs/2404.10775)）；离散事件仿真的代理模型 [arXiv 2507.10714](https://arxiv.org/abs/2507.10714) [arXiv 2605.27556](https://arxiv.org/abs/2605.27556)。按 WWC（全场统一控制，[00 总览](../../链路/00_总览_工厂级世界动作模型/README.md) 1.3 节），整厂层世界模型是 FWAM 的预测部分：全场的联合动作要先预测后果，才能选择。

## 2. 输入与产物

**输入**

- [W04（设备逻辑与事件日志）](../W04_设备逻辑与事件日志/README.md) 的事件日志与离散事件仿真
- [W09（工位与机器人层世界模型）](../W09_工位与机器人层世界模型/README.md)、[W12（子级技能与端口）](../W12_子级技能与端口/README.md) 的自报告与事件
- [W01（问题定义、接口与评测协议）](../W01_问题定义与接口/README.md) 的图模式
- [W11（反事实与主动数据）](../W11_反事实与主动数据/README.md) 的反事实数据

**产物**

- 事件驱动的整厂图世界模型
- 多步预测与不确定性
- 与显式仿真的速度和误差对比

## 3. 具体工作

1. 先建显式基线：[W04（设备逻辑与事件日志）](../W04_设备逻辑与事件日志/README.md) 的离散事件仿真加规则派工，既是训练数据的来源，也是对照（[L11](../../链路/L11_工厂级世界动作模型_FWAM/README.md) 形态 A）。
2. 状态编码：节点为机器人、机床、工件、工单、缓存、通道段；边为占用、装夹、隶属、相邻。
3. 时间推进：按“下一个事件”推进，预测事件类型与时间。可用时间点过程 [arXiv 1612.09328](https://arxiv.org/abs/1612.09328) [arXiv 2002.09291](https://arxiv.org/abs/2002.09291)，或带事件函数的神经 ODE [arXiv 2011.03902](https://arxiv.org/abs/2011.03902)、Latent ODE [arXiv 1907.03907](https://arxiv.org/abs/1907.03907)。
4. 结构：图 Transformer 或 GNN。DeepFleet 比较了四种结构：机器人中心（97M 参数）、机器人—地面（840M）、图像—地面（900M）、图—地面（13M）[arXiv 2508.08574](https://arxiv.org/abs/2508.08574)。
5. 物体中心与组合式建模：C-SWM [arXiv 1911.12247](https://arxiv.org/abs/1911.12247)、SlotFormer [arXiv 2210.05861](https://arxiv.org/abs/2210.05861)、COMBO [arXiv 2404.10775](https://arxiv.org/abs/2404.10775)；Gamma-World 让多个智能体可交换且可独立控制 [arXiv 2605.28816](https://arxiv.org/abs/2605.28816)。
6. 分层：H-WM 联合预测逻辑状态与视觉状态 [arXiv 2602.11291](https://arxiv.org/abs/2602.11291)；Director [arXiv 2206.04114](https://arxiv.org/abs/2206.04114)；H-JEPA [P56](../../papers/P56_H_JEPA_2610.06805v2.pdf)。
7. 共享状态：World Dreamer v5-lite 把多台机器人的相机特征写入工作空间坐标的共享状态，每台机器人用一个查询读取 [arXiv 2610.37518](https://arxiv.org/abs/2610.37518)，可借鉴到车间平面图。
8. 验收：多步事件时间误差、节点属性误差、吞吐预测误差；推理速度与显式仿真的对比。

## 4. 可以写成论文的方向

### 4.1 事件驱动的整厂图世界模型

- 类型：方法
- 研究问题：以派工动作为条件，在实体—关系图上预测下一个事件的类型、时间和状态变化，精度能否接近离散事件仿真，速度快几个数量级？
- 已有工作与空白：DeepFleet 预测仓储机器人车队，状态是机器人位置、地面标记和物体 [arXiv 2508.08574](https://arxiv.org/abs/2508.08574)；时间点过程模型预测事件时间，但不以动作为条件（分析判断）[arXiv 1612.09328](https://arxiv.org/abs/1612.09328) [arXiv 2002.09291](https://arxiv.org/abs/2002.09291)。本轮检索没有找到同时含机床、机器人和工单的动作条件整厂模型。
- 怎样验证：与 [W04（设备逻辑与事件日志）](../W04_设备逻辑与事件日志/README.md) 的显式仿真比较多步误差与速度；在未见布局上的泛化。

### 4.2 异构实体的组合式世界模型

- 类型：方法
- 研究问题：机床、机器人、AGV、工单的动力学差别很大。怎样按实体类型组合模型，使新增一台设备时只需少量数据？
- 已有工作与空白：COMBO 把多智能体世界模型按智能体分解再组合 [arXiv 2404.10775](https://arxiv.org/abs/2404.10775)；Gamma-World 用单纯形旋转编码表示可交换的多个智能体 [arXiv 2605.28816](https://arxiv.org/abs/2605.28816)。它们处理的是同类智能体，异构实体的组合还很少研究（分析判断）。
- 怎样验证：新增设备类型时的样本效率与误差。

### 4.3 整厂层与工位层的跨层一致性训练

- 类型：方法（闭环 ⑤）
- 研究问题：同一事件（如“CNC-1 在 t 时刻完工”）在两层都有预测。能否让两层互相监督，减少层间不一致？
- 已有工作与空白：[L11](../../链路/L11_工厂级世界动作模型_FWAM/README.md) Idea 3 提出这个设想，尚未验证；H-WM 在逻辑层和视觉层之间做联合预测 [arXiv 2602.11291](https://arxiv.org/abs/2602.11291)。
- 怎样验证：层间预测的一致率；整厂层预测误差的变化。

## 5. 所在闭环

- ① 主动与反事实数据：W09·W10 找出误差大或不确定的状态 → W11 选状态，设计动作扰动 → W03·W04·W05 从快照复位，执行并记录 → 回训模型。OpenWAM 报告，加入反事实监督后前向动力学的 RGB 预测误差下降 34.5% [arXiv 2610.07922](https://arxiv.org/abs/2610.07922)；Plan2Explore 用模型集成的分歧选择探索目标 [arXiv 2005.05960](https://arxiv.org/abs/2005.05960)。
- ④ 世界模型—策略协同：W09·W10 预测动作后果 → W12·W14 在模型中规划或训练 → 仿真或真实执行 记录新轨迹 → 更新模型。World-in-World 发现，用动作—观测数据做后训练，比换用更强的预训练视频生成器更有效 [arXiv 2510.18135](https://arxiv.org/abs/2510.18135)；DreamerV3、TD-MPC2 交替更新模型与策略 [P02](../../papers/P02_DreamerV3_2301.04104v2.pdf) [P03](../../papers/P03_TD_MPC2_2310.16828v2.pdf)。
- ⑤ 跨层一致：W12 执行技能，返回事件与实际耗时 → W09 工位层预测同一事件 → W10 整厂层预测同一事件 → W14 按预测下发新命令 → 下发命令。[L11](../../链路/L11_工厂级世界动作模型_FWAM/README.md) Idea 3 提出跨层一致性训练，尚未验证；H-WM 联合预测逻辑状态和视觉状态的转移 [arXiv 2602.11291](https://arxiv.org/abs/2602.11291)。

## 6. 对应的链路

- [L4](../../链路/L4_PLC联仿与产线离散事件/README.md)：L4 PLC／NC 接入仿真，再接产线离散事件
- [L6](../../链路/L6_仿真加学习混合/README.md)：L6 仿真＋学习混合：残差、外观与快速代理
- [L11](../../链路/L11_工厂级世界动作模型_FWAM/README.md)：L11 工厂级世界动作模型（FWAM）

## 7. 算力

- DeepFleet 的图—地面模型只有 13M 参数 [arXiv 2508.08574](https://arxiv.org/abs/2508.08574)；按 [L11](../../链路/L11_工厂级世界动作模型_FWAM/README.md) 的估计，10M–100M 参数的整厂层模型可在 1–2 张 3090／4090 上训练。

## 8. 高价值参考文献

### 图与关系模型

- **Relational inductive biases, deep learning, and graph networks**（2018），[arXiv 1806.01261](https://arxiv.org/abs/1806.01261)：Graph Networks：关系归纳偏置与图网络框架。
- **Interaction Networks for Learning about Objects, Relations and Physics**（2016），[arXiv 1612.00222](https://arxiv.org/abs/1612.00222)：Interaction Networks：学习物体与关系的动力学。
- **Temporal Graph Networks for Deep Learning on Dynamic Graphs**（2020），[arXiv 2006.10637](https://arxiv.org/abs/2006.10637)：TGN：动态图上的时序图网络。

### 事件时间

- **The Neural Hawkes Process: A Neurally Self-Modulating Multivariate Point Process**（2016），[arXiv 1612.09328](https://arxiv.org/abs/1612.09328)：Neural Hawkes：神经自调制的多元点过程。
- **Transformer Hawkes Process**（2020），[arXiv 2002.09291](https://arxiv.org/abs/2002.09291)：Transformer Hawkes Process。
- **Learning Neural Event Functions for Ordinary Differential Equations**（2020），[arXiv 2011.03902](https://arxiv.org/abs/2011.03902)：为 ODE 学习神经事件函数，处理离散事件与连续动力学的混合。
- **Latent ODEs for Irregularly-Sampled Time Series**（2019），[arXiv 1907.03907](https://arxiv.org/abs/1907.03907)：Latent ODE：不规则采样时间序列。

### 物体中心与组合

- **Contrastive Learning of Structured World Models**（2019），[arXiv 1911.12247](https://arxiv.org/abs/1911.12247)：C-SWM：对比学习的结构化世界模型。
- **SlotFormer: Unsupervised Visual Dynamics Simulation with Object-Centric Models**（2022），[arXiv 2210.05861](https://arxiv.org/abs/2210.05861)：SlotFormer：基于槽的长时视频动力学。
- **COMBO: Compositional World Models for Embodied Multi-Agent Cooperation**（2024），[arXiv 2404.10775](https://arxiv.org/abs/2404.10775)：COMBO：组合式多智能体世界模型。
- **Gamma-World: Generative Multi-Agent World Modeling Beyond Two Players**（2026），[arXiv 2605.28816](https://arxiv.org/abs/2605.28816)：Gamma-World：两人以上的生成式多智能体世界模型。

### 车队与多主体世界模型

- **DeepFleet: Multi-Agent Foundation Models for Mobile Robots**（2025），[arXiv 2508.08574](https://arxiv.org/abs/2508.08574)：DeepFleet：移动机器人车队的基础模型。
- **MAPF-World: Action World Model for Multi-Agent Path Finding**（2025），[arXiv 2508.12087](https://arxiv.org/abs/2508.12087)：MAPF-World：多智能体路径规划的动作世界模型。
- **MA-WAM: Multi-Agent World-Action Model for Test-Time Planning**（2026），[arXiv 2609.31281](https://arxiv.org/abs/2609.31281)：MA-WAM：多智能体测试时规划。
- **World Dreamer v5-lite: A Multi-Robot World Action Model with One Dreamer**（2026），[arXiv 2610.37518](https://arxiv.org/abs/2610.37518)：World Dreamer v5-lite：多机器人共享世界状态。

### 分层

- **H-WM: Robotic Task and Motion Planning Guided by Hierarchical World Model**（2026），[arXiv 2602.11291](https://arxiv.org/abs/2602.11291)：H-WM：逻辑与视觉两层世界模型指导任务与运动规划。
- **Deep Hierarchical Planning from Pixels**（2022），[arXiv 2206.04114](https://arxiv.org/abs/2206.04114)：Director：从像素做分层规划。
- **H-JEPA: End-to-End Learning of Hierarchical World Models for Visual Planning**（2026），[P56 本地 PDF](../../papers/P56_H_JEPA_2610.06805v2.pdf)：H-JEPA：分层 JEPA 世界模型。

### 离散事件仿真的代理模型

- **A Simple Approximate Bayesian Inference Neural Surrogate for Stochastic Petri Net Models**（2025），[arXiv 2507.10714](https://arxiv.org/abs/2507.10714)：随机 Petri 网的神经代理。
- **Accelerating Reinforcement Learning Training Using Simulation Surrogate Models**（2026），[arXiv 2605.27556](https://arxiv.org/abs/2605.27556)：用仿真代理模型加速 RL 训练，在离散事件仿真的服务系统上验证。
- **LLM-Based Exogenous World Modeling for Dynamic Scheduling**（2026），[P38 本地 PDF](../../papers/P38_AWMP_Dynamic_Scheduling_2610.29308v1.pdf)：AWMP：排产世界模型，分离已知转移与外生到达。

## 9. 参考项目

- [pyg-team/pytorch_geometric](https://github.com/pyg-team/pytorch_geometric)：图神经网络库
- [rtqichen/torchdiffeq](https://github.com/rtqichen/torchdiffeq)：神经 ODE，含事件处理
- [ant-research/EasyTemporalPointProcess](https://github.com/ant-research/EasyTemporalPointProcess)：时间点过程模型库

---

说明：arXiv 文献的标题取自 arXiv 页面元数据（2026-11-22 核对，2026-11-27 补充）；P 编号对应 `papers/` 中的本地 PDF；GitHub 仓库已用 `gh api` 核对，均未归档。“分析判断”表示本目录的推断，尚未验证。本文件由 `scripts/build_works.py` 生成，请改 `scripts/works_src/` 后重新生成。
