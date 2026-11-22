# W09 工位与机器人层世界模型

> 阶段：S2 子级：机器人与工位　·　总看板：[research_board.html](../research_board.html#W09)

预测机器人动作和设备状态变化在工位上的后果，并向整厂层报告预计耗时和成功率。本工作不限定实现路线。

| 上游（交付物） | 下游（交付物） | 所在闭环 |
|---|---|---|
| [W05（机器人动作数据生成）](../W05_机器人动作数据生成/README.md)：仿真示范与转移<br>[W07（真实数据采集与同步）](../W07_真实数据采集与同步/README.md)：真实数据<br>[W08（仿真—真实对齐）](../W08_仿真真实对齐/README.md)：校准参数与残差<br>[W11（反事实与主动数据）](../W11_反事实与主动数据/README.md)：反事实数据 | [W12（子级技能与端口）](../W12_子级技能与端口/README.md)：模型内规划与评估<br>[W10（整厂层世界模型）](../W10_整厂层世界模型/README.md)：工位预测与自报告<br>[W16（基准与评测）](../W16_基准与评测/README.md)：待评测模型 | ① 主动与反事实数据<br>④ 世界模型—策略协同<br>⑤ 跨层一致 |

## 1. 为什么要做

这一层对应 [L1](../../链路/L1_STEP资产化与物理仿真/README.md)、[L2](../../链路/L2_扫描配准与数字孪生/README.md)、[L6](../../链路/L6_仿真加学习混合/README.md)–[L10](../../链路/L10_视频世界模型/README.md) 等链路，本工作不在其中做选择。不论用哪条链路，工厂工位都多出两个要求：一是设备状态（门、夹具、主轴、程序段）既是输入也是输出；二是要给整厂层一个可用的摘要，例如“这次上料预计多少秒、成功概率多少”。已有的动作条件世界模型，如 V-JEPA 2-AC [P05](../../papers/P05_V_JEPA_2_2506.09985v1.pdf)、DINO-WM [P07](../../papers/P07_DINO_WM_2411.04983v2.pdf)、PointWorld [P44](../../papers/P44_PointWorld_2601.03782v1.pdf)、LeWorldModel [P55](../../papers/P55_LeWorldModel_2603.19312v3.pdf)，从摘要看都只以机器人动作为条件。WorldEcho 发现，动作条件的机器人世界模型不一定真的遵循给定动作 [P77](../../papers/P77_WorldEcho_2608.24885v2.pdf)，评测时要专门检查。

## 2. 输入与产物

**输入**

- [W05（机器人动作数据生成）](../W05_机器人动作数据生成/README.md)、[W07（真实数据采集与同步）](../W07_真实数据采集与同步/README.md) 的数据
- [W08（仿真—真实对齐）](../W08_仿真真实对齐/README.md) 的校准结果与残差
- [W04（设备逻辑与事件日志）](../W04_设备逻辑与事件日志/README.md) 的设备状态
- [W11（反事实与主动数据）](../W11_反事实与主动数据/README.md) 的反事实数据

**产物**

- 动作条件的工位预测器（任一链路实现），提供 reset、assimilate、predict 接口（见 report.html 的统一接口）
- 不确定性估计（供 [W11（反事实与主动数据）](../W11_反事实与主动数据/README.md)）
- 自报告：预计耗时、成功概率、置信度（供 [W10（整厂层世界模型）](../W10_整厂层世界模型/README.md)）

## 3. 具体工作

1. 按 [00 总览](../../链路/00_总览_工厂级世界动作模型/README.md) 和各链路文件夹选一种或几种表示；本工作只规定接口和评测。
2. 把设备状态加入模型的输入和输出，检查模型能否预测设备状态的变化，例如门开到位的时间。
3. 任务涉及加工、形变或流体时，按 [形变专题](../../链路/专题_形变流体断裂与加工/README.md) 补过程代理：物理信息神经网络 [arXiv 1711.10561](https://arxiv.org/abs/1711.10561)、傅里叶神经算子 [arXiv 2010.08895](https://arxiv.org/abs/2010.08895)、MeshGraphNets [P32](../../papers/P32_MeshGraphNets_2010.03409v4.pdf)、GNS [P31](../../papers/P31_Graph_Network_Simulator_2002.09405v2.pdf)。
4. 估计不确定性，例如用模型集成的分歧 [arXiv 1906.04161](https://arxiv.org/abs/1906.04161)，供 [W11（反事实与主动数据）](../W11_反事实与主动数据/README.md) 选择要生成的数据。
5. 从模型推出技能耗时与成功率，再用 [W07（真实数据采集与同步）](../W07_真实数据采集与同步/README.md) 或仿真试验标定。
6. 评测：同初态不同动作的对照；动作遵循性检查 [P77](../../papers/P77_WorldEcho_2608.24885v2.pdf)；多步误差随预测时长的变化。
7. 视频与动作联合建模也是一类实现：UWM [arXiv 2504.02792](https://arxiv.org/abs/2504.02792)、UVA [arXiv 2503.00200](https://arxiv.org/abs/2503.00200)、WorldVLA [arXiv 2506.21539](https://arxiv.org/abs/2506.21539)、OpenWAM [arXiv 2610.07922](https://arxiv.org/abs/2610.07922)、Ctrl-World [P72](../../papers/P72_Ctrl_World_2510.10125v3.pdf)、DreamDojo [P75](../../papers/P75_DreamDojo_2602.06949v1.pdf)、RoboJEPA [P57](../../papers/P57_RoboJEPA_2610.10515v1.pdf)。

## 4. 可以写成论文的方向

### 4.1 以设备状态为条件的工位世界模型

- 类型：方法
- 研究问题：把 PLC／NC 状态作为条件和预测目标后，工位世界模型的预测误差和规划成功率怎样变化？
- 已有工作与空白：上述动作条件世界模型以机器人动作为条件（依据其摘要判断）；工厂工位的结果强烈依赖设备状态。
- 怎样验证：比较有无设备状态输入的模型：设备状态预测准确率、几何误差、规划成功率。

### 4.2 可校准的子级自报告

- 类型：方法（与 W10、W12 衔接）
- 研究问题：怎样从工位世界模型得到技能耗时和成功率的估计，并让它在统计上校准？
- 已有工作与空白：KnowNo 用保形预测给 LLM 规划器提供统计保证 [arXiv 2307.01928](https://arxiv.org/abs/2307.01928)；FAIL-Detect 用保形预测做运行时失败检测 [arXiv 2503.08558](https://arxiv.org/abs/2503.08558)。为上层规划提供校准的耗时与成功率估计，还未见专门研究（分析判断）。
- 怎样验证：校准曲线：预测成功率与实际成功率；整厂层使用这些自报告规划时的收益。

### 4.3 工厂任务上的动作遵循性评测

- 类型：评测
- 研究问题：在工厂任务上，世界模型是否真的按给定动作做预测？
- 已有工作与空白：WorldEcho 在机器人操作上提出了诊断方法和指标 [P77](../../papers/P77_WorldEcho_2608.24885v2.pdf)。
- 怎样验证：同初态不同动作时，预测差异与真实差异的一致性。

## 5. 所在闭环

- ① 主动与反事实数据：W09·W10 找出误差大或不确定的状态 → W11 选状态，设计动作扰动 → W03·W04·W05 从快照复位，执行并记录 → 回训模型。OpenWAM 报告，加入反事实监督后前向动力学的 RGB 预测误差下降 34.5% [arXiv 2610.07922](https://arxiv.org/abs/2610.07922)；Plan2Explore 用模型集成的分歧选择探索目标 [arXiv 2005.05960](https://arxiv.org/abs/2005.05960)。
- ④ 世界模型—策略协同：W09·W10 预测动作后果 → W12·W14 在模型中规划或训练 → 仿真或真实执行 记录新轨迹 → 更新模型。World-in-World 发现，用动作—观测数据做后训练，比换用更强的预训练视频生成器更有效 [arXiv 2510.18135](https://arxiv.org/abs/2510.18135)；DreamerV3、TD-MPC2 交替更新模型与策略 [P02](../../papers/P02_DreamerV3_2301.04104v2.pdf) [P03](../../papers/P03_TD_MPC2_2310.16828v2.pdf)。
- ⑤ 跨层一致：W12 执行技能，返回事件与实际耗时 → W09 工位层预测同一事件 → W10 整厂层预测同一事件 → W14 按预测下发新命令 → 下发命令。[L11](../../链路/L11_工厂级世界动作模型_FWAM/README.md) Idea 3 提出跨层一致性训练，尚未验证；H-WM 联合预测逻辑状态和视觉状态的转移 [arXiv 2602.11291](https://arxiv.org/abs/2602.11291)。

## 6. 对应的链路

- [L1](../../链路/L1_STEP资产化与物理仿真/README.md)：L1 STEP 资产化＋物理仿真作为世界模型
- [L2](../../链路/L2_扫描配准与数字孪生/README.md)：L2 扫描配准到 STEP 资产，并校准成数字孪生
- [L6](../../链路/L6_仿真加学习混合/README.md)：L6 仿真＋学习混合：残差、外观与快速代理
- [L7](../../链路/L7_三维动作条件动力学/README.md)：L7 扫描场景中的三维动作条件动力学
- [L8](../../链路/L8_JEPA特征空间世界模型/README.md)：L8 JEPA 特征空间世界模型
- [L9](../../链路/L9_潜变量模型式强化学习/README.md)：L9 潜变量模型式强化学习
- [L10](../../链路/L10_视频世界模型/README.md)：L10 视频世界模型：合成数据与策略评估
- [形变专题](../../链路/专题_形变流体断裂与加工/README.md)：专题：形变、流体、断裂与加工

## 7. 算力

- LeWorldModel 有 15M 参数，单张 GPU 几小时可训练 [P55](../../papers/P55_LeWorldModel_2603.19312v3.pdf)，适合 3090／4090。
- RoboJEPA 的预测器最大到 80 亿参数 [P57](../../papers/P57_RoboJEPA_2610.10515v1.pdf)；OpenWAM 从 Wan2.2-5B 出发，用 1 万小时以上视频做预训练 [arXiv 2610.07922](https://arxiv.org/abs/2610.07922)。这两类预训练超出本项目算力，只能用公开权重做微调或评估。

## 8. 高价值参考文献

### 特征空间与三维表示

- **V-JEPA 2: Self-Supervised Video Models Enable Understanding, Prediction and Planning**（2025），[P05 本地 PDF](../../papers/P05_V_JEPA_2_2506.09985v1.pdf)：V-JEPA 2：大规模视频预训练，再做动作条件后训练。
- **DINO-WM: World Models on Pre-trained Visual Features enable Zero-shot Planning**（2024），[P07 本地 PDF](../../papers/P07_DINO_WM_2411.04983v2.pdf)：DINO-WM：在冻结的 DINOv2 特征上学动作条件预测。
- **PointWorld: Scaling 3D World Models for In-The-Wild Robotic Manipulation**（2026），[P44 本地 PDF](../../papers/P44_PointWorld_2601.03782v1.pdf)：PointWorld：以三维点流统一状态与动作。
- **LeWorldModel: Stable End-to-End Joint-Embedding Predictive Architecture from Pixels**（2026），[P55 本地 PDF](../../papers/P55_LeWorldModel_2603.19312v3.pdf)：LeWorldModel：从像素端到端训练的小型 JEPA 世界模型。
- **RoboJEPA: Scaling Robotic Latent World Models**（2026），[P57 本地 PDF](../../papers/P57_RoboJEPA_2610.10515v1.pdf)：RoboJEPA：机器人潜世界模型的缩放研究。

### 视频与动作联合

- **Unified World Models: Coupling Video and Action Diffusion for Pretraining on Large Robotic Datasets**（2025），[arXiv 2504.02792](https://arxiv.org/abs/2504.02792)：UWM：视频扩散与动作扩散耦合，可用无动作视频。
- **Unified Video Action Model**（2025），[arXiv 2503.00200](https://arxiv.org/abs/2503.00200)：UVA：联合优化视频与动作预测。
- **WorldVLA: Towards Autoregressive Action World Model**（2025），[arXiv 2506.21539](https://arxiv.org/abs/2506.21539)：WorldVLA：自回归的动作世界模型。
- **OpenWAM: An Open Framework for Composable World-Action Models**（2026），[arXiv 2610.07922](https://arxiv.org/abs/2610.07922)：OpenWAM：可组合的 WAM 框架，研究反事实数据对动力学模型的作用。
- **Ctrl-World: A Controllable Generative World Model for Robot Manipulation**（2025），[P72 本地 PDF](../../papers/P72_Ctrl_World_2510.10125v3.pdf)：Ctrl-World：多视角可控的操作世界模型。
- **DreamDojo: A Generalist Robot World Model from Large-Scale Human Videos**（2026），[P75 本地 PDF](../../papers/P75_DreamDojo_2602.06949v1.pdf)：DreamDojo：从 4.4 万小时人类视频学世界模型。

### 评测

- **Do Robotic World Models Really Follow Actions? Diagnosing and Aligning Action-Conditioned Generation for Policy Learning**（2026），[P77 本地 PDF](../../papers/P77_WorldEcho_2608.24885v2.pdf)：WorldEcho：诊断世界模型是否遵循动作。

### 过程代理（任务涉及加工、形变时）

- **Physics Informed Deep Learning (Part I): Data-driven Solutions of Nonlinear Partial Differential Equations**（2017），[arXiv 1711.10561](https://arxiv.org/abs/1711.10561)：物理信息深度学习（PINN）。
- **Fourier Neural Operator for Parametric Partial Differential Equations**（2020），[arXiv 2010.08895](https://arxiv.org/abs/2010.08895)：傅里叶神经算子（FNO）。
- **Learning Mesh-Based Simulation with Graph Networks**（2020），[P32 本地 PDF](../../papers/P32_MeshGraphNets_2010.03409v4.pdf)：MeshGraphNets：网格上的学习式仿真。
- **Learning to Simulate Complex Physics with Graph Networks**（2020），[P31 本地 PDF](../../papers/P31_Graph_Network_Simulator_2002.09405v2.pdf)：GNS：粒子图网络仿真。

### 不确定性

- **Self-Supervised Exploration via Disagreement**（2019），[arXiv 1906.04161](https://arxiv.org/abs/1906.04161)：用模型集成的分歧做自监督探索。

## 9. 参考项目

- [facebookresearch/vjepa2](https://github.com/facebookresearch/vjepa2)：V-JEPA 2
- [lucas-maes/le-wm](https://github.com/lucas-maes/le-wm)：LeWorldModel
- [NVlabs/PointWorld](https://github.com/NVlabs/PointWorld)：PointWorld
- [WEIRDLabUW/unified-world-model](https://github.com/WEIRDLabUW/unified-world-model)：UWM
- [ShuangLI59/unified_video_action](https://github.com/ShuangLI59/unified_video_action)：UVA
- [neuraloperator/neuraloperator](https://github.com/neuraloperator/neuraloperator)：神经算子库
- [lululxvi/deepxde](https://github.com/lululxvi/deepxde)：PINN 等物理信息学习库
- [maziarraissi/PINNs](https://github.com/maziarraissi/PINNs)：PINN 原始实现

---

说明：arXiv 文献的标题取自 arXiv 页面元数据（2026-11-22 核对）；P 编号对应 `papers/` 中的本地 PDF；GitHub 仓库已用 `gh api` 核对，均未归档。“分析判断”表示本目录的推断，尚未验证。本文件由 `scripts/build_works.py` 生成，请改 `scripts/works_src/` 后重新生成。
